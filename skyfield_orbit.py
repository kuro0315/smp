import numpy as np
from i_orbit import IOrbit
from i_component import IComponent

from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta, timezone


def normalize_print_decorator(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        a = func(*args, **kwargs)
        print(np.linalg.norm(a))
        return a
    return wrapper

line1 = '1 47930U 98067SG  21078.66151466  .00007199  00000-0  13516-3 0  9991'
line2 = '2 47930  51.6433  65.4945 0003366  59.8640 300.2682 15.49748776   841'

class SkyfieldOrbit(IOrbit, IComponent):
    def __init__ (self) -> None:
        self.__ts = load.timescale()
        self.__planets = load('de421.bsp')
        self.__earth = self.__planets['earth']
        self.__sun = self.__planets['sun']

        # 作ったときの時間
        tle_time = self.__line2tletime(line1,line2)
        self.__t = self.__ts.utc(tle_time)
        
        self.__sat = EarthSatellite(line1, line2)
        
        self.__pos = None
        # print(np.degrees(self.calc_beta_angle()))
    
    def step(self, dt) -> None:
        # dt秒ごとの位置を計算
        self.__t = self.__ts.utc(self.__t.utc_datetime() + timedelta(seconds=dt))
        self.pos_sat = self.__sat.at(self.__t)
        
    def GetSunVec(self) -> np.ndarray:
        t = self.__t
        earth = self.__earth
        apparent = earth.at(t).observe(self.__sun).apparent()
        _vec = np.array(apparent.position.km)
        return _vec / np.linalg.norm(_vec)
    
    def GetSatPos(self)-> np.ndarray:
        return np.array(self.pos_sat.position.km)
    
    def GetSatVel(self) -> np.ndarray:
        return np.array(self.pos_sat.velocity.km_per_s)
    
    def IsSunlit(self) -> bool:
        return self.pos_sat.is_sunlit(self.__planets)
    
    def __line2tletime(self,line1,line2) -> datetime:
        epoch_year = int(line1.split()[3][:2])
        epoch_day = float(line1.split()[3][2:]) 
        tle_time = datetime(2000+(epoch_year), 1, 1,0,0,0, tzinfo=timezone.utc) + timedelta( days = epoch_day) 
        print(tle_time)
        return tle_time
    
    #β角を計算する
    def calc_beta_angle(self):
        position = self.__earth.at(self.__t).observe(self.__sun)
        ra, dec, distance = position.radec()

        #定数の定義
        d = np.radians(dec.degrees) # 赤経
        r = ra.radians # 赤緯
        o0 = self.__sat.model.nodeo # 初昇交点赤経
        i = self.__sat.model.inclo # 軌道傾斜角
        J2 = 0.00108262 # 扁球摂動定数
        Req = 6378.1 # 地球の赤道半径
        m = 398600 # 地球重力定数
        h = 400
        R = Req + h # 半直弦
        # 昇交点赤経oの時間変化 do (rad/s)
        do = - 3/2 * J2 * (Req/R)*(Req/R) * np.sqrt(m/(R*R*R)) * np.cos(i)
        # /dayに変換 (rad/day)
        do = do*60*60*24
        o0 = o0- do*0
        return( 
            np.arcsin( 
                np.cos(d)*np.sin(i)*np.sin((o0) - r) 
                + np.sin(d)*np.cos(i)
            ))