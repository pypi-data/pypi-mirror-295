"""
This module implements the aligned-spin TaylorT3 equations.

Some references:

 - [arXiv:0802.1249](https://arxiv.org/abs/0802.1249)
 - [arXiv:0901.2437](https://arxiv.org/abs/0901.2437)
 - [arXiv:0610122](https://arxiv.org/abs/gr-qc/0610122)
 - [arXiv:0907.0700](https://arxiv.org/abs/0907.0700)
 - [arXiv:0406012](https://arxiv.org/abs/gr-qc/0406012)
 - [arXiv:1210.2339](https://arxiv.org/abs/1210.2339)
 - [arXiv:1210.2339](https://arxiv.org/abs/1210.2339)
 - [arXiv:2004.08302](http://arxiv.org/abs/2004.08302)
 - [arXiv:2012.11923](http://arxiv.org/abs/2012.11923)
 - [LALSimInspiralTaylorT3.c](https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralTaylorT3.c)
 - [LALSimInspiralPNCoefficients.c](https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralPNCoefficients.c)
"""

import numpy as np
from lal import GAMMA, MTSUN_SI


def Msun_to_sec(M: float | int) -> float:
    """
    Geometric units convertion.
    convert mass (in units of solar masses)
    into seconds.

    The equation is M * MSUN_SI * G_SI / C_SI**3.

    Parameters
    ----------
    M : float | int
        Total mass in solar masses

    Returns
    -------
    float | int
        Mass converted into units of seconds.
    """
    #     return
    return M * MTSUN_SI


def TaylorT3_Omega_GW_Newt(t, tc: float | int, eta: float, M: float | int):
    """
    Newtonian pre factor for GW angular frequency

    Parameters
    ----------
    t : number or array
        The time coordinate
    tc : float | int
        The TaylorT3 coalescence time
    eta : float
        The symmetric mass ratio
    M : float | int
        Total mass in solar masses

    Returns
    -------
    float or array
        Newtonian pre factor for GW angular frequency
    """
    theta = TaylorT3_theta(t, tc, eta, M)
    return theta**3 / (8.0 * M)


def TaylorT3_theta(t, tc, eta, M):
    """
    Taylor3 parameter
    """
    theta = eta * (tc - t) / (5 * M)
    theta = theta ** (-1 / 8.0)
    return theta


def TaylorT3_Omega_GW(t, tc, eta, M):
    """
    22 mode angular GW frequency
    equation 7 in 0901.2437

    3.5PN term from https://arxiv.org/pdf/gr-qc/0610122.pdf and https://arxiv.org/pdf/0907.0700.pdf
    and this too apparently https://arxiv.org/pdf/gr-qc/0406012.pdf?

    https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralTaylorT3.c

    https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralPNCoefficients.c

    t: time
    tc: coalescence time
    eta: symmetric mass ratio
    M: total mass (Msun)
    """

    pi2 = np.pi * np.pi

    theta = TaylorT3_theta(t, tc, eta, M)

    theta2 = theta * theta
    theta3 = theta2 * theta
    theta4 = theta3 * theta
    theta5 = theta4 * theta
    theta6 = theta5 * theta
    theta7 = theta6 * theta

    # pre factor
    ftaN = 1.0 / (8.0 * M)
    # 0PN
    fts1 = 1.0
    # 0.5PN = 0 in GR
    # 1PN
    fta2 = 7.43 / 26.88 + 1.1 / 3.2 * eta
    # 1.5PN
    fta3 = -3.0 / 10.0 * np.pi
    # 2PN
    fta4 = 1.855099 / 14.450688 + 5.6975 / 25.8048 * eta + 3.71 / 20.48 * eta * eta
    # 2.5PN
    fta5 = (-7.729 / 21.504 + 1.3 / 25.6 * eta) * np.pi
    # 3PN
    fta6 = (
        -7.20817631400877 / 2.88412611379200
        + 5.3 / 20.0 * pi2
        + 1.07 / 2.80 * GAMMA
        + (25.302017977 / 4.161798144 - 4.51 / 20.48 * pi2) * eta
        - 3.0913 / 183.5008 * eta * eta
        + 2.35925 / 17.69472 * eta * eta * eta
    )

    # 3.5PN
    fta7 = (
        -1.88516689 / 4.33520640 - 9.7765 / 25.8048 * eta + 1.41769 / 12.90240 * eta * eta
    ) * np.pi

    # 3PN log term
    ftal6 = 1.07 / 2.80

    omega_orb = (
        theta3
        * ftaN
        * (
            fts1
            + fta2 * theta2
            + fta3 * theta3
            + fta4 * theta4
            + fta5 * theta5
            + (fta6 + ftal6 * np.log(2.0 * theta)) * theta6
            + fta7 * theta7
        )
    )

    # convert from orb to 22 GW
    return 2 * omega_orb


