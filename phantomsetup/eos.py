# The type ignore comments are due to the following bug:
# https://github.com/python/mypy/issues/4975

from typing import Any, Dict

from . import defaults

ieos_label = {
    1: 'isothermal',
    2: 'adiabatic/polytropic',
    3: 'locally isothermal disc',
    6: 'locally isothermal disc centered on sink particle',
    7: 'z-dependent locally isothermal eos',
    8: 'barotropic',
    9: 'piecewise polytrope',
    10: 'MESA',
    11: 'isothermal with zero pressure',
    14: 'locally isothermal binary disc',
}

ieos_has = {
    'polyk': (1, 2, 3, 6, 7, 8, 9, 10, 11, 14),
    'gamma': (2, 8, 9),
    'qfacdisc': (3, 6, 7, 14),
}

ieos_isothermal = {1, 3, 6, 7, 11, 14}


class EquationOfState:
    """
    Equation of state for gas.

    Parameters
    ----------
    ieos : int
        The equation of state as represented by the following integers:
            1: 'isothermal'
            2: 'adiabatic/polytropic'
            3: 'locally isothermal disc'
            6: 'locally isothermal disc centered on sink particle'
            7: 'z-dependent locally isothermal eos'
            8: 'barotropic'
            9: 'piecewise polytrope'
            10: 'MESA'
            11: 'isothermal with zero pressure'
            14: 'locally isothermal binary disc'
    """

    def __init__(self, ieos: int = None, **kwargs) -> None:

        if ieos is None:
            ieos = 1
        if ieos not in ieos_label:
            raise ValueError(f'ieos={ieos} does not exist')
        if ieos > 3:
            raise NotImplementedError('ieos > 3 not available currently')

        self.ieos = ieos

        self._parameters: Dict[str, Any] = {
            key: None for key in ('polyk', 'gamma', 'qfacdisc')
        }

        for parameter in self._parameters.keys():
            if ieos in ieos_has[parameter]:  # type: ignore
                if parameter == 'polyk':
                    self._parameters[parameter] = 2 / 3 * defaults.header['RK2']
                else:
                    self._parameters[parameter] = defaults.header[parameter]

        for parameter in self._parameters:
            if parameter in kwargs:
                if ieos not in ieos_has[parameter]:  # type: ignore
                    raise ValueError(f'Cannot set {parameter} for ieos={ieos}')
                else:
                    self._parameters[parameter] = kwargs[parameter]

    @property
    def polyk(self) -> float:
        """
        'polyk' is a constant of proportionality in the eos.

        Isothermal eos: polyk = (sound speed)^2.
        Adiabatic/polytropic eos: polyk = pressure / rho^(gamma).
        """
        return self._parameters['polyk']

    @polyk.setter
    def polyk(self, value: float) -> None:
        if self.ieos is None:
            raise ValueError('set ieos first')
        self._polyk = value

    @property
    def gamma(self) -> float:
        """
        'gamma' is the adiabatic index.
        """
        return self._parameters['gamma']

    @gamma.setter
    def gamma(self, value: float) -> None:
        if self.ieos not in ieos_has['gamma']:  # type: ignore
            raise ValueError(f'ieos={self.ieos} not compatible with setting gamma')
        self._gamma = value

    @property
    def qfacdisc(self) -> float:
        """
        'qfacdisc' is the 'q' exponent of locally isothermal disc.

        Sound speed is proportional to radius^(-q).
        """
        return self._parameters['qfacdisc']

    @qfacdisc.setter
    def qfacdisc(self, value: float) -> None:
        if self.ieos not in ieos_has['qfacdisc']:  # type: ignore
            raise ValueError(f'ieos={self.ieos} not compatible with setting qfacdisc')
        self._qfacdisc = value