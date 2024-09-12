from surfpack.saft import SAFT
from surfpack.saft_hardsphere import SAFT_WhiteBear
from thermopack.saftvrqmie import saftvrqmie
import numpy as np
import warnings
from scipy.constants import Boltzmann
from surfpack.Functional import profilecaching, solve_sequential_rhoT, Profile, Grid, Geometry, picard_rhoT, anderson_rhoT, ExpandedSoft

class SAFT_VRQ_Mie(SAFT):
    def __init__(self, comps, hs_model=SAFT_WhiteBear, parameter_ref='Default', FH_order=None):
        super().__init__(comps, saftvrqmie, hs_model, parameter_ref=parameter_ref)
        self.eos = saftvrqmie(comps, feynman_hibbs_order=FH_order)
        fh_orders = np.array([self.eos.get_feynman_hibbs_order(i + 1) for i in range(self.ncomps)])
        if FH_order is not None:
            if any(fh_orders != FH_order):
                raise ValueError(f"parameter_ref '{parameter_ref}' is for FH orders {fh_orders}, but the FH orders {FH_order} "
                                 f"were specified.")
        self.fh_orders = fh_orders
        self.saved_temperature = None


    def get_characteristic_lengths(self):
        return self.eos.get_pure_fluid_param(1)[1] * 1e10

    def get_fh_orders(self):
        return self.fh_orders

    def get_caching_id(self):
        """Internal
        Get id that identifies this model. See `Functional` for more information.

        Returns:
            str : Unique id for initialised model.
        """
        ostr = f'SAFT-VRQ Mie {self._comps}, FH orders : {self.get_fh_orders()}\n' \
               + super().get_caching_id()
        return ostr

    def pair_potential(self, i, j, r, T):
        """Utility
        Compute the pair potential between species i and j at distance r and temperature T.

        Args:
            i (int) : First component index
            j (int) : Second component index
            r (float) : Seperation disntance (Å)
            T (float) : Temperature (K)
        Returns:
            float : Interaction potential energy (J)
        """
        return Boltzmann * self.eos.potential(i + 1, j + 1, r * 1e-10, T)

    @profilecaching
    def radial_distribution_functions(self, rho_b, T, comp_idx=0, grid=None, rmax=50, solver=None, rdf_0=None):
        """rhoT Property
        Compute the radial distribution functions $g_{i,j}$ for $i =$ `comp_idx` using the "Percus trick". To help convergence:
        First converge the profile for a planar geometry, exposed to an ExtendedSoft potential with a core radius $5R$, where
        $R$ is the maximum `characteristic_length` of the mixture. Then, shift that profile to the left, and use it as
        an initial guess for the spherical case.
        If that doesn't work, the profile can be shifted in several steps (by gradually reducing the core radius of the
        ExtendedSoft potential). The latter possibility is not implemented, but is just a matter of putting the "shift
        and recompute" part of this method in a for-loop, and adding some appropriate kwargs.

        Args:
            rho_b (list[float]) : The bulk densities [particles / Å^3]
            T (float) : Temperature [K]
            comp_idx (int) : The first component in the pair, defaults to the first component
            grid (Grid) : The spatial discretisation (should have Spherical geometry for results to make sense)
            rmax (float) : Maximum range for which to compute the RDF.
            solver (SequentialSolver or GridRefiner) : Optional, The solver to use. A default solver is constructed if
                                                        none is supplied.
            rdf_0 (list[Profile]) : Initial guess for the rdf.
        Returns:
            list[Profile] : The radial distribution functions around a particle of type `comp_idx`
        """

        if grid is None:
            grid = Grid(1000, Geometry.SPHERICAL, rmax)

        solvers = [picard_rhoT, picard_rhoT, anderson_rhoT]
        tolerances = [1e-3, 1e-5, 1e-9]
        solver_kwargs = [{'mixing_alpha': 0.01, 'max_iter': 1000},
                         {'mixing_alpha': 0.05, 'max_iter': 500},
                         {'beta_mix': 0.05, 'max_iter': 500}]

        # First, converge for a planar geometry
        grid_p = Grid(grid.N, Geometry.PLANAR, grid.L)
        Vext = [lambda r: self.pair_potential(comp_idx, i, r, T) for i in range(self.ncomps)]
        if rdf_0 is None: # Generate initial guess and converge profile with planar potential to improve it.
            rho = Profile.from_potential(rho_b, T, grid_p, Vext=Vext)
            sol = solve_sequential_rhoT(self, rho, rho_b, T, solvers=solvers, tolerances=tolerances,
                                        solver_kwargs=solver_kwargs, Vext=Vext, verbose=2)
            if sol.converged is False:
                warnings.warn('Initial computation for planar profile did not converge!', RuntimeWarning, stacklevel=2)
        else:
            rho = [rho_b[i] * rdf_0[i] for i in range(self.ncomps)]

        rho = [Profile(rho[i], grid) for i in range(self.ncomps)]
        Vext = [lambda r: self.pair_potential(comp_idx, i, r, T) for i in range(self.ncomps)]
        sol = solve_sequential_rhoT(self, rho, rho_b, T, solvers=solvers,
                                    tolerances=tolerances, solver_kwargs=solver_kwargs, Vext=Vext, verbose=2)
        if sol.converged is False:
            warnings.warn('Density profile did not converge after maximum number of iterations', RuntimeWarning,
                          stacklevel=2)

        # Divide by bulk densities to get RDF.
        rdf = [Profile(sol.profile[i] / rho_b[i], grid) for i in range(self.ncomps)]
        return rdf