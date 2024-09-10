def dms_to_degrees(d, m, s) -> float:
    """
    将度分秒形式的坐标转换为度形式
    """
    d, m, s = float(d), float(m), float(s)
    decimal_degrees = d + m / 60 + s / 3600
    return decimal_degrees


def degrees_to_dms(decimal_degrees) -> tuple:
    """
    将度形式的坐标转换为度分秒形式
    """
    if decimal_degrees < 0:
        sign = '-'
        decimal_degrees = abs(decimal_degrees)
    else:
        sign = ''
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = round(decimal_degrees * 3600 - degrees * 3600 - minutes * 60)
    # 都保留为两位整数，不足的部分用0补齐
    degrees = str(degrees).zfill(2)
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)
    return f'{sign}{degrees}°{minutes}′{seconds}″',-float(degrees),-float(minutes),-float(seconds)


if __name__ == '__main__':
    decimal_degrees = dms_to_degrees(30, 45, 30)
    print(decimal_degrees)
    dms = degrees_to_dms(decimal_degrees)
    print(dms)
