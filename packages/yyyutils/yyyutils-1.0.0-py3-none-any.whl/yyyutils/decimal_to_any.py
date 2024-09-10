"""
功能：将十进制数转换为任意进制数
"""


def decimal_to_any(decimal, base):
    if base < 2 or base > 36:
        return "Error: Base should be between 2 and 36"
    if decimal == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while decimal > 0:
        decimal, remainder = divmod(decimal, base)
        result += digits[remainder]
    return result[::-1]

# 示例
if __name__ == '__main__':
    decimal = 123456789
    base = 16
    print(decimal_to_any(decimal, base))  # Output: 75BCD15
