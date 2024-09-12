from surfpack.saft import SAFT
from surfpack.saft_hardsphere import SAFT_WhiteBear
from thermopack.saftvrss import saftvrss
import numpy as np
import warnings
from scipy.constants import Boltzmann

class SAFT_VR_Sigma(SAFT):
    def __init__(self, comps, hs_model=SAFT_WhiteBear, parameter_ref='Default', C=None, lamb=None, sigma=None, eps_div_k=None):
        """Constructor

        Args:
            comps (str) : Component identifiers
            hs_model (SAFT_HardSphere) : Hard-Sphere model
            parameter_ref (str) : ID for parameter set
            C (3d array) : Pure fluid Potential coefficients, organised as C[term][comp 1][comp 2]
            lamb (3d array) : Pure fluid Potential exponents, organised as lamb[term][comp 1][comp 2]
            sigma (2d array) : Pure fluid Size parameters (m)
            eps_div_k (2d array) : Pure fluid Energy parameters (K)
        """
        super().__init__(comps, eos=lambda *args, **kwargs: saftvrss(*args, **kwargs, init_from_db='SAFT-VR-MIE'), hs_model=hs_model, parameter_ref=parameter_ref)
        self.coeff = C
        self.lamb = lamb
        self.sigma = sigma
        self.eps_div_k = eps_div_k
        self.eos = saftvrss(comps, init_from_db='SAFT-VR-MIE')
        for i in range(self.ncomps):
            for j in range(self.ncomps):
                self.eos.set_pair_potential_params(i + 1, j + 1, self.coeff[:, i, j], self.lamb[:, i, j], self.sigma[i][j],
                                                       self.eps_div_k[i][j])


    @staticmethod
    def init_single(sigma, eps_div_k, C, lamb):
        """Constructor

        Args:
            sigma (float) : Size parameter (m)
            eps_div_k (float) : Energy parameter (K)
            C (1d array) : Potential coefficients
            lamb (1d array) : Potential exponents
        """
        return SAFT_VR_Sigma('LJF', C=np.array([[[Ci]] for Ci in C]), lamb=np.array([[[li]] for li in lamb]), sigma=np.array([[sigma]]),
                             eps_div_k=np.array([[eps_div_k]]))

    @staticmethod
    def init_single_reduced(C, lamb):
        """Comstructor

        Args:
            C (1d array) : Potential coefficients
            lamb (1d array) : Potential exponents
        """
        sigma = 3e-10
        eps_div_k = 100
        return SAFT_VR_Sigma.init_single(sigma, eps_div_k, C, lamb)

    def get_characteristic_lengths(self):
        return self.eos.get_pure_fluid_param(1)[1] * 1e10

    def get_caching_id(self):
        """Internal
        Get id that identifies this model. See `Functional` for more information.

        Returns:
            str : Unique id for initialised model.
        """
        ostr = f'SAFT-VR Sigma {self._comps}, Coeffs: {self.coeff}, expo : {self.lamb}\n' \
               + super().get_caching_id()
        return ostr

    def pair_potential(self, i, j, r):
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