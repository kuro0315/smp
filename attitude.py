from injector import inject
import numpy as np
from i_orbit import IOrbit
from i_attitude import IAttitude
from i_component import IComponent

class Attitude(IAttitude, IComponent):
    @inject
    def __init__(self, orbit : IOrbit) -> None:
        self.__SetAttitude(
            GetPlusX = orbit.GetSatVel,
            GetPlusZ= lambda: -orbit.GetSatPos()
        )
        
    def step(self, dt) -> None:
        self.__plus_x = self.__CalcPlusX()
        self.__plus_z = self.__CalcPlusZ()
        
        self.__plus_x /= np.linalg.norm(self.__plus_x)
        self.__plus_z /= np.linalg.norm(self.__plus_z)
        
        self.__plus_y = np.cross(self.__plus_x, self.__plus_z)
        
    def __SetAttitude(self, GetPlusX, GetPlusZ) -> None:
        """軸の設定

        Args:
            GetPlusX (Callable): +X軸の方向を返す関数
            GetPlusZ (Callable): +Z軸の方向を返す関数
        """
        self.__CalcPlusX = GetPlusX
        self.__CalcPlusZ = GetPlusZ
    
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