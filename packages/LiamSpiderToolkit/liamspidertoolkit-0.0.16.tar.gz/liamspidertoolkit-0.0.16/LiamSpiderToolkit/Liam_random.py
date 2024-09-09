
def randint():
    print("Liam Random Init")


def random():
    print("Liam Random")


def randrange():
    print("Liam Random Range")


'''
import hashlib
import time

def generate_random_number(length=8):
    """
    生成一个基于当前时间戳的"随机"数字字符串。

    参数:
    length -- 生成字符串的长度，默认为8。

    返回:
    一个长度为length的随机数字字符串。
    """
    # 获取当前时间戳（以微秒为单位）
    timestamp = int(time.time() * 1000000)
    # 将时间戳转换为字节串
    timestamp_bytes = str(timestamp).encode('utf-8')
    # 使用hashlib的sha256算法对字节串进行哈希
    hashed_data = hashlib.sha256(timestamp_bytes).hexdigest()
    # 取哈希值的前length位作为随机数
    random_number = hashed_data[:length]
    # 由于哈希值是十六进制表示的，我们可能需要转换为十进制数字字符串
    # 这里简单起见，直接返回十六进制字符串，如果需要十进制，可以进一步转换
    # random_number_decimal = int(random_number, 16)
    # 注意：如果length不是8的倍数，转换为十进制可能会导致数据丢失
    
    # 如果确实需要十进制数字，可以考虑只取哈希值的一部分进行转换
    # 例如：random_number_decimal = int(hashed_data[:8], 16)
    
    return random_number

# 示例
print(generate_random_number())  # 输出一个随机十六进制数字字符串
# 如果你需要十进制数字，可以取消注释相关代码行
'''


'''
import time

def generate_random_number_in_range(min_val, max_val):
    """
    生成一个位于[min_val, max_val]范围内的随机整数（包含边界值）。

    注意：这里的“随机”是基于当前时间戳的，因此并不适合加密或安全敏感的应用。

    参数:
    min_val -- 范围的最小值（包含）
    max_val -- 范围的最大值（包含）

    返回:
    一个位于[min_val, max_val]范围内的随机整数。
    """
    # 确保max_val大于min_val
    if max_val <= min_val:
        raise ValueError("max_val must be greater than min_val")

    # 获取当前时间戳（以秒为单位），然后乘以一个大数（或进行其他变换）以增加“随机性”
    # 注意：这里的时间戳精度较低，可能导致在短时间内生成的随机数相同
    # 为了增加随机性，你可以考虑使用时间戳的更高精度（如毫秒、微秒）或结合其他系统状态
    timestamp = int(time.time())

    # 使用模运算将时间戳映射到所需范围内
    # 注意：这种方法可能会在某些情况下导致生成的随机数分布不均匀
    random_number = (timestamp % (max_val - min_val + 1)) + min_val

    return random_number

# 示例
print(generate_random_number_in_range(1, 100))  # 输出一个1到100之间的随机整数
'''
