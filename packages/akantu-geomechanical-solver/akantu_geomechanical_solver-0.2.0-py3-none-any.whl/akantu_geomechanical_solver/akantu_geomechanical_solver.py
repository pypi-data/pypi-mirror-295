#!/usr/bin/env python
"""
Implementation of the Akantu Geomechanical simulator.

"""

__author__ = "Emil Gallyamov"
__credits__ = [
    "Emil Gallyamov <emil.gallyamov@epfl.ch>",
]
__copyright__ = (
    "Copyright (©) 2016-2021 EPFL (Ecole Polytechnique Fédérale"
    " de Lausanne) Laboratory (LSMS - Laboratoire de Simulation"
    " en Mécanique des Solides)"
)
__license__ = "LGPLv3"


import numpy as np
import os

try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    prank = comm.Get_rank()
    psize = comm.Get_size()
except ImportError:
    prank = 0

import akantu as aka


class IterativeOptions:
    """
    The class storing iterative parameters and keeping track of Newton and PCG iterations

    Args:
        pcg_maxiterations (int): Prescribes the maximum number of iterations for the partitioned conjugate gradient (PCG) solver.
        newton_maxiterations (int): The maximum number of iterations of the Newton-Raphson (NR) solver.
        f_rtol (float): Relative tolerance that will multiply the initial residuals both of the solid and flow subproblems.
        f_rock_tol (float): Absolute tolerance for the residual of the solid subproblem checked for NR convergence.
        f_flow_tol (float): Absolute tolerance for the residual of the flow subproblem checked both in NR and PCG solvers.
        f0_rock_norm (float): Initial norm of the residual for the solid subproblem.
        f0_flow_norm (float): Initial norm of the residual for the flow subproblem.

    Attributes:
        pcg_maxiterations (int): Stores pcg_maxiterations
        newton_maxiterations (int): Stores newton_maxiterations.
        f_rtol (float): Stores f_rtol.
        f_rock_tol (float): Stores f_rock_tol.
        f_flow_tol (float): Stores f_flow_tol.
        f0_rock_norm (float): Stores f0_rock_norm.
        f0_flow_norm (float): Stores f0_flow_norm.
        pcg_iteration (int): Stores current iteration number of the PCG solver.
        nr_iteration (int): Stores current iteration number of the NR solver.
    """

    def __init__(
        self,
        pcg_maxiterations: int = 10,
        newton_maxiterations: int = 10,
        f_rtol: float = 1.0e-4,
        f_rock_tol: float = 1.0e-8,
        f_flow_tol: float = 1.0e-8,
        f0_rock_norm: float = 1.0,
        f0_flow_norm: float = 1.0,
    ):
        self.pcg_maxiterations = pcg_maxiterations
        self.newton_maxiterations = newton_maxiterations
        self.f_rtol = f_rtol  # value for the check |F|<f_rtol |F_0|
        self.f_rock_tol = f_rock_tol  # value for the check |F|<f_tol
        self.f_flow_tol = f_flow_tol  # value for the check |F|<f_tol
        self.f0_rock_norm = f0_rock_norm
        self.f0_flow_norm = f0_flow_norm
        self.pcg_iteration = 0
        self.nr_iteration = 0

    def check_pcg_cvgence(self, f_norm: float):
        """Checks convergence of the PCG solver by comparing the residual with maximum of two tolerances: relative-tolerance based and absolute one.

        Args:
            f_norm (float): Norm of the residual of the flow subproblem.

        Returns:
            check (bool): True if converged, False if not.
        """
        check = self.isless(
            f_norm, max(self.f_flow_tol, self.f_rtol * self.f0_flow_norm)
        )
        return check

    def check_newton_cvgence(self, res_rock: float, res_flow: float):
        """Checks convergence of the NR solver by comparing residuals of the solid and fluid subproblems with absolute tolerances.

        Args:
            f_norm (float): Norm of the residual of the flow subproblem.

        Returns:
            check (bool): True if converged, False if not.
        """
        cvged = self.isless(
            res_rock, max(self.f_rock_tol, self.f_rtol * self.f0_rock_norm)
        ) and self.isless(res_flow, self.f_flow_tol)
        return cvged

    def isless(self, a: float, b: float, abs_tol=1e-09):
        """Compares two floats with user-provided absolute tolerance.

        Args:
            a (float): First float to compare.
            b (float): Second float to compare.
            abs_tol (float): User-provided absolute tolerance.

        Returns:
            check (bool): True if a is less or equal to b + tolerance, False otherwise.
        """
        return a <= b + abs_tol


