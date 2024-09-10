"""
用于工程测量的工具库
"""


def new_round(number, digits=3) -> str:
    """
    实现了四舍五入（单进双不进）的功能，可以指定保留几位小数
    Parameters
    ----------
    number
    digits

    Returns
    -------

    """
    if digits == 0:
        raise ValueError('digits should be greater than 0')
    # 将数字转换为字符串，以便操作小数点后的具体位数
    num_str = str(number)

    # 分离整数部分和小数部分
    parts = num_str.split('.')

    if len(parts) == 2:
        integer_part = int(parts[0])
        decimal_part = parts[1]

        # 检查第四位小数
        if len(decimal_part) >= digits + 1:
            decimal_part = decimal_part[: digits + 1]
            fourth_digit = int(decimal_part[digits])  # 第四位小数
            third_digit = int(decimal_part[digits - 1])  # 第三位小数

            # 如果第四位是5，则根据第三位是否为奇数来决定是否进位
            if fourth_digit == 5:
                if third_digit % 2 == 1:
                    # 第三位是奇数，进位
                    temp = str(int(decimal_part[:digits]) + 1)
                    if decimal_part[0] == '0':
                        decimal_part = '0' + temp
                    else:
                        decimal_part = temp
                    # 处理小数部分只剩下三位
                    if len(decimal_part) > digits:
                        integer_part += 1
                        decimal_part = decimal_part[1:]
                else:
                    # 第三位是偶数，不进位
                    decimal_part = decimal_part[:digits]
            else:
                return f'{str(round(number, digits)):0<{digits + len(parts[0]) + 1}}'

        # 重新组合数字并转换为浮点数
        result_str = str(integer_part) + '.' + decimal_part
        return f'{result_str:0<{digits + len(parts[0]) + 1}}'
    else:
        num_str += '.'
        return f'{num_str:0<{digits + len(num_str)}}'


if __name__ == '__main__':
    print(new_round(8.0975567, 4))
