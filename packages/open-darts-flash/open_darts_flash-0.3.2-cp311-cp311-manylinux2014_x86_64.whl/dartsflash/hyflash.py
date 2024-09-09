import numpy as np

from dartsflash.pyflash import PyFlash
from dartsflash.libflash import VdWP


class HyFlash(PyFlash):
    hydrate_eos: dict = {}

    def add_hydrate_eos(self, name: str, eos: VdWP):
        """
        Method to add hydrate EoS to map
        """
        self.hydrate_eos[name] = eos

    def calc_df(self, pressure, temperature, composition, phase: str = "sI"):
        """
        Method to calculate fugacity difference between fluid mixture and hydrate phase

        :param pressure: Pressure [bar]
        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param phase: Hydrate phase type
        """
        self.f.evaluate(pressure, temperature, composition)
        flash_results = self.f.get_flash_results()
        V = np.array(flash_results.nu)
        x = np.array(flash_results.X).reshape(len(V), self.ns)
        f0 = self.flash_params.eos_params["AQ"].eos.fugacity(pressure, temperature, x[0, :])

        fwH = self.hydrate_eos[phase].fw(pressure, temperature, f0)
        df = fwH - f0[self.H2O_idx]
        return df

    def calc_equilibrium_pressure(self, temperature: float, composition: list, p_init: float, phase: str = "sI",
                                  max_it: int = 100, dp: float = 10., min_p: float = 1., max_p: float = None):
        """
        Method to calculate equilibrium pressure between fluid phases and hydrate phase at given T, z

        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param p_init: Initial guess for equilibrium pressure [bar]
        :param phase: Hydrate phase type
        :param max_it: Maximum number of iterations of bisection method
        :param dp: Step size to find pressure bounds
        :param min_p: Minimum pressure [bar]
        :param max_p: Maximum pressure [bar]
        """
        # Find bounds for pressure
        p_min, p_max = p_init, p_init
        if self.calc_df(p_init, temperature, composition, phase) > 0:
            # Hydrate fugacity larger than fluid fugacity
            while True:
                p_max += dp
                if self.calc_df(p_max, temperature, composition, phase) < 0:
                    break
                p_min += dp
        else:
            # Hydrate fugacity smaller than fluid fugacity
            while True:
                p_min = max(min_p, p_min-dp)
                if self.calc_df(p_min, temperature, composition, phase) > 0:
                    break
                p_max = max(min_p, p_max-dp)

        for it in range(1, max_it+1):
            pressure = (p_min + p_max) / 2
            df = self.calc_df(pressure, temperature, composition, phase)

            if np.abs(df) < 1e-10:
                return pressure
            else:
                if df > 0:
                    p_min = pressure
                else:
                    p_max = pressure
        print("Not converged", temperature)
        return None

    def calc_equilibrium_temperature(self, pressure: float, composition: list, t_init: float, phase: str = "sI",
                                     max_it: int = 100, dT: float = 10., min_t: float = 273.15, max_t: float = 373.15):
        """
        Method to calculate equilibrium temperature between fluid phases and hydrate phase at given P, z

        :param pressure: Pressure [bar]
        :param composition: Feed mole fractions [-]
        :param t_init: Initial guess for equilibrium temperature [K]
        :param phase: Hydrate phase type
        :param max_it: Maximum number of iterations of bisection method
        :param dT: Step size to find pressure bounds
        :param min_t: Minimum temperature [K]
        :param max_t: Maximum temperature [K]
        """
        # Find bounds for temperature
        T_min, T_max = t_init, t_init
        if self.calc_df(pressure, t_init, composition, phase) < 0:
            while True:
                T_max += dT
                if self.calc_df(pressure, T_max, composition) > 0:
                    break
                T_min += dT
        else:
            while True:
                T_min -= dT
                if self.calc_df(pressure, T_min, composition, phase) < 0:
                    break
                T_max -= dT

        for it in range(1, max_it+1):
            temperature = (T_min + T_max) / 2

            df = self.calc_df(pressure, temperature, composition, phase)

            if np.abs(df) < 1e-10:
                return temperature
            else:
                if df < 0:
                    T_min = temperature
                else:
                    T_max = temperature
        print("Not converged", pressure)
        return None

    def calc_equilibrium_curve(self, composition: list, ref_data: list, pressure: list = None, temperature: list = None,
                               phase: str = "sI", max_it: int = 100, dX: float = 10.):
        """
        Method to calculate equilibrium pressure/temperature between fluid phases and hydrate phase at given P/T, z

        :param composition: Feed mole fractions [-]
        :param ref_data: Reference data to be used as initial guess for equilibrium P/T
        :param pressure: Pressure [bar]
        :param temperature: Temperature [K]
        :param phase: Hydrate phase type
        :param max_it: Maximum number of iterations of bisection method
        :param dX: Step size to find P/T bounds
        """
        assert not ((pressure is None) == (temperature is None)), "Specify either range of pressures or temperatures"

        # Calculate pressure for each temperature
        if pressure is None:
            len_data = len(temperature)
            pressure = np.zeros(len_data)
            for ith_temp, t in enumerate(temperature):
                pressure[ith_temp] = self.calc_equilibrium_pressure(t, composition, ref_data[ith_temp],
                                                                    phase, max_it, dp=dX)
        # Else, calculate temperature for each pressure
        elif temperature is None:
            len_data = len(pressure)
            temperature = np.zeros(len_data)
            for ith_pres, p in enumerate(pressure):
                temperature[ith_pres] = self.calc_equilibrium_temperature(p, composition, ref_data[ith_pres],
                                                                          phase, max_it, dT=dX)
        return pressure, temperature

    def calc_properties(self, pressure: list, temperature: list, composition: list, guest_idx: list,
                        number_of_curves: int = 1, phase: str = "sI"):
        """
        Method to calculate hydrate phase properties at given P,T,z:
        - Hydration number nH [-]
        - Density rhoH [kg/m3]
        - Enthalpy of hydrate formation/dissociation dH [kJ/kmol]

        :param pressure: Pressure [bar]
        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param guest_idx: Index of guest molecule(s)
        :param phase: Hydrate phase type
        :param number_of_curves: Number of equilibrium curves
        """
        from darts.physics.properties.eos_properties import EoSEnthalpy, VdWPDensity, VdWPEnthalpy
        densH = VdWPDensity(self.hydrate_eos[phase], self.mixture.comp_data.Mw)
        enthH = VdWPEnthalpy(self.hydrate_eos[phase])
        enthV = EoSEnthalpy(self.flash_params.eos_params["SRK"].eos)
        enthA = EoSEnthalpy(self.flash_params.eos_params["AQ"].eos)

        pressure = np.tile(pressure, (number_of_curves, 1)) if not isinstance(pressure[0], (list, np.ndarray)) else pressure
        temperature = np.tile(temperature, (number_of_curves, 1)) if not isinstance(temperature[0], (list, np.ndarray)) else temperature
        nH = [[] for i in range(number_of_curves)]
        rhoH = [[] for i in range(number_of_curves)]
        dH = [[] for i in range(number_of_curves)]

        for i in range(number_of_curves):
            len_data = len(pressure[i])
            assert len(temperature[i]) == len_data

            nH[i] = [None] * len_data
            rhoH[i] = [None] * len_data
            dH[i] = [None] * len_data

            for j in range(len_data):
                if not pressure[i][j] is None or not temperature[i][j] is None:
                    self.calc_df(pressure[i][j], temperature[i][j], composition[i])
                    flash_results = self.f.get_flash_results()
                    V = np.array(flash_results.nu)
                    x = np.array(flash_results.X).reshape(len(V), self.ns)
                    xH = self.hydrate_eos[phase].xH()

                    # Calculate hydration number nH
                    nH[i][j] = 1. / xH[guest_idx] - 1.

                    # Density rhoH
                    rhoH[i][j] = densH.evaluate(pressure[i][j], temperature[i][j], xH)

                    # Enthalpy of hydrate formation/dissociation
                    Hv = enthV.evaluate(pressure[i][j], temperature[i][j], x[1, :])
                    Ha = nH[i][j] * enthA.evaluate(pressure[i][j], temperature[i][j], x[0, :])
                    Hh = enthH.evaluate(pressure[i][j], temperature[i][j], xH) * (nH[i][j] + 1)
                    dH[i][j] = (Hv + Ha - Hh) * 1e-3  # H_hyd < H_fluids -> enthalpy release upon formation

        return nH, rhoH, dH
