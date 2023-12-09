import numpy as np
from i_orbit import IOrbit
from i_component import IComponent

class Orbit(IOrbit, IComponent):
    Re = 6378.137 # km
    def __init__ (self) -> None:
        """軌道のクラス

        Args:
            beta (float): β角度[radian]
            h (float): 高度[km]
        """
        self.beta = np.radians(45.51)
        self.h = 348.723 # km
        self.theta = np.radians(0)
        
        # 人工衛星の速度[km/s]
        self.vel = np.sqrt(398600.4418 / (self.Re + self.h))
        self.omega = self.vel / (self.Re + self.h)
        
        self.theta_star = np.arcsin(
        np.sqrt(
                1/(np.cos(self.beta)**2) * (
                    (self.Re / (self.Re + self.h))**2 - np.sin(self.beta)**2
                )
            )
        )
        
        # self_theta_statがπ/2より大きく,πより小さいため,πから引く
        self.theta_star = np.pi - self.theta_star
        
    def step(self, dt) -> None:
        self.theta += self.omega * dt
        
    def GetSunVec(self) -> np.ndarray:
        return np.array([1, 0, 0])

    def GetSatPos(self)-> np.ndarray: 
        r_sat = (self.Re + self.h) * np.array(
            [
                np.cos(self.theta) * np.cos(self.beta), 
                np.sin(self.theta),
                np.cos(self.theta) * np.sin(self.beta)
            ]
        )
        return r_sat
    
    def GetSatVel(self) -> np.ndarray:
        v_sat = (self.Re + self.h) * np.array(
            [
                -np.sin(self.theta) * np.cos(self.beta),
                np.cos(self.theta),
                -np.sin(self.theta) * np.sin(self.beta)
            ]
        )
        return v_sat
    
    def IsSunlit(self) -> bool:
        is_sunlit = self.theta < self.theta_star or (2 * np.pi - self.theta_star) < self.theta
        return is_sunlit