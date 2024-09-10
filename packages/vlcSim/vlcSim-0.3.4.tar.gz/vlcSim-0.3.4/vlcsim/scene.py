"""
It manages the physical sustrate. 
"""

import numpy as np
import math as m
from enum import Enum
import warnings


class AccessPoint:
    """
    Class representing a generic access point. The :class:`vlcsim.scene.AccessPoint` class is in charge of managing the physical sustrate. It has the following attributes:

    - **x**: **x** coordinate of the position of this VLed.
    - **y**: **y** coordinate of the position of this VLed.
    - **z**: **z** coordinate of the position of this VLed.
    - **state**: Current state of the access point. Could be IDLE or BUSY.
    - **sliceTime**: Time of the slice in [s]
    """

    stateap = Enum("state", "IDLE BUSY")

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
    ) -> None:
        """
        VLed constructor

        :param x: **x** coordinate of the position of this VLed.
        :type x: float
        :param y: **y** coordinate of the position of this VLed.
        :type y: float
        :param z: **z** coordinate of the position of this VLed.
        :type z: float
        :param nLedsX: Number of rows in the led.
        :type nLedsX: int
        :param nLedsY: Number of cols in the led.
        :type nLedsY: int
        :param ledPower: Power of the led in [mW]
        :type ledPower: float
        :param theta: semi-angle median ilumination (degrees)
        :type theta: float
        """
        self._x = x
        self._y = y
        self._z = z
        self._state = AccessPoint.stateap.IDLE
        self._sliceTime = None
        self._slicesInFrame = None

        self._ID = None
        self._position = np.array([x, y, z])
        self._B = None

    @property
    def B(self) -> float:
        """
        Gets the Bandwith of this AccessPoint

        :return: The B of this AccessPoint
        :rtype: float
        """
        return self._B

    @B.setter
    def B(self, value: float):
        self._B = value

    @property
    def ID(self) -> int:
        """
        Identification of VLed

        :return: VLed ID.
        :rtype: int
        """
        return self._ID

    @ID.setter
    def ID(self, value: int):
        self._ID = value

    @property
    def x(self) -> float:
        """
        x Coordinate of this VLed

        :return: x coordinate
        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value
        self._position = np.array([self._x, self.y, self.z])

    @property
    def y(self) -> float:
        """
        y Coordinate of this VLed

        :return: y coordinate.
        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value
        self._position = np.array([self.x, self._y, self.z])

    @property
    def z(self) -> float:
        """
        z Coordinate of this VLed

        :return: z coordinate
        :rtype: float
        """
        return self._z

    @z.setter
    def z(self, value: float):
        self._z = value
        self._position = np.array([self.x, self.y, self._z])

    @property
    def position(self) -> np.ndarray:
        """
        The coordinates of the position of this VLed

        :return: Coordinates of the position
        :rtype: np.array
        """
        return self._position

    @property
    def state(self) -> stateap:
        """
        VLed state

        :return: This access point state. Could be IDLE or BUSY.
        :rtype: :class:`vlcsim.scene.AccessPoint.stateap`
        """
        return self._state

    def setIDLE(self):
        """
        Set the state of this access point to IDLE
        """
        self._state = AccessPoint.stateap.IDLE

    def setBUSY(self):
        """
        Set the state of this VLed to BUSY
        """
        self.__state = AccessPoint.stateap.BUSY

    @property
    def sliceTime(self) -> float:
        """
        The slice time correspond to the time that a connection will be using this VLed.

        :return: Slice time
        :rtype: float
        """
        return self._sliceTime

    @sliceTime.setter
    def sliceTime(self, value: float):
        self._sliceTime = value

    @property
    def slicesInFrame(self) -> int:
        """
        The number of slices in the frame. This is used to determine how many slices will be in the frame.

        :return: The number of slices in the frame
        :rtype: int
        """
        return self._slicesInFrame

    @slicesInFrame.setter
    def slicesInFrame(self, value: int):
        self._slicesInFrame = value


