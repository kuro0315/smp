import numpy as np

from IComponent import IComponent

class IAttitude(IComponent):
    def GetPlusX(self) -> np.ndarray:
        raise NotImplementedError()
    
    def GetMinusX(self)-> np.ndarray:
        raise NotImplementedError()
    
    def GetPlusY(self) -> np.ndarray:
        raise NotImplementedError()
    
    def GetMinusY(self)-> np.ndarray:
        raise NotImplementedError()
    
    def GetPlusZ(self) -> np.ndarray:
        raise NotImplementedError()
    
    def GetMinusZ(self) -> np.ndarray:
        raise NotImplementedError()