from orbit import Orbit
from skyfield_orbit import SkyfieldOrbit
from attitude import Attitude

from IAttitude import IAttitude
from IOrbit import IOrbit

from typing import Tuple

def CreateOrbitAttitude(pattern : str) -> Tuple[IOrbit, IAttitude]:
    if pattern == "simple":
        orb = Orbit()
        return orb, Attitude(orb)
    elif pattern == "skyfield":
        orb = SkyfieldOrbit()
        return orb, Attitude(orb)
    else:
        raise NotImplementedError
    