class AkantuGeomechanicSolver:
    """
    The class containing the geomechanical solver based on HeatTransferModel and SolidMechanicsModel of Akantu FEM library.
    Currently possible to have faults and fractures with the same hydro-mechanical properties only.

    Args:
        rock_model (SolidMechanicsModel or SolidMechanicsModelCohesive): Reference to the solid subproblem.
        flow_model (HeatTransferModel or HeatTransferModelCohesive): Reference to the flow subproblem.
        alpha (float): Biot coefficient.
        dump_iterations (bool): Boolean indicating dump of every newton iteration.
        update_stiffness (bool): Stiffness of the solid subproblem is updated while solving with Newton-Raphson. Otherwise, initial elastic stiffness is employed.

    Attributes:
        rock_model (aka.SolidMechanicsModel or aka.SolidMechanicsModelCohesive): Stores rock_model.
        flow_model (aka.HeatTransferModel or aka.HeatTransferInterfaceModel): Stores flow_model.
        alpha (float): Stores alpha.
        dump_iterations (bool): Stores dump_iterations.
        update_stiffness (bool): Stores update_stiffness.
        heat_interface_model (bool): A boolean indicating if the flow model is of type HeatTransferInterfaceModel.
        ghost_types (list): Stores possible ghost types.
        rock_dof_manager (aka.DOFManager): Reference to the DOFManager of rock_model
        flow_dof_manager (aka.DOFManager): Reference to the DOFManager of flow_model
        rhs_rock (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing residual for the rock_model
        rhs_flow (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing residual for the flow_model
        r2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing r2 vector of PCG
        x2k (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing x2k vector of PCG
        b1a (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing b1a vector of PCG
        A12x2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing the product [A12]{x2}
        x1k (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing x1k vector of PCG
        A21x1 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing the product [A21]{x1}
        A22x2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing the product [A22]{x2}
        A11x1 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing the product [A11]{x1}
        dx2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing dx2 vector of PCG
        z2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing z2 vector of PCG
        p2 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing p2 vector of PCG
        p1 (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing p1 vector of PCG
        q (aka.SolverVectorDefault or aka.SolverVectorDistributed): Reference to the solver vector containing q vector of PCG
    """

    def __init__(
        self,
        rock_model,
        flow_model,
        alpha: float,
        dump_iterations=False,
        update_stiffness=True,
    ):
        self.rock_model = rock_model
        self.rock_model.getNewSolver(
            "linear_static",
            aka.TimeStepSolverType.static,
            aka.NonLinearSolverType.linear,
        )
        self.rock_model.setIntegrationScheme(
            "linear_static", "displacement", aka.IntegrationSchemeType.pseudo_time
        )
        self.rock_model.setDisplacementRelease(
            self.rock_model.getDisplacementRelease() + 1
        )
        self.rock_model.updateCurrentPosition()
        self.rock_model.assembleStiffnessMatrix(True)

        self.flow_model = flow_model
        self.flow_model.getNewSolver(
            "linear_dynamic",
            aka.TimeStepSolverType.dynamic,
            aka.NonLinearSolverType.linear,
        )
        self.flow_model.setIntegrationScheme(
            "linear_dynamic",
            "temperature",
            aka.IntegrationSchemeType.backward_euler,
            aka.IntegrationScheme._temperature,
        )
        assert self.flow_model.getTimeStep() != 0.0, "Zero time step in flow model"
        self.flow_model.setTimeStep(self.flow_model.getTimeStep(), "linear_dynamic")
        if isinstance(self.flow_model, aka.HeatTransferInterfaceModel):
            self.heat_interface_model = True
        else:
            self.heat_interface_model = False

        self.update_stiffness = update_stiffness
        self.alpha = alpha
        self.ghost_types = [aka._not_ghost, aka._ghost]
        self.rock_dof_manager = self.rock_model.getDOFManager()
        self.flow_dof_manager = self.flow_model.getDOFManager()
        self.rhs_rock = self.rock_dof_manager.getNewGlobalVector("rhs_rock")
        self.rhs_flow = self.flow_dof_manager.getNewGlobalVector("rhs_flow")
        self.r2 = self.flow_dof_manager.getNewGlobalVector("r2")
        self.x2k = self.flow_dof_manager.getNewGlobalVector("x2k")
        self.b1a = self.rock_dof_manager.getNewGlobalVector("b1a")
        self.A12x2 = self.rock_dof_manager.getNewGlobalVector("A12x2")
        self.x1k = self.rock_dof_manager.getNewGlobalVector("x1k")
        self.A21x1 = self.flow_dof_manager.getNewGlobalVector("A21x1")
        self.A22x2 = self.flow_dof_manager.getNewGlobalVector("A22x2")
        self.A11x1 = self.rock_dof_manager.getNewGlobalVector("A11x1")
        self.dx2 = self.flow_dof_manager.getNewGlobalVector("dx2")
        self.z2 = self.flow_dof_manager.getNewGlobalVector("z2")
        self.p2 = self.flow_dof_manager.getNewGlobalVector("p2")
        self.p1 = self.rock_dof_manager.getNewGlobalVector("p1")
        self.q = self.flow_dof_manager.getNewGlobalVector("q")
        self.dump_iterations = dump_iterations

    def update_time_step_A22_solve(self, new_time_step: float):
        """Updates the time step in the flow subpoblem. Necessary for the A_{22} operator in PCG.

        Args:
            new_time_step (float): Value of the new time step.
        """
        self.flow_model.setTimeStep(new_time_step, "linear_dynamic")

    def solve_step(self, delta_u_0, delta_p_0, it_options: IterativeOptions) -> bool:
        """Solves a single time step by the Newton Raphson solver.

        Args:
            delta_u_0 (ndarray[float]): An array containing the first guess for the displacement.
            delta_p_0 (ndarray[float]): An array containing the first guess for the pressure.
            it_options (IterativeOptions): Contains iterative options to be used within NR and PCG

        Returns:
            cvged (bool): True if a is the time step converged, False otherwise.
        """

        # reset the newton tolerance and iteration counter
        it_options.f0_rock_norm = it_options.f_rock_tol / it_options.f_rtol
        it_options.nr_iteration = 0

        u = self.rock_model.getDisplacement()
        p = self.flow_model.getTemperature()
        p_rate = self.flow_model.getTemperatureRate()

        # set pressure rate to zero at the beginning of each step
        p_rate.fill(0)
        du_accum = np.zeros(u.shape)

        # test initial solution
        self.compute_residual_rock(u + delta_u_0, p + delta_p_0, self.rhs_rock)
        self.compute_residual_flow(delta_u_0, self.rhs_flow)
        # residuals without blocked DOFs are used for convergence check
        res_rock_norm_0 = self.getNormWithoutBlockedDOFs(self.rock_model, self.rhs_rock)
        res_flow_norm_0 = self.getNormWithoutBlockedDOFs(self.flow_model, self.rhs_flow)
        # full residual is used to adjust the convergence criterium for solid part
        res_rock_norm_full = self.getNorm(self.rock_model, self.rhs_rock)

        # check convergence of NR solver
        cvged = it_options.check_newton_cvgence(res_rock_norm_0, res_flow_norm_0)
        if prank == 0:
            print(
                f"\nNewton 0 iteration: p res {res_flow_norm_0} vs {it_options.f_flow_tol}; u res {res_rock_norm_0} vs {max(it_options.f_rock_tol, it_options.f_rtol * it_options.f0_rock_norm)}; u res full {res_rock_norm_full}",
                flush=True,
            )
        if cvged:
            u += delta_u_0
            p += delta_p_0
            p_rate += delta_p_0 / self.flow_model.getTimeStep()
            return True
        else:
            # adjust the convergence criterium for the solid subproblem
            it_options.f0_rock_norm = res_rock_norm_full

        #  assembling rhs for the solid subproblem
        self.compute_residual_rock(u, p, self.rhs_rock)

        # assembling rhs for the flow problem (no pressure increase)
        residual_flow = self.flow_model.getExternalHeatRate().copy()
        self.flow_model.assembleInternalHeatRate()
        # internal heat rates are not multiplied by -1 like internal forces
        residual_flow -= self.flow_model.getInternalHeatRate()

        self.rhs_flow.zero()
        self.flow_model.getDOFManager().assembleToGlobalArray(
            "temperature", residual_flow, self.rhs_flow
        )

        while it_options.nr_iteration < it_options.newton_maxiterations:

            it_options.nr_iteration += 1

            # solving a single Newton iteration (linearized problem) by the PCG solver
            delta_u, delta_p = self.pcg_solve(
                delta_u_0, delta_p_0, self.rhs_rock, self.rhs_flow, it_options
            )
            delta_u_0.fill(0)
            delta_p_0.fill(0)

            # update displacement & pressure fields
            u += delta_u
            p += delta_p
            p_rate += delta_p / self.flow_model.getTimeStep()
            du_accum += delta_u

            # update displacement release and current position, so that the stiffness matrix will be reassembled for the next NR iteration
            self.rock_model.setDisplacementRelease(
                self.rock_model.getDisplacementRelease() + 1
            )
            self.rock_model.updateCurrentPosition()

            # update residuals
            self.compute_residual_rock(u, p, self.rhs_rock)
            res_rock_norm = self.getNormWithoutBlockedDOFs(
                self.rock_model, self.rhs_rock
            )
            self.compute_residual_flow(du_accum, self.rhs_flow)
            res_flow_norm = self.getNormWithoutBlockedDOFs(
                self.flow_model, self.rhs_flow
            )

            # assembling stiffness based on the new displacement state
            if self.update_stiffness:
                self.rock_model.assembleStiffnessMatrix(True)

            # output data on a single NR iteration
            delta_u_norm = self.getNorm(self.rock_model, delta_u)
            delta_p_norm = self.getNorm(self.flow_model, delta_p)
            if prank == 0:
                print(
                    f"\nNewton {it_options.nr_iteration} iteration: p res {res_flow_norm} vs {it_options.f_flow_tol}; u res {res_rock_norm} vs {max(it_options.f_rock_tol, it_options.f_rtol * it_options.f0_rock_norm)}; delta u norm {delta_u_norm}; delta p norm {delta_p_norm}",
                    flush=True,
                )

            # check NR convergence
            cvged = it_options.check_newton_cvgence(res_rock_norm, res_flow_norm)

            if self.dump_iterations:
                self.rock_model.dump("solid_mechanics_model")
                self.flow_model.dump("heat_transfer")
                if self.heat_interface_model:
                    self.rock_model.dump("cohesive elements")
                    self.flow_model.dump("heat_interfaces")

            if cvged:
                return True

        return False

    def pcg_solve(self, x1_0, x2_0, b1, b2, it_options: IterativeOptions):
        """Solves a linear two-fields problem by partitioned conjugate gradient methods (see Prevost 1997).

        Args:
            x1_0 (ndarray[float]): An array containing the first guess for the displacement increment.
            x2_0 (ndarray[float]): An array containing the first guess for the pressure increment.
            b1 (aka.SolverVector): A global vector containing the rhs for the solid subproblem.
            b2 (aka.SolverVector): A global vector containing the rhs for the flow subproblem.
            it_options (IterativeOptions): Contains iterative options to be used within NR and PCG

        Returns:
            x1 (ndarray[float]): An array containing the resulting displacement increment.
            x2 (ndarray[float]): An array containing the resulting pressure increment.

        Raises:
            Exception: PCG solver did not converge.
        """

        # assemble / synchronize NORMALS on cohesives before fixing them by assembling internal forces
        self.rock_model.assembleInternalForces()

        # fix normals and openings during pcg solve
        nb_materials = self.rock_model.getNbMaterials()
        for material_id in range(nb_materials):
            material = self.rock_model.getMaterial(material_id)
            if isinstance(material, aka.MaterialCohesive):
                material.fixCohesiveState()

        # get dof managers
        solid_dof_manager = self.rock_model.getDOFManager()
        flow_dof_manager = self.flow_model.getDOFManager()

        self.r2.zero()

        if isinstance(b2, aka.SolverVector):
            self.r2.copy(b2)
        else:
            flow_dof_manager.assembleToGlobalArray("temperature", b2, self.r2)

        # solve for x1
        self.x2k.zero()
        flow_dof_manager.assembleToGlobalArray("temperature", x2_0, self.x2k)
        self.b1a.zero()
        if isinstance(b2, aka.SolverVector):
            self.b1a.copy(b1)
        else:
            solid_dof_manager.assembleToGlobalArray("displacement", b1, self.b1a)
        self.A12x2.zero()
        self.A12Mult(self.x2k, self.A12x2, False)

        self.b1a -= self.A12x2
        self.x1k.zero()
        self.A11SolveLinear(self.b1a, self.x1k)

        # update x1k with the fixed dofs from x1_0
        blocked_dofs_u = self.rock_model.getBlockedDOFs()
        x1_0[np.nonzero(~blocked_dofs_u)] = 0
        solid_dof_manager.assembleToGlobalArray("displacement", x1_0, self.x1k)

        # solve 22
        self.A21x1.zero()
        self.A21Mult(self.x1k, self.A21x1, True)
        self.A22x2.zero()
        self.A22Mult(self.x2k, self.A22x2)
        self.r2 -= self.A21x1
        self.r2 -= self.A22x2

        # take ALL dofs not only free ones
        bn = self.getNorm(self.flow_model, self.r2)

        # set defaults
        it_options.f0_flow_norm = bn

        self.dx2.zero()
        flow_dof_manager.assembleToGlobalArray("temperature", x2_0, self.dx2)
        self.z2.zero()
        self.A22SolveLinear(self.r2, self.z2)
        self.p2.zero()
        self.p2.copy(self.z2)
        rho1 = self.r2.dot(self.z2)
        self.p1.zero()
        self.q.zero()

        cvged = False

        for k in range(it_options.pcg_maxiterations):
            # update current pcg iteration
            it_options.pcg_iteration = k

            self.A12Mult(self.p2, self.A12x2, True)
            self.b1a.copy(self.A12x2)
            self.A11SolveLinear(self.b1a, self.p1)
            self.p1 *= -1
            self.A21Mult(self.p1, self.A21x1, True)
            self.A22Mult(self.p2, self.A22x2)
            self.q.copy(self.A21x1)
            self.q += self.A22x2
            nominator = self.r2.dot(self.z2)
            denominator = self.p2.dot(self.q)
            Alpha = 1.0
            if nominator == 0:
                Alpha = 0
            elif not (nominator == denominator):
                Alpha = nominator / denominator

            # update x1k
            self.x1k.add(self.p1, Alpha)
            self.dx2.copy(self.p2)
            self.dx2 *= Alpha
            self.x2k.add(self.dx2, 1)
            self.r2.add(self.q, -Alpha)

            r2_norm = self.getNormWithoutBlockedDOFs(self.flow_model, self.r2)
            dx2_norm = self.getNormWithoutBlockedDOFs(self.flow_model, self.dx2)

            if prank == 0:
                print(
                    f"\niteration {it_options.pcg_iteration} {os.linesep}r2 {r2_norm} vs. max[r0 {it_options.f0_flow_norm} * {it_options.f_rtol}, rtol {it_options.f_flow_tol}] {os.linesep}dx2 {dx2_norm}"
                )

            cvged = it_options.check_pcg_cvgence(r2_norm)

            if cvged:
                break

            self.A22SolveLinear(self.r2, self.z2)
            r2z2 = self.r2.dot(self.z2)
            Beta = 0.0
            if rho1 != 0:
                Beta = r2z2 / rho1
            self.p2 *= Beta
            self.p2 += self.z2
            rho1 = r2z2

        # end of loop
        if not cvged:
            raise Exception("PCG did not converge after {it_options.pcg_iteration}")

        x1 = np.zeros(x1_0.shape)
        solid_dof_manager.getArrayPerDOFs("displacement", self.x1k, x1)
        x2 = np.zeros(x2_0.shape)
        flow_dof_manager.getArrayPerDOFs("temperature", self.x2k, x2)

        # unfix state of cohesive elements
        nb_materials = self.rock_model.getNbMaterials()
        for material_id in range(nb_materials):
            material = self.rock_model.getMaterial(material_id)
            if isinstance(material, aka.MaterialCohesive):
                material.unfixCohesiveState()

        return x1, x2

    def compute_residual_flow(self, du, residual_flow):
        """Updates the residual to the flow subproblem according to the following equation:
        :math:'\{f^p\}_{n+1} - [C] \{p\}_{n+1} - [S] \{\dot{p}\}_{n+1} - [A_{\textrm{dp}}] \{\dot{u}\}_{n+1}'

        Args:
            du (ndarray[float]): An array with displacement increment.
            residual_flow (aka.SolverVector or ndarray): A global vector containing the residual for the flow subproblem.
        """
        du_copy = du.copy()
        p = self.flow_model.getTemperature()
        p_rate = self.flow_model.getTemperatureRate()
        nb_nodes = self.rock_model.getMesh().getNbNodes()
        p_backup = p.copy()
        p_rate_backup = p_rate.copy()
        residual_array = np.zeros([nb_nodes, 1])
        self.flow_model.getDOFManager().getTimeStepSolver("implicit").assembleResidual()
        self.flow_model.getDOFManager().getArrayPerDOFs(
            "temperature", self.flow_model.getDOFManager().getResidual(), residual_array
        )

        A21du = np.zeros([nb_nodes, 1])
        # A21du is divided by the timestep inside A21Mult function
        self.A21Mult(du_copy, A21du, True)
        residual_array -= A21du

        if isinstance(residual_flow, aka.SolverVector):
            residual_flow.zero()
            self.flow_model.getDOFManager().assembleToGlobalArray(
                "temperature", residual_array, residual_flow
            )
        else:
            np.copyto(residual_flow, residual_array)

        # rollback nodal values
        np.copyto(p, p_backup)
        np.copyto(p_rate, p_rate_backup)

    def compute_residual_rock(self, u_in, p_in, residual_rock):
        """Updates the residual to the solid subproblem according to the following equation:
        :math:'\{f^d\}_{n+1} - [K]\{d\}_{n+1} + [A_{\textrm{pd}}] \{p\}_{n+1}'

        Args:
            u_in (ndarray[float]): An array with the displacement.
            p_in (ndarray[float]): An array with the pressure.
            residual_rock (aka.SolverVector or ndarra): A global vector containing the residual for the solid subproblem.
        """
        nb_nodes = self.rock_model.getMesh().getNbNodes()
        dim = self.rock_model.getSpatialDimension()
        residual_array = self.rock_model.getExternalForce().copy()
        u_copy = u_in.copy()
        p_copy = p_in.copy()
        u = self.rock_model.getDisplacement()
        u_backup = u.copy()
        np.copyto(u, u_copy)
        self.rock_model.assembleInternalForces()

        # internal forces are multiplied by -1 in their assembly in Akantu
        residual_array += self.rock_model.getInternalForce()

        # subtract A12p. "-" sign is already included in A12p assembly
        A12p = np.zeros([nb_nodes, dim])
        self.A12Mult(p_copy, A12p, False)
        residual_array -= A12p

        if isinstance(residual_rock, aka.SolverVector):
            residual_rock.zero()
            self.rock_model.getDOFManager().assembleToGlobalArray(
                "displacement", residual_array, residual_rock
            )
        else:
            np.copyto(residual_rock, residual_array)

        # rollback nodal values
        np.copyto(u, u_backup)

    def A12Mult(self, p, A12x2, ignore_blocked_dofs):
        """Wrapper over A12MultArray. If delta_p is a SolverVector, transforms it into an array and passes to
        A12MultArray. If A12x2 is a SolverVector, transforms the resulting array into the SolverVector.

        Args:
            p (ndarray[float]  or SolverVector): An array with the pressure.
            A12x2 (ndarray or SolverVector): An array with the final product.
            ignore_blocked_dofs (bool): Turns off contribution of blocked pressure dofs to A12p product
        """

        nb_nodes = self.rock_model.getMesh().getNbNodes()
        dim = self.rock_model.getSpatialDimension()
        p_array = np.zeros([nb_nodes, 1])
        A12x2_array = np.zeros([nb_nodes, dim])
        if isinstance(p, aka.SolverVector):
            self.flow_model.getDOFManager().getArrayPerDOFs("temperature", p, p_array)
        else:
            np.copyto(p_array, p)

        self.A12MultArray(p_array, A12x2_array, ignore_blocked_dofs)

        if isinstance(A12x2, aka.SolverVector):
            A12x2.zero()
            self.rock_model.getDOFManager().assembleToGlobalArray(
                "displacement", A12x2_array, A12x2
            )
        else:
            np.copyto(A12x2, A12x2_array)

    def A12MultArray(self, p_array, A12x2_array, ignore_blocked_dofs):
        """Quadpoint-wise multiplication of Apd with pressure.

        Args:
            p_array (ndarray): An array with the pressure.
            A12x2 (ndarray): An array with the final product.
            ignore_blocked_dofs (bool): Turns off contribution of blocked pressure dofs to A12p product
        """

        mesh = self.rock_model.getMesh()
        nb_nodes = mesh.getNbNodes()
        assert nb_nodes == p_array.shape[0], "Wrong dimension of p_array"

        # put fixed pressure values to zero
        p_copy = p_array.copy()
        if ignore_blocked_dofs:
            self.zeroAtBlockedDOFs(self.flow_model, p_copy)

        # interpolate pressures at both solid and cohesive elements
        # p on qpoints is synced in computeTempOnQPoints in model
        self.interpolate_pressure_on_qpoints(p_copy)

        A12x2_array.fill(0.0)
        dim = self.rock_model.getSpatialDimension()

        for ghost_type in self.ghost_types:
            for el_type in mesh.elementTypes(dim, ghost_type, aka._ek_not_defined):
                nb_elements = mesh.getNbElement(el_type, ghost_type)

                if nb_elements == 0:
                    continue

                if mesh.getKind(el_type) == aka._ek_regular:
                    fem = self.rock_model.getFEEngine()
                elif mesh.getKind(el_type) == aka._ek_cohesive:
                    fem = self.rock_model.getFEEngine("CohesiveFEEngine")

                shapes_derivatives = fem.getShapesDerivatives(
                    el_type, ghost_type
                ).copy()
                size_of_shapes_derivatives = shapes_derivatives.shape[1]

                nb_quad_points = fem.getNbIntegrationPoints(el_type)
                nb_nodes_per_element = mesh.getNbNodesPerElement(el_type)

                int_f_dn_dx = np.zeros((nb_elements, nb_nodes_per_element * dim))

                if mesh.getKind(el_type) == aka._ek_regular:
                    # accessing interpolated values
                    # as there is a single material, mesh numbering and material numbering coincide
                    pressure_at_quads = self.flow_model.getTemperatureOnQpoints(
                        el_type, ghost_type
                    )
                    field_tensor_at_quads = np.zeros(
                        (nb_elements * nb_quad_points, dim * dim)
                    )

                    # fill along diagonal with pressure values
                    for i in range(dim):
                        field_tensor_at_quads[:, i + i * dim] = (
                            pressure_at_quads.reshape(nb_elements * nb_quad_points)
                        )

                    # multiplication by shape function derivatives
                    f_dn_dx = np.zeros(
                        (nb_elements * nb_quad_points, size_of_shapes_derivatives)
                    )
                    fem.computeBtD(field_tensor_at_quads, f_dn_dx, el_type, ghost_type)

                    # scaling with alpha
                    f_dn_dx *= self.alpha
                    fem.integrate(
                        f_dn_dx,
                        int_f_dn_dx,
                        size_of_shapes_derivatives,
                        el_type,
                        ghost_type,
                    )

                elif mesh.getKind(el_type) == aka._ek_cohesive:

                    # accessing interpolated values
                    pressure_at_quads = self.flow_model.getTemperatureOnQpointsCoh(
                        el_type, ghost_type
                    )
                    shape_functions = fem.getShapeFunctions()

                    # get normals to cohesives from solid subproblem
                    # this algorithm currently supports only a single cohesive / interface material
                    nb_materials = self.rock_model.getNbMaterials()
                    for material_id in range(nb_materials):
                        material = self.rock_model.getMaterial(material_id)
                        if isinstance(material, aka.MaterialCohesive):
                            normals = material.getNormalsAtQuads(el_type, ghost_type)
                            break

                    # important to transit from material local numbering to mesh global numbering of cohesive elements
                    el_local_numbering = self.rock_model.getMaterialLocalNumbering(
                        el_type, ghost_type
                    ).squeeze()
                    quad_local_numbering = np.zeros(
                        nb_elements * nb_quad_points, dtype=int
                    )
                    for i in range(dim):
                        quad_local_numbering[i::dim] = (
                            el_local_numbering * nb_quad_points + i
                        )
                    normals_global_numbering = normals[quad_local_numbering]

                    # compute pressure force on crack face
                    p_vector = normals_global_numbering.copy()
                    p_vector = np.multiply(p_vector, pressure_at_quads)

                    # compute product of pressure force with shape functions
                    shapes = fem.getShapes(el_type, ghost_type)
                    shape_size = shape_functions.getShapeSize(el_type)
                    p_vec_N = np.zeros((nb_elements * nb_quad_points, dim * shape_size))
                    for _p_vec, _p_vec_N, _shapes in zip(p_vector, p_vec_N, shapes):
                        p_vec_N_view = _p_vec_N.view().reshape(dim, shape_size)
                        np.copyto(p_vec_N_view, np.outer(_p_vec, _shapes).transpose())

                    # partially integrate pressure forces
                    partial_int_p_vec_N = np.zeros((nb_elements, dim * shape_size))
                    fem.integrate(
                        p_vec_N,
                        partial_int_p_vec_N,
                        dim * shape_size,
                        el_type,
                        ghost_type,
                    )

                    # assemble partial in full integral vector
                    for _part_int_p_vec_N, _int_f_dn_dx in zip(
                        partial_int_p_vec_N, int_f_dn_dx
                    ):
                        _int_f_dn_dx[: dim * shape_size] = _part_int_p_vec_N
                        _int_f_dn_dx[dim * shape_size :] = -_part_int_p_vec_N

                # Apd has -1 as a prefactor in the weak form
                int_f_dn_dx *= -1

                # assemble into resulting vector
                self.rock_model.getDOFManager().assembleElementalArrayLocalArray(
                    int_f_dn_dx, A12x2_array, el_type, ghost_type
                )

    def A21Mult(self, du, A21x1, ignore_blocked_dofs):
        """Wrapper over A21MultArray. If delta_p is a SolverVector, transforms it into an array and passes to
        A21MultArray. If A21x1 is a SolverVector, transforms the resulting array into the SolverVector.

        Args:
            delta_u (ndarray[float]  or SolverVector): An array with displacement increment.
            A21x1 (ndarray or SolverVector): An array with the final product.
            ignore_blocked_dofs (bool): Turns off contribution of the blocked displacement dofs to A21du product
        """

        nb_nodes = self.rock_model.getMesh().getNbNodes()
        dim = self.rock_model.getSpatialDimension()
        du_array = np.zeros([nb_nodes, dim])
        A21x1_array = np.zeros([nb_nodes, 1])
        # Pass displacement into an array
        if isinstance(du, aka.SolverVector):
            self.rock_model.getDOFManager().getArrayPerDOFs(
                "displacement", du, du_array
            )
        else:
            np.copyto(du_array, du)

        # call the function operating on arrays
        self.A21MultArray(du_array, A21x1_array, ignore_blocked_dofs)

        # transform final product into a solver vector if needed
        if isinstance(A21x1, aka.SolverVector):
            A21x1.zero()
            self.flow_model.getDOFManager().assembleToGlobalArray(
                "temperature", A21x1_array, A21x1
            )
        else:
            np.copyto(A21x1, A21x1_array)

    def A21MultArray(self, du_array, A21x1_array, ignore_blocked_dofs):
        """Quadpoint-wise multiplication of Adp with displacement increment.

        Args:
            du_array (ndarray): An array with displacement increment.
            A21x1_array (ndarray): An array with the final product.
            ignore_blocked_dofs (bool): Turns off contribution of blocked displacement dofs to the A21du product
        """

        mesh = self.rock_model.getMesh()
        nb_nodes = mesh.getNbNodes()
        assert nb_nodes == du_array.shape[0], "Wrong dimension of du_array"

        du_copy = du_array.copy()
        # set fixed displacement dofs to zero
        if ignore_blocked_dofs:
            self.zeroAtBlockedDOFs(self.rock_model, du_copy)

        dim = self.flow_model.getSpatialDimension()
        A21x1_array.fill(0.0)

        # assemble and synchronize quadrature fields
        for el_type in mesh.elementTypes(dim, aka._not_ghost, aka._ek_not_defined):
            nb_elements = mesh.getNbElement(el_type, aka._not_ghost)

            if mesh.getKind(el_type) == aka._ek_regular:
                # gradu is synced
                self.compute_gradu_on_qpoints(du_copy, el_type)
            elif mesh.getKind(el_type) == aka._ek_cohesive:
                # compute openings of cohesive elements and then synchronize them
                # this algorithm currently supports only a single cohesive / interface material
                nb_materials = self.rock_model.getNbMaterials()
                for material_id in range(nb_materials):
                    material = self.rock_model.getMaterial(material_id)
                    if isinstance(material, aka.MaterialCohesive):
                        delta_opening = material.getOpening(el_type, aka._not_ghost)
                        normals = material.getNormalsAtQuads(el_type, aka._not_ghost)
                        material.computeOpening(
                            du_copy, delta_opening, el_type, aka._not_ghost
                        )
                        break

        # synchronize cohesive openings
        self.rock_model.synchronizeField(aka.smmc_opening)

        # collect computed values from above both on ghosts and not ghosts
        for ghost_type in self.ghost_types:
            for el_type in mesh.elementTypes(dim, ghost_type, aka._ek_not_defined):
                nb_elements = mesh.getNbElement(el_type, ghost_type)

                if nb_elements == 0:
                    continue

                if mesh.getKind(el_type) == aka._ek_regular:
                    fem = self.flow_model.getFEEngine()
                elif mesh.getKind(el_type) == aka._ek_cohesive:
                    fem = self.flow_model.getFEEngine("InterfacesFEEngine")

                nb_quad_points = fem.getNbIntegrationPoints(el_type)
                nb_nodes_per_element = mesh.getNbNodesPerElement(el_type)
                eps_vol = np.zeros((nb_elements * nb_quad_points, 1))

                if mesh.getKind(el_type) == aka._ek_regular:
                    grad_u = np.zeros((nb_elements * nb_quad_points, dim * dim))
                    # function below transits from mat local numbering to mesh global els numbering
                    self.assemble_gradu_global(grad_u, el_type, ghost_type)

                    # extracting the volumetric strain
                    for i in range(dim):
                        eps_vol[:, 0] += grad_u[:, i + i * dim]

                    # scale with Biot's coefficient for bulk elements
                    eps_vol *= self.alpha

                elif mesh.getKind(el_type) == aka._ek_cohesive:
                    # compute jump in displacement increment across cohesive elements
                    nb_materials = self.rock_model.getNbMaterials()
                    for material_id in range(nb_materials):
                        material = self.rock_model.getMaterial(material_id)
                        if isinstance(material, aka.MaterialCohesive):
                            delta_opening = material.getOpening(el_type, ghost_type)
                            normals = material.getNormalsAtQuads(el_type, ghost_type)
                            delta_opening = material.getOpening(el_type, ghost_type)
                            normals = material.getNormalsAtQuads(el_type, ghost_type)
                            break
                    delta_normal_opening = self.computeNormalOpening(
                        delta_opening, normals
                    )

                    # important to transit from material local numbering to mesh global numbering of cohesive elements
                    el_local_numbering = self.rock_model.getMaterialLocalNumbering(
                        el_type, ghost_type
                    ).squeeze()
                    quad_local_numbering = np.zeros(
                        nb_elements * nb_quad_points, dtype=int
                    )
                    for i in range(dim):
                        quad_local_numbering[i::dim] = (
                            el_local_numbering * nb_quad_points + i
                        )
                    delta_normal_opening_global = delta_normal_opening[
                        quad_local_numbering
                    ]

                    eps_vol = delta_normal_opening_global

                # multiplying volumetric strain with shape functions
                eps_vol_by_shapes = np.zeros(
                    (nb_elements * nb_quad_points, nb_nodes_per_element)
                )
                fem.computeNtb(eps_vol, eps_vol_by_shapes, el_type, ghost_type)

                # integration part
                int_Nt_eps_vol = np.zeros((nb_elements, nb_nodes_per_element))
                fem.integrate(
                    eps_vol_by_shapes,
                    int_Nt_eps_vol,
                    nb_nodes_per_element,
                    el_type,
                    ghost_type,
                )

                # divide by the time step
                int_Nt_eps_vol /= self.flow_model.getTimeStep()

                # assemble into resulting vector
                self.flow_model.getDOFManager().assembleElementalArrayLocalArray(
                    int_Nt_eps_vol, A21x1_array, el_type, ghost_type
                )

    def computeNormalOpening(self, opening, normal):
        """Dot product between opening vector and normals to cohesives.

        Args:
            opening (ndarray): An array with opening vectors.
            normal (ndarray): An array with normal vectors.

        Returns:
            normal_opening (ndarray): An array with normal openings.
        """

        normal_opening = np.einsum("ij,ij->i", opening, normal)
        return normal_opening

    def A22Mult(self, p, A22x2):
        """Explicit multiplication of A22 matrix with pressure vector.

        Args:
            p (ndarray or SolverVector): An array with pressures.
            A22x2 (ndarray or SolverVector): An array with final product.
        """

        nb_nodes = self.rock_model.getMesh().getNbNodes()
        dp = np.zeros(nb_nodes)
        p_rate = np.zeros(nb_nodes)

        if isinstance(p, aka.SolverVector):
            self.flow_model.getDOFManager().getArrayPerDOFs("temperature", p, dp)
        else:
            np.copyto(dp, p)

        np.copyto(p_rate, dp / self.flow_model.getTimeStep())

        if not self.flow_model.getDOFManager().hasMatrix("J"):
            self.flow_model.getTimeStepSolver().assembleMatrix("J")

        if isinstance(A22x2, aka.SolverVector):
            A22x2.zero()
            self.flow_model.getDOFManager().assembleMatMulVectToGlobalArray(
                "temperature", "K", dp, A22x2
            )
            self.flow_model.getDOFManager().assembleMatMulVectToGlobalArray(
                "temperature", "M", p_rate, A22x2
            )
        else:
            assert (
                psize == 1
            ), "A22Mult with numpy-array type A22x2 works only in sequential"
            K_ = self.flow_model.getDOFManager().getMatrix("K")
            K = aka.AkantuSparseMatrix(K_)
            M_ = self.flow_model.getDOFManager().getMatrix("M")
            M = aka.AkantuSparseMatrix(M_)
            np.copyto(A22x2, K.dot(dp))
            A22x2 += M.dot(p_rate)

    def A11SolveLinear(self, rhs_solid, solution):
        """Solution of the linear system A11x=b by the Akantu direct solver. Literally x = A11^{inv} b.

        Args:
            rhs_solid (ndarray or SolverVector): Right hand side of the equation.
            solution (ndarray or SolverVector): An array with solution of linear system.
        """

        ext_force = self.rock_model.getExternalForce()
        ext_force_backup = ext_force.copy()
        u = self.rock_model.getDisplacement()
        u_backup = u.copy()
        nb_nodes = self.rock_model.getMesh().getNbNodes()
        dim = self.rock_model.getSpatialDimension()

        # parallelization is taken into account
        rhs_local = np.zeros([nb_nodes, dim])
        if isinstance(rhs_solid, aka.SolverVector):
            self.rock_model.getDOFManager().getArrayPerDOFs(
                "displacement", rhs_solid, rhs_local
            )
        else:
            np.copyto(rhs_local, rhs_solid)
        self.zeroAtBlockedDOFs(self.rock_model, rhs_local)
        np.copyto(ext_force, rhs_local)
        u.fill(0)

        self.rock_model.solveStep("linear_static")

        # roll back the displacement release so that the stiffness is not updated
        self.rock_model.setDisplacementRelease(
            self.rock_model.getDisplacementRelease() - 1
        )

        if isinstance(solution, aka.SolverVector):
            solution.zero()
            self.rock_model.getDOFManager().assembleToGlobalArray(
                "displacement", u, solution
            )
        else:
            np.copyto(solution, u)

        # put back the original values
        np.copyto(u, u_backup)
        np.copyto(ext_force, ext_force_backup)

    def A22SolveLinear(self, rhs_flow, solution):
        """Solution of the linear system A22x=b by the Akantu direct solver. Literally x = A22^{inv} b.

        Args:
            rhs_flow (ndarray or SolverVector): Right hand side of the equation.
            solution (ndarray or SolverVector): An array with solution of the linear system.
        """

        ext_rate = self.flow_model.getExternalHeatRate()
        ext_rate_backup = ext_rate.copy()
        press = self.flow_model.getTemperature()
        press_rate = self.flow_model.getTemperatureRate()
        press_backup = press.copy()
        press_rate_backup = press_rate.copy()
        rhs_local = np.zeros(ext_rate.shape)
        if isinstance(rhs_flow, aka.SolverVector):
            self.flow_model.getDOFManager().getArrayPerDOFs(
                "temperature", rhs_flow, rhs_local
            )
        else:
            np.copyto(rhs_local, rhs_flow)
        self.zeroAtBlockedDOFs(self.flow_model, rhs_local)

        np.copyto(ext_rate, rhs_local)
        press.fill(0)
        press_rate.fill(0)

        self.flow_model.solveStep("linear_dynamic")

        if isinstance(solution, aka.SolverVector):
            solution.zero()
            self.flow_model.getDOFManager().assembleToGlobalArray(
                "temperature", press, solution
            )
        else:
            np.copyto(solution, press)

        # rollback the original values
        np.copyto(press, press_backup)
        np.copyto(press_rate, press_rate_backup)
        np.copyto(ext_rate, ext_rate_backup)

    def getNormWithoutBlockedDOFs(self, model, array):
        """Computes norm of a vector ignoring blocked and ghost dofs.

        Args:
            model (SolidMechanicsModel or HeatTransferModel): Reference to the model.
            array (ndarray or SolverVector): An array whose norm the function is computing.
        """

        if isinstance(array, aka.SolverVector):
            norm = array.normFreeDOFs()
            return norm
        else:
            array_copy = array.copy()
            self.zeroAtBlockedDOFs(model, array_copy)
            self.zeroAtGhosts(model, array_copy)
            array_copy = array_copy.flatten()
            dot = np.dot(array_copy, array_copy)
            dot_reduced = comm.allreduce(dot, op=MPI.SUM)
            norm = np.sqrt(dot_reduced)
            return norm

    def getNorm(self, model, array):
        """Computes norm of a vector including blocked dofs but excluding ghosts.

        Args:
            model (SolidMechanicsModel or HeatTransferModel): Reference to the model.
            array (ndarray or SolverVector): An array whose norm the function is computing.
        """

        if isinstance(array, aka.SolverVector):
            # norm on solver vector includes only local and masters
            norm = array.norm()
            return norm
        else:
            array_copy = array.copy()
            self.zeroAtGhosts(model, array_copy)
            array_copy = array_copy.flatten()
            dot = np.dot(array_copy, array_copy)
            dot_reduced = comm.allreduce(dot, op=MPI.SUM)
            norm = np.sqrt(dot_reduced)
            return norm

    def zeroAtBlockedDOFs(self, model, array):
        """Set blocked DOFs to zero.

        Args:
            model (SolidMechanicsModel or HeatTransferModel): Reference to the model.
            array (ndarray or SolverVector): An array who is being modified.
        """

        if isinstance(model, aka.SolidMechanicsModel):
            # bring blocked dofs to zero
            blocked_dofs_u = self.rock_model.getBlockedDOFs()
            array[blocked_dofs_u.nonzero()] = 0

        else:
            # put to zero at blocked dof positions
            blocked_dofs_p = self.flow_model.getBlockedDOFs()
            array[np.where(blocked_dofs_p)] = 0

    def zeroAtGhosts(self, model, array):
        """Set ghost DOFs to zero.

        Args:
            model (SolidMechanicsModel or HeatTransferModel): Reference to the model.
            array (ndarray or SolverVector): An array who is being modified.
        """

        if isinstance(model, aka.SolidMechanicsModel):
            # put to zero at pure ghost nodes
            node_flags = self.rock_model.getMesh().getNodesFlags()
            pure_ghost_pos = np.asarray(
                node_flags == np.uint8(aka._pure_ghost)
            ).nonzero()[0]
            array[pure_ghost_pos, :] = 0
            # same for slaves
            slave_pos = np.asarray(node_flags == np.uint8(aka._slave)).nonzero()[0]
            array[slave_pos, :] = 0

        else:
            # put to zero at pure ghost nodes
            node_flags = self.flow_model.getMesh().getNodesFlags()
            pure_ghost_pos = np.asarray(
                node_flags == np.uint8(aka._pure_ghost)
            ).nonzero()[0]
            array[pure_ghost_pos] = 0
            # same for slaves
            slave_pos = np.asarray(node_flags == np.uint8(aka._slave)).nonzero()[0]
            array[slave_pos] = 0

    def interpolate_pressure_on_qpoints(self, p_in):
        """Interpolates pressure field p_in on quadrature points and stores it in the temperature_on_qpoints array.

        Args:
            p_in (ndarray): Nodal pressure field to be interpolated.
        """

        p = self.flow_model.getTemperature()
        p_backup = p.copy()
        np.copyto(p, p_in)
        self.flow_model.computeTempOnQpoints(aka._not_ghost)

        # roll back the initial values
        np.copyto(p, p_backup)

    def compute_gradu_on_qpoints(self, u, el_type):
        """Computes gradient of u, stores it in gradU internal field, and synchronizes it.

        Args:
            u (ndarray): Displacement field.
            el_type (aka.ElementType): Type of elements on which gradU is computed.
        """

        fem = self.rock_model.getFEEngine()

        # compute gradu within each material for specified el_type
        for mat_id in range(self.rock_model.getNbMaterials()):
            mat = self.rock_model.getMaterial(mat_id)
            elem_filter = mat.getElementFilter(el_type, aka._not_ghost)
            if len(elem_filter) == 0:
                continue
            grad_u = mat.getGradU(el_type, aka._not_ghost)
            fem.gradientOnIntegrationPoints(
                u,
                grad_u,
                self.rock_model.getSpatialDimension(),
                el_type,
                aka._not_ghost,
                elem_filter,
            )

        # synchronize grad_u field between partitions
        self.rock_model.synchronizeField(aka.smm_gradu)

    def assemble_gradu_global(self, grad_u_global, el_type, ghost_type):
        """Assembles grad_u of each material into a global grad_u.

        Args:
            grad_u_global (ndarray): Global gradU array.
            el_type (aka.ElementType): Type of elements on which gradU is computed.
            ghost_type (aka.GhostType): Ghost type of elements.
        """

        dim = self.rock_model.getSpatialDimension()
        nb_elements = self.rock_model.getMesh().getNbElement(el_type, ghost_type)

        if nb_elements == 0:
            return

        fem = self.rock_model.getFEEngine()
        nb_quad_points = fem.getNbIntegrationPoints(el_type)
        assert grad_u_global.shape == (
            nb_elements * nb_quad_points,
            dim * dim,
        ), "Provided grad_u has a wrong shape"

        # assemble grad_u of each material into a global grad_u
        for mat_id in range(self.rock_model.getNbMaterials()):
            mat = self.rock_model.getMaterial(mat_id)
            elem_filter = np.squeeze(mat.getElementFilter(el_type, ghost_type))
            if len(elem_filter) == 0:
                continue
            grad_u = mat.getGradU(el_type, ghost_type)
            global_ips = np.zeros(len(elem_filter) * nb_quad_points, dtype=int)
            for i in range(nb_quad_points):
                global_ips[i::nb_quad_points] = elem_filter * nb_quad_points + i
            mask = np.full(grad_u_global.shape, False)
            mask[global_ips] = True
            np.copyto(grad_u_global, grad_u, where=mask)