def Hhat22_pre_factor(x, eta):
    """
    https://arxiv.org/pdf/0802.1249.pdf
    eq. 9.3a and 9.3b
    """
    return np.sqrt(16.0 * np.pi / 5) * 2 * eta * x


def Hhat22_x(x, eta):
    """
    https://arxiv.org/pdf/0802.1249.pdf - eq. 9.4a

    3.5PN term: https://arxiv.org/pdf/1210.2339.pdf

    here we leave the expression to depend on the post-newtonian
    parameter 'x' so that you can choose how to calculate it.
    e.g., from PN like TaylorT3 or from the model which
    is TaylorT3 + corrections

    return complex
    """

    xarr = np.zeros(8, dtype=np.complex128)

    C = 0.577216  # is the Euler constant

    xarr[0] = 1.0
    # 0.5 PN term is zero
    xarr[1] = 0
    xarr[2] = -107.0 / 42 + 55 * eta / 42
    xarr[3] = 2.0 * np.pi
    xarr[4] = -2173.0 / 1512 - 1069.0 * eta / 216 + 2047.0 * eta**2 / 1512
    xarr[5] = (
        -107 * np.pi / 21 - 24.0 * 1.0j * eta + 34.0 * np.pi * eta / 21
    )  # there is an i... not sure what to do...

    x6a = 27027409.0 / 646800 - 856.0 * C / 105 + 428 * 1.0j * np.pi / 105 + 2.0 * np.pi**2 / 3
    x6b = (
        (-278185.0 / 33264 + 41 * np.pi**2 / 96) * eta
        - 20261.0 * eta**2 / 2772
        + 114635.0 * eta**3 / 99792
    )

    x6log = -428.0 * np.log(16 * x) / 105

    xarr[6] = x6a + x6b  # there is an i...  not sure what to do...

    xarr[7] = (
        -2173 * np.pi / 756
        + (-(2495 * np.pi / 378) + (14333 * 1.0j / 162)) * eta
        + ((40 * np.pi / 27) - (4066 * 1.0j / 945)) * eta**2
    )

    # pn = xarr[0] + x*xarr[2] + x**(3/2.)*xarr[3] + x**2*xarr[4] + x**(5/2.)*xarr[5] + x**3*(xarr[6] + x6log) + x**(7/2.)*xarr[7]
    pn = xarr[0]
    pn += x * xarr[2]
    pn += x ** (3 / 2.0) * xarr[3]
    pn += x**2 * xarr[4]
    pn += x ** (5 / 2.0) * xarr[5]
    pn += x**3 * (xarr[6] + x6log)
    pn += x ** (7 / 2.0) * xarr[7]

    pre = Hhat22_pre_factor(x, eta)

    return pre * pn


def x_from_omega_22(GW22AngFreq, M=1):
    OrgAngFreq = GW22AngFreq / 2
    x = (M * OrgAngFreq) ** (2.0 / 3)
    return x


def TaylorT3_Hhat22(t, tc, eta, M):
    """
    https://arxiv.org/pdf/0802.1249.pdf - eq. 9.4a
    Post-Newtonian expression for (l,m)=(2,2) time domain
    amplitude assuming TaylorT3 frequency evolution
    """

    GW22AngFreq = TaylorT3_Omega_GW(t, tc, eta, M)
    x = x_from_omega_22(GW22AngFreq, M)
    return Hhat22_x(x, eta)
