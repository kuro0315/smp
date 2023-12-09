from injector import inject, Injector
from bindings import calculator_binding
import matplotlib.pyplot as plt
import numpy as np

from IOrbit import IOrbit
from IAttitude import IAttitude

class Calculator():
    @inject
    def __init__(self, orb:IOrbit, attitude:IAttitude) -> None:
        self.__orb, self.__attitude = orb, attitude
        self.components = [self.__orb, self.__attitude]
        
    def run(self):
        deltat = 1
        totalt = 90 * 60
        
        # 太陽光と衛星パネルのなす角度の余弦
        cos_sun_panels = []

        for _ in range(totalt):
            
            # 全て更新する
            for component in self.components:
                component.step(deltat)
            
            cos_sun_panels.append(
                np.clip(
                    np.dot(
                        self.__attitude.GetPlusZ(),
                        self.__orb.GetSunVec()
                    ), 0, 1
                ) * self.__orb.IsSunlit()
            )

        plt.plot(cos_sun_panels)
        plt.xlim(0, totalt)
        plt.ylim(0, 1)
        plt.xlabel("Time [s]")
        plt.ylabel("cos(θ)")
        plt.savefig("cos.png")

if __name__ == "__main__":
    inj = Injector([calculator_binding])
    calc = inj.get(Calculator)
    calc.run()