class VLed(AccessPoint):
    """
    Class that represents Visual Lights Leds.
    """

    numberOfVLeds = 0
    """
    number of VLeds created
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        nLedsX: int,
        nLedsY: int,
        ledPower: float,
        theta: float,
    ) -> None:
        """
        VLed constructor

        :param x: **x** coordinate of the position of this VLed.
        :type x: float
        :param y: **y** coordinate of the position of this VLed.
        :type y: float
        :param z: **z** coordinate of the position of this VLed.
        :type z: float
        :param nLedsX: Number of rows in the led.
        :type nLedsX: int
        :param nLedsY: Number of cols in the led.
        :type nLedsY: int
        :param ledPower: Power of the led in [mW]
        :type ledPower: float
        :param theta: semi-angle median ilumination (degrees)
        :type theta: float
        """
        AccessPoint.__init__(self, x, y, z)
        self.__nLedsX = nLedsX
        self.__nLedsY = nLedsY
        self.__ledPower = ledPower
        self.__theta = theta
        self._state = AccessPoint.stateap.IDLE

        self.__numberOfLeds = self.__nLedsX * self.__nLedsY
        self.__totalPower = self.__numberOfLeds * self.__ledPower
        self.__ml = -m.log10(2) / m.log10(m.cos(m.radians(theta)))

        self._ID = VLed.numberOfVLeds
        VLed.numberOfVLeds += 1
        self._position = np.array([x, y, z])

    @property
    def nLedsX(self) -> int:
        """
        Number of leds in each row.

        :return: leds on each row
        :rtype: int
        """
        return self.__nLedsX

    @nLedsX.setter
    def nLedsX(self, value: int):
        self.__nLedsX = value

    @property
    def nLedsY(self) -> int:
        """
        Number of leds in each col.

        :return: leds on each col
        :rtype: int
        """
        return self.__nLedsY

    @nLedsY.setter
    def nLedsY(self, value: int):
        self.__nLedsY = value

    @property
    def ledPower(self) -> float:
        """
        Power of each lead in [mW]

        :return: power in [mW]
        :rtype: float
        """
        return self.__ledPower

    @ledPower.setter
    def ledPower(self, value: float):
        self.__ledPower = value

    @property
    def theta(self) -> float:
        """
        semi-angle median ilumination (degrees)

        :return: angle in degrees
        :rtype: float
        """
        return self.__theta

    @theta.setter
    def theta(self, value: float):
        self.__theta = value

    @property
    def numberOfLeds(self) -> int:
        """
        Number of leds in this VLed

        :return: number of leds
        :rtype: int
        """
        return self.__numberOfLeds

    @property
    def totalPower(self) -> float:
        """
        The Power of this VLed in [mW]. Corresponds to the multiplication of the number of cols in leds with the number of rows and the power of each led.

        :return: total power in [mW]
        :rtype: float
        """
        return self.__totalPower

    @totalPower.setter
    def totalPower(self, value: float):
        self.__totalPower = value

    @property
    def ml(self) -> float:
        """
        Lambertian emission order is given by:

        .. math::
            \\begin{eqnarray}
                ml = -\\frac{\\log_{10} 2}{\\log_{10} (\\cos(\\theta))}
            \\end{eqnarray}

        :return: Lambertian emission order
        :rtype: float
        """
        return self.__ml


class RF(AccessPoint):
    """
    Class that represents a RF object
    """

    numberOfRFs = 0
    """
    Number of RFs created
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        bf: float = 5e6,
        pf: float = 40,
        BERf: float = 10e-5,
        Af: float = 10.0,
        Ef: float = 1.0,
        R_awgn: float = 1 * 10 ** (-174 / 10),
        N_rf: int = 10,
        nFactor_rf: float = 1.0,
        A: float = 0.1e6,
    ) -> None:
        AccessPoint.__init__(self, x, y, z)
        self.__bf = bf
        self.__pf = pf
        self.__BERf = BERf
        self.__Af = Af
        self.__Ef = Ef
        self.__R_awgn = R_awgn
        self.__N_rf = N_rf
        self.__nFactor_rf = nFactor_rf
        self.__A = A
        self._state = AccessPoint.stateap.IDLE

        self.__pif = -1.5 / m.log(5 * self.__BERf)
        self._ID = RF.numberOfRFs
        RF.numberOfRFs += 1

    @property
    def bf(self) -> float:
        """
        femtocell bandwidth

        :return: Value of BF property
        :rtype: float
        """
        return self.__bf

    @bf.setter
    def bf(self, value: float):
        self.__bf = value

    @property
    def pf(self) -> float:
        """
        Femtobase power transmission

        :return: Femtobase power transmission
        :rtype: float

        """
        return self.__pf

    @pf.setter
    def pf(self, value: float):
        self.__pf = value

    @property
    def BERf(self) -> float:
        """
        BER desired in femto network

        :return: BER
        :rtype: float
        """
        return self.__BERf

    @BERf.setter
    def BERf(self, value: float):
        self.__BERf = value

    @property
    def Af(self) -> float:
        """
        Pathloss constant

        :return: Pathloss constant
        :rtype: float
        """
        return self.__Af

    @Af.setter
    def Af(self, value: float):
        self.__Af = value

    @property
    def Ef(self) -> float:
        """
        Pathloss exponent

        :return: Pathloss exponent
        :rtype: float
        """
        return self.__Ef

    @Ef.setter
    def Ef(self, value: float):
        self.__Ef = value

    @property
    def R_awgn(self) -> float:
        """
        Normalized AWGN noise power

        :return: Normalized AWGN noise power
        :rtype: float
        """
        return self.__R_awgn

    @R_awgn.setter
    def R_awgn(self, value: float):
        self.__R_awgn = value

    @property
    def pif(self) -> float:
        """
        The received SNR discrepancy from the continuous input memoryless channel’s capacity at the target BER. (pif=-1.5log2-1(5 BERf))

        .. math::
            \\begin{eqnarray}
                pif = -1.5 \log_2^{-1}(5\cdot BERf)
            \\end{eqnarray}

        :return: SNR discrepancy
        :rtype: float
        """
        return self.__pif

    @pif.setter
    def pif(self, value: float):
        self.__pif = value

    @property
    def N_rf(self) -> int:
        """
        Number of cells using this femtocell

        :return: Number of cells using this femtocell
        :rtype: int
        """
        return self.__N_rf

    @N_rf.setter
    def N_rf(self, value: int):
        self.__N_rf = value

    @property
    def nFactor_rf(self) -> float:
        """
        RF constant

        :return: RF constant
        :rtype: float
        """
        return self.__nFactor_rf

    @nFactor_rf.setter
    def nFactor_rf(self, value: int):
        self.__nFactor_rf = value

    @property
    def A(self) -> float:
        """
        Rayleigh distributed channel gain.

        :return: Rayleigh distributed channel gain.
        :rtype: float
        """
        return self.__A

    @A.setter
    def A(self, value: float):
        self.__A = value


