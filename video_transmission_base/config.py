# 图像转换成jpg格式传输，每次
#  数据头记录数据长度
# 
# 
# 

PACKAGE_SIZE = 4096
PACKAGE_HEAD_SIZE = 4 # 4 * 8 共32位头部数据
PACKAGE_DATA_SIZE = PACKAGE_SIZE - PACKAGE_HEAD_SIZE

COMMUNICATION_ADDR = "127.0.0.1"
COMMUNICATION_PORT = 8888