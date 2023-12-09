from injector import inject
import numpy as np
from i_orbit import IOrbit
from i_attitude import IAttitude
from i_component import IComponent

class Attitude(IAttitude, IComponent):
    @inject
    def __init__(self, orbit : IOrbit) -> None:
        self.__orbit = orbit
        
    def step(self, dt) -> None:
        self.__plus_x = self.__orbit.GetSatVel()
        self.__plus_z = - self.__orbit.GetSatPos()
        
        self.__plus_x /= np.linalg.norm(self.__plus_x)
        self.__plus_z /= np.linalg.norm(self.__plus_z)
        
        self.__plus_y = np.cross(self.__plus_x, self.__plus_z)
    
    def GetPlusX(self) -> np.ndarray:
        return self.__plus_x
    
    def GetMinusX(self):
        return -self.GetPlusX()
    
    def GetPlusY(self) -> np.ndarray:
        return self.__plus_y
    
    def GetMinusY(self):
        return -self.GetPlusY()
    
    def GetPlusZ(self) -> np.ndarray:
        return self.__plus_z
    
    def GetMinusZ(self):
        return -self.GetPlusZ()