class Receiver:
    """
    Class that represents a VLC object
    """

    receiversCreated = 0
    """
    Number of receivers created by this class.
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        aDet: float,
        ts: float,
        index: float,
        fov: float,
        q: float = 1.6e-19,
        s: float = 0.54,
        b: float = 10e6,
        ibg: float = 5.1e-3,
        cb: float = 1.380649e-23,
        tk: float = 298.0,
        a: float = 1.0,
        gv: float = 10.0,
        n: float = 1.12e-6,
        fr: float = 1.5,
        gm: float = 3e-2,
        i1: float = 0.562,
        i2: float = 0.0868,
    ) -> None:
        """
        Initializes the object with the values. This is the constructor for the Schrodinger model

        :param x: x coordinate of the object
        :type x: float
        :param y: y coordinate of the object's coordinate.
        :type y: float
        :param z: z coordinate of the object's coordinate.
        :type z: float
        :param aDet: aDet value of the object's coordinate.
        :type aDet: float
        :param ts: time of the object's coordinate. Default is 10 seconds.
        :type ts: float
        :param index: order of Lambertian emission that depends on the half-angle at half illumination of the LED.
        :type index: float
        :param fov: width of the field of view.
        :type fov: float
        :param q: electronic load. Default is -1.602e-19 culombios
        :type q: float
        :param s: ibg b - parameter of the Ib - Galactic model. Default is 5 seconds.
        :type s: float
        :param b: c b - parameter of the Ib - Galactic model. Default is 5 seconds.
        :type b: float
        :param ibg: background current. Default is 5.1e-3 Amperes.
        :type ibg: float
        :param cb: Boltzmann constant. Default is 1.380649e-23 J/K.
        :type cb: float
        :param tk: 380649
        :type tk: float
        :param a: n n - prameter of the B - parameter. Default is 10 seconds.
        :type a: float
        :param gv: Open-loop voltage gain. Default is 10
        :type gv: float
        :param n: Fixed capacitance of the PD per unit area. Default is 1.12e-6.
        :type n: float
        :param fr: FET channel noise factor. Default is 1.5
        :type fr: float
        :param gm: FET transconductance. Default is 3e-2.
        :type gm: float
        :param i1: constant experimental value. Default is 0.562.
        :type i1: float
        :param i2: constant experimental value. Default is 0.0868.
        :type i2: float
        """
        self.__x = x
        self.__y = y
        self.__z = z
        self.__aDet = aDet
        self.__ts = ts
        self.__index = index
        self.__fov = fov
        self.__q = q
        self.__s = s
        self.__b = b
        self.__ibg = ibg
        self.__cb = cb
        self.__tk = tk
        self.__a = a
        self.__gv = gv
        self.__n = n
        self.__fr = fr
        self.__gm = gm
        self.__i1 = i1
        self.__i2 = i2

        self.__timeFirstConnected = None
        self.__goalTime = None
        self.__timeActive = 0
        self.__timeFinished = None
        self.__capacityFromAP = None

        self.__gCon = (index**2) / (m.sin(m.radians(fov)) ** 2)
        self.__position = np.array([x, y, z])
        self.__ID = Receiver.receiversCreated
        Receiver.receiversCreated += 1

    @property
    def capacityFromAP(self):
        """
        Get the capacity from AP.

        :return: capacity from AP
        :rtype: float
        """
        return self.__capacityFromAP

    @capacityFromAP.setter
    def capacityFromAP(self, value):
        self.__capacityFromAP = value

    @property
    def ID(self) -> int:
        """
        Return the ID of the object. This is used to distinguish between different objects that are part of the same object group.

        :return: The ID of the object
        :rtype: int
        """
        return self.__ID

    @ID.setter
    def ID(self, value: int):
        self.__ID = value

    @property
    def x(self) -> float:
        """
        Get the x coordinate.

        :return: The x coordinate
        :rtype: float
        """
        return self.__x

    @x.setter
    def x(self, value: float):
        self.__x = value

    @property
    def y(self) -> float:
        """
        Gets the y coordinate .

        :return: The y coordinate
        :rtype: float
        """
        return self.__y

    @y.setter
    def y(self, value: float):
        self.__y = value

    @property
    def z(self) -> float:
        """
        Z coordinate .

        :return: the z coordinate
        :rtype: float
        """
        return self.__z

    @z.setter
    def z(self, value: float):
        self.__z = value

    @property
    def aDet(self) -> float:
        """
        aDet value of the object's coordinate.

        :return: aDet value of the object's coordinate.
        :rtype: float
        """
        return self.__aDet

    @aDet.setter
    def aDet(self, value: float):
        self.__aDet = value

    @property
    def ts(self) -> float:
        """
        time of the object's coordinate. Default is 10 seconds.

        :return: time of the object's coordinate.
        :rtype: float
        """
        return self.__ts

    @ts.setter
    def ts(self, value: float):
        self.__ts = value

    @property
    def index(self) -> float:
        """
        order of Lambertian emission that depends on the half-angle at half illumination of the LED.

        :return: order of Lambertian emission
        :rtype: float
        """
        return self.__index

    @index.setter
    def index(self, value: float):
        self.__index = value

    @property
    def fov(self) -> float:
        """
        width of the field of view.

        :return: width of the field of view.
        :rtype: float
        """
        return self.__fov

    @fov.setter
    def fov(self, value: float):
        self.__fov = value

    @property
    def gCon(self) -> float:
        return self.__gCon

    @property
    def position(self) -> float:
        """
        Return the position of the object. This is a tuple of ( x y z)

        :return: the position of the object
        :rtype: tuple
        """
        return self.__position

    @property
    def q(self):
        """
        electronic load. Default is -1.602e-19 culombios

        :return: electronic load.
        :rtype: _type_
        """
        return self.__q

    @q.setter
    def q(self, value):
        self.__q = value

    @property
    def s(self):
        """
        ibg b - parameter of the Ib - Galactic model. Default is 5 seconds.

        :return: ibg b - parameter of the Ib - Galactic model.
        """
        return self.__s

    @s.setter
    def s(self, value):
        self.__s = value

    @property
    def b(self):
        """
        c b - parameter of the Ib - Galactic model.

        :return: c b - parameter of the Ib - Galactic model.
        """
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value

    @property
    def ibg(self) -> float:
        """
        background current. Default is 5.1e-3 Amperes.

        :return: background current.
        :rtype: float
        """
        return self.__ibg

    @ibg.setter
    def ibg(self, value):
        self.__ibg = value

    @property
    def cb(self) -> float:
        """
        Boltzmann constant. Default is 1.380649e-23 J/K.

        :return: Boltzmann constant.
        :rtype: float
        """
        return self.__cb

    @cb.setter
    def cb(self, value):
        self.__cb = value

    @property
    def tk(self) -> float:
        return self.__tk

    @tk.setter
    def tk(self, value):
        self.__tk = value

    @property
    def a(self) -> float:
        """
        n n - parameter of the B - parameter. Default is 10 seconds.

        :return: n n -  B - parameter
        :rtype: float
        """
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value

    @property
    def gv(self) -> float:
        """
        Open-loop voltage gain. Default is 10

        :return: Open-loop voltage gain.
        :rtype: float
        """
        return self.__gv

    @gv.setter
    def gv(self, value):
        self.__gv = value

    @property
    def n(self) -> float:
        """
        Fixed capacitance of the PD per unit area. Default is 1.12e-6.

        :return: Fixed capacitance of the PD per unit area.
        :rtype: float
        """
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    @property
    def fr(self) -> float:
        """
        FET channel noise factor. Default is 1.5

        :return: FET channel noise factor.
        :rtype: float
        """
        return self.__fr

    @fr.setter
    def fr(self, value):
        self.__fr = value

    @property
    def gm(self) -> float:
        """
        FET transconductance. Default is 3e-2.

        :return: FET transconductance.
        :rtype: float
        """
        return self.__gm

    @gm.setter
    def gm(self, value):
        self.__gm = value

    @property
    def i1(self) -> float:
        """
        constant experimental value. Default is 0.562.

        :return: constant experimental value.
        :rtype: float
        """
        return self.__i1

    @i1.setter
    def i1(self, value):
        self.__i1 = value

    @property
    def i2(self) -> float:
        """
        constant experimental value. Default is 0.0868.

        :return: constant experimental value.
        :rtype: float
        """
        return self.__i2

    @i2.setter
    def i2(self, value):
        self.__i2 = value

    @property
    def timeFirstConnected(self) -> float:
        """
        time point at which this receiver was first connected

        :return: time point at which this receiver was first connected
        :rtype: float
        """
        return self.__timeFirstConnected

    @timeFirstConnected.setter
    def timeFirstConnected(self, value):
        self.__timeFirstConnected = value

    @property
    def goalTime(self) -> float:
        """
        Amount of time that this receiver will be connected. Depends on tha SNR.

        :return: Amount of time that this receiver will be connected.
        :rtype: float
        """
        return self.__goalTime

    @goalTime.setter
    def goalTime(self, value):
        self.__goalTime = value

    @property
    def timeActive(self) -> float:
        """
        Effective time connected.

        :return: Effective time connected
        :rtype: float
        """
        return self.__timeActive

    @timeActive.setter
    def timeActive(self, value):
        self.__timeActive = value

    @property
    def timeFinished(self) -> float:
        """
        point in time when this receiver wil be finished.

        :return: point in time when this receiver wil be finished.
        :rtype: float
        """
        return self.__timeFinished

    @timeFinished.setter
    def timeFinished(self, value):
        self.__timeFinished = value


class Scenario:
    """
    Class that represents the characteristics of the scenario

    :return: _description_
    :rtype: _type_
    """

    numberOfAPs = 0
    """
    Number of access points in the scenario.

    :return: Number of access points in the scenario.
    :rtype: int
    """

    warnings.filterwarnings(
        "ignore", message="invalid value encountered in double_scalars"
    )

    def __init__(
        self, width: float, length: float, height: float, nGrids: int, rho: float
    ) -> None:
        """Scenario Constructor

        :param width: Width of the room
        :type width: float
        :param length: Length of the room
        :type length: float
        :param height: Height of the room
        :type height: float
        :param nGrids: Number of grids of each VLED
        :type nGrids: int
        :param rho: Reflexion coefficient
        :type rho: float
        """
        self.__length = length  # x
        self.__width = width  # y
        self.__height = height  # z

        self.__rho = rho

        self.__start_x = -self.__width / 2
        self.__start_y = -self.__length / 2
        self.__end_x = self.__width / 2
        self.__end_y = self.__length / 2

        self.__mobile_terminals = []
        self.__vleds = []
        self.__femtocells = []

        self.__vledsPositions = []
        self.__rfsPositions = []

        self.__nx = round(self.__length * nGrids)
        self.__ny = round(self.__width * nGrids)
        self.__nz = round(self.__height * nGrids)

        self.__g_x = np.linspace(self.__start_x, self.__end_x, self.__nx)
        self.__g_y = np.linspace(self.__start_y, self.__end_y, self.__ny)
        self.__g_z = np.linspace(0, self.__height, self.__nz)

        self.__g_xyz = np.array([self.__g_x, self.__g_y, self.__g_z], dtype=object)

    def addVLed(self, vled: VLed):
        """
        Add a VLED to this Scenario

        :param vled: the VLED to be added
        :type vled: VLed
        """
        self.__vleds.append(vled)
        self.__vledsPositions.append(Scenario.numberOfAPs)
        Scenario.numberOfAPs += 1

    def addRF(self, rf: RF):
        """
        Add an RF to this Scenario

        :param rf: The RF to be added
        :type rf: RF
        """
        self.__femtocells.append(rf)
        self.__rfsPositions.append(Scenario.numberOfAPs)
        Scenario.numberOfAPs += 1

    def getPowerInPointFromWalls(self, receiver: Receiver, vledID: int) -> float:
        """
        Get the incident power in an specific point in the room, received from the walls.

        :param receiver: The receiver which is in the point
        :type receiver: Receiver
        :param vledID: The VLED that is sending the signal
        :type vledID: int
        :return: Power from walls
        :rtype: float
        """
        vled = self.__vleds[vledID]
        h1 = self.__channelGainWall(receiver, vled, 1, 0)
        h2 = self.__channelGainWall(receiver, vled, 0, 1)
        h3 = self.__channelGainWall(receiver, vled, 1, 2)
        h4 = self.__channelGainWall(receiver, vled, 0, 3)
        power = (h1 + h2 + h3 + h4) * vled.totalPower * receiver.ts * receiver.gCon
        return float(power)

    def getPowerInPointFromVled(self, receiver: Receiver, vledID: int) -> float:
        """
        Get the power from the VLED in LOS

        :param receiver: The receiver which is in the point
        :type receiver: Receiver
        :param vledID: The VLED that is sending the signal
        :type vledID: int
        :return: Power from VLED
        :rtype: float
        """
        vled = self.__vleds[vledID]
        D_los = m.sqrt(
            (receiver.x - vled.x) ** 2
            + (receiver.y - vled.y) ** 2
            + (receiver.z - vled.z) ** 2
        )
        cosphi = (vled.z - receiver.z) / D_los
        # print(vled.x, vled.y, vled.z)
        # print(receiver.x, receiver.y, receiver.z)
        # print(cosphi)
        r_angle = m.degrees(m.acos(cosphi))
        H = (
            (vled.ml + 1)
            * receiver.aDet
            * cosphi ** (vled.ml + 1)
            / (2 * m.pi * D_los**2)
        )
        power = (
            vled.totalPower * H * receiver.ts * receiver.gCon
            if abs(r_angle) <= receiver.fov
            else 0
        )
        return power

    def __channelGainWall(
        self, receiver: Receiver, vled: VLed, posVar: int, posFixed: int
    ) -> float:
        """
        Gain in channel from walls

        :param receiver: The receiver which is in the point
        :type receiver: Receiver
        :param vled: The VLED that is sending the signal
        :type vled: VLed
        :param posVar: Auxiliar variable
        :type posVar: int
        :param posFixed: Auxiliar variable
        :type posFixed: int
        :return: Gain in channel
        :rtype: float
        """
        wall = None
        dA = self.__height
        if posFixed == 0:
            wall = (self.__start_x, 0)
            dA *= self.__length / (self.__nx * self.__nz)
        elif posFixed == 1:
            wall = (self.__start_y, 1)
            dA *= self.__width / (self.__ny * self.__nz)
        elif posFixed == 2:
            wall = (self.__end_x, 0)
            dA *= self.__length / (self.__nx * self.__nz)
        elif posFixed == 3:
            wall = (self.__end_y, 1)
            dA *= self.__width / (self.__ny * self.__nz)

        h = 0
        wp = np.full(3, wall[0])
        g = self.__g_xyz[posVar]
        for i in g:
            wp[posVar] = i
            for j in self.__g_z:
                wp[2] = j
                D1 = m.sqrt(np.dot(vled.position - wp, vled.position - wp))
                cosphi = abs(wp[2] - vled.position[2]) / D1
                cosalpha = abs(vled.position[wall[1]] - wp[wall[1]]) / D1
                D2 = m.sqrt(np.dot(wp - receiver.position, wp - receiver.position))
                cosbeta = abs(wp[wall[1]] - receiver.position[wall[1]]) / D2
                cospsi = abs(wp[2] - receiver.position[2]) / D2
                if abs(m.degrees(m.acos(cospsi))) <= receiver.fov:
                    h = h + (vled.ml + 1) * receiver.aDet * self.__rho * dA * (
                        cosphi**vled.ml
                    ) * cosalpha * cosbeta * cospsi / (
                        2 * (m.pi**2) * (D1**2) * (D2**2)
                    )
        return h

    @property
    def numberOfVLeds(self) -> int:
        """
        number of VLeds in this scenario

        :return: number of vleds
        :rtype: int
        """
        return len(self.__vleds)

    @property
    def numberOfRFs(self) -> int:
        """
        Number of RFs in this scenario

        :return: number of RFs
        :rtype: int
        """
        return len(self.__femtocells)

    @property
    def vleds(self) -> list:
        """
        set of VLEDs in this scenario.

        :return: set of VLEDs
        :rtype: list
        """
        return self.__vleds

    @property
    def rfs(self) -> list:
        """
        List of RFs in this scenario

        :return: List of RFs
        :rtype: list
        """
        return self.__femtocells

    @property
    def start_x(self) -> float:
        """
        Auxiliar variable determining the starting X coordinate of the room

        :return: Starting X coordinate
        :rtype: float
        """
        return self.__start_x

    @start_x.setter
    def start_x(self, value):
        self.__start_x = value

    @property
    def start_y(self) -> float:
        """
        Auxiliar variable determining the starting Y coordinate of the room

        :return: Starting Y coordinate
        :rtype: float
        """
        return self.__start_y

    @start_y.setter
    def start_y(self, value):
        self.__start_y = value

    @property
    def end_x(self) -> float:
        """
        Auxiliar variable determining the ending X coordinate of the room

        :return: Ending X coordinate
        :rtype: float
        """
        return self.__end_x

    @end_x.setter
    def end_x(self, value):
        self.__end_x = value

    @property
    def end_y(self) -> float:
        """
        Auxiliar variable determining the ending Y coordinate of the room

        :return: Ending Y coordinate
        :rtype: float
        """
        return self.__end_y

    @end_y.setter
    def end_y(self, value):
        self.__end_y = value

    @property
    def height(self) -> float:
        """
        Scenario height

        :return: Scenario height
        :rtype: float
        """
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def length(self) -> float:
        """
        Scenario Length

        :return: Scenario Length
        :rtype: float
        """
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def width(self) -> float:
        """
        Scenario width

        :return: Scenario width
        :rtype: float
        """
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def vledsPositions(self) -> list:
        """
        Vleds positions in room

        :return: Vleds position
        :rtype: list
        """
        return self.__vledsPositions

    @property
    def rfsPositions(self) -> list:
        """
        RFs positions

        :return: RFs positions
        :rtype: list
        """
        return self.__rfsPositions

    def snrVled(self, receiver: Receiver, vled: VLed) -> float:
        """
        Total SNR in an specific point from a VLED, considering walls and positions.

        :param receiver: Receiver device
        :type receiver: Receiver
        :param vled: VLED
        :type vled: VLed
        :return: Total SNR
        :rtype: float
        """
        powerReceived = self.getPowerInPointFromVled(
            receiver, vled.ID
        ) + self.getPowerInPointFromWalls(receiver, vled.ID)
        rd = (2 * receiver.q * receiver.s * powerReceived * receiver.b) + (
            2 * receiver.q * receiver.ibg * receiver.i1 * receiver.b
        )
        rt = (
            8
            * m.pi
            * receiver.cb
            * receiver.tk
            * receiver.n
            * receiver.a
            * receiver.b**2
            * (
                (receiver.i1 / receiver.gv)
                + (2 * m.pi)
                * receiver.fr
                / receiver.gm
                * receiver.n
                * receiver.a
                * receiver.i2
                * receiver.b
            )
        )
        rg = rd + rt
        return (receiver.s * powerReceived) ** 2 / rg

    def snrRf(self, receiver: Receiver, rf: RF) -> float:
        """
        Total SNR in an specific point from an RF.

        :param receiver: Receiver device
        :type receiver: Receiver
        :param rf: RF device
        :type rf: RF
        :return: Total SNR
        :rtype: float
        """
        df = m.sqrt(
            (receiver.x - rf.x) ** 2
            + (receiver.y - rf.y) ** 2
            + (receiver.z - rf.z) ** 2
        )

        return rf.pf * rf.Af * df ** (-rf.Ef)

    def capacityVled(self, receiver: Receiver, vled: VLed) -> float:
        """
        Capacity of the VLED channel considering receiver devices in an specific point.

        :param receiver: Receiver device
        :type receiver: Receiver
        :param vled: VLED
        :type vled: VLed
        :return: Capacity
        :rtype: float
        """
        return vled.B * m.log2(1 + self.snrVled(receiver, vled))

    def capacityRf(self, receiver: Receiver, rf: RF) -> float:
        """
        Capacity of the RF channel considering receiver devices in an specific point.

        :param receiver: Receiver device
        :type receiver: Receiver
        :param rf: RF
        :type rf: RF
        :return: Capacity
        :rtype: float
        """
        return rf.B * m.log2(1 + self.snrRf(receiver, rf))
