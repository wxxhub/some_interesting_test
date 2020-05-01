#coding:utf-8

import socket
import time
import cv2 as cv
import numpy as np
from config import *

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((COMMUNICATION_ADDR, COMMUNICATION_PORT))

    capture = cv.VideoCapture(0)

    ret, frame = capture.read()

    while ret:

        ## mat转jpg,再转为bytes
        _, encode_img = cv.imencode('.jpg', frame)
        data_arry = np.array(encode_img)
        data = data_arry.tostring()

        ## 获取数据长度
        data_size = len(data)

        ## 用数据长度作头
        head_data = data_size
        head_index = PACKAGE_HEAD_SIZE - 1
        head_value = [0 for i in range(PACKAGE_HEAD_SIZE)]
        while head_data >= 0 and head_data > 0:

            head_value[head_index] = head_data & 0xff
            head_data = head_data >> 8
            head_index -= 1
            pass
        
        # 转换为bytes
        head = bytes(head_value)

        # 将数据分组
        package_num = int(data_size / PACKAGE_DATA_SIZE)

        # 分段发送
        for i in range(package_num):
            send_data = head + data[i * PACKAGE_DATA_SIZE : (i+1) * PACKAGE_DATA_SIZE]
            print (len(send_data))
            send_len = client_socket.sendall(send_data)
            print (send_len)
        
        # 由于int(data_size / PACKAGE_DATA_SIZE)舍去了小数点后面的数据，所以要检查实际发送的和实际数据量
        if data_size > package_num * PACKAGE_DATA_SIZE:
            send_data = head + data[package_num * PACKAGE_DATA_SIZE :] + bytearray(PACKAGE_DATA_SIZE - (data_size%PACKAGE_DATA_SIZE))
            print (len(send_data))
            send_len = client_socket.sendall(send_data)
            print (send_len)
            pass
        
        # 数据复原
        recovery_data = np.fromstring(data, np.uint8)
        recovery_image = cv.imdecode(recovery_data, cv.IMREAD_COLOR)

        cv.imshow('origin_image', frame)
        cv.imshow('recovery_image', recovery_image)
        cv.waitKey(10)

        ret, frame = capture.read()
    pass

    print ("colse")
    client_socket.close()

if __name__ == '__main__':
    main()