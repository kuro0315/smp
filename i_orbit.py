import numpy as np

from i_component import IComponent

class IOrbit(IComponent):
    def GetSunVec(self) -> np.ndarray:
        raise NotImplementedError()

    def GetSatPos(self)-> np.ndarray: 
        raise NotImplementedError()
    
    def GetSatVel(self) -> np.ndarray:
        raise NotImplementedError()
    
    def IsSunlit(self) -> bool:
        raise NotImplementedError()
    