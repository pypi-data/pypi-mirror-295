from astropy.units import UnitBase
import numpy as np


def convertUnitToLateX(unit: UnitBase):
    s = "$\mathrm{"
    bases = unit.bases
    powers = np.array(unit.powers)
    positivePowers = powers[powers > 0]
    negativePowers = powers[powers < 0]
    positivePowerCount = len(positivePowers)
    negativePowerCount = len(negativePowers)
    if positivePowerCount == 0:
        s += "1"
    else:
        for i in range(positivePowerCount):
            if i > 0:
                s += "\\cdot " + str(bases[i])
            else:
                s += str(bases[i])
            if (np.abs(positivePowers[i]) != 1):
                s += "^{" + str(np.abs(positivePowers[i])) + "}"
    if negativePowerCount > 0:
        s += "/"
        if negativePowerCount > 1:
            s += "("
        for i in range(negativePowerCount):
            if i > 0:
                s += "\\cdot " + str(bases[i + positivePowerCount])
            else:
                s += str(bases[i + positivePowerCount])
            if (np.abs(negativePowers[i]) != 1):
                s += "^{" + str(np.abs(negativePowers[i])) + "}"
        if negativePowerCount > 1:
            s += ")"
    return s + "}$"
