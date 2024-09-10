import math


def arctan(x, y):
    """
    输出角度都在0-360度之间，可区分四个象限
    :param x:
    :param y:
    :return:
    """
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    return angle


def coordinate_inversion(Xa, Ya, Xb, Yb):
    Dab = math.sqrt((Xb - Xa) ** 2 + (Yb - Ya) ** 2)
    alpha = arctan(Yb - Ya, Xb - Xa)
    return Dab, alpha


def coordinate_forward_calculation(Xa, Ya, Dab, alpha):
    """
    弧度制输入
    :param Xa:
    :param Ya:
    :param Dab:
    :param alpha:
    :return:
    """
    Xb = Xa + Dab * math.cos(alpha)
    Yb = Ya + Dab * math.sin(alpha)
    return Xb, Yb


if __name__ == '__main__':
    pass
