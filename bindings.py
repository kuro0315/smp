import injector
from IOrbit import IOrbit
from IAttitude import IAttitude

from orbit import Orbit
from attitude import Attitude

def calculator_binding(binder):
    binder.bind(IOrbit, to=Orbit, scope=injector.singleton)
    binder.bind(IAttitude, to=Attitude, scope=injector.singleton)
