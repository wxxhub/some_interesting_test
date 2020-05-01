#coding:utf-8

import socket
import threading
import numpy as np
import cv2 as cv
from config import *

def reciveAll(socket, size):
    buf = bytes()
    while size:
        recv_buf = socket.recv(size)
        if not recv_buf: return None
        buf += recv_buf
        size -= len(recv_buf)
    
    return buf

def toImage(name, data):
    image_data = np.fromstring(data, np.uint8)
    image = cv.imdecode(image_data, 1)

    cv.imshow(name, image)
    cv.waitKey(10)
    pass

def calculateHead(head):
    value = 0
    for i in range(PACKAGE_HEAD_SIZE):
        value = value << 8
        value += int(head[i])
    
    return value

def clientThread(client, addr):
    last_head_value = 0
    current_head_value = 0
    data = bytes()

    while True:
        recv_data = reciveAll(client, PACKAGE_SIZE)

        if not recv_data:
            print ("client {} disconnect!".format(addr))
            break

        current_head_value = calculateHead(recv_data[:4])

        # 如果本次头部值和上次头部值相同，判断是否为同一组数据。如果本次头部值和上次头部值不同，那么这就不是同一组数据。    
        if current_head_value == last_head_value:
            #检查数据长度和头部值，判断是否为同一组数据
            data += recv_data[4:]
            data_len = len(data)
            #如果数据长度小于头部值那么为同一组数据，如果大于等于，那么这就是这组数据的最后一个package
            if data_len >= current_head_value:
                print ("i recive a image..")
                toImage(str(addr), data)

                # 进行重置。
                data = bytes()
        else:
            # 数据已经接收了，由于不属于同一组，所以进行更新。
            data = recv_data[4:]

            last_head_value = current_head_value

    client.close()
    pass

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((COMMUNICATION_ADDR, COMMUNICATION_PORT))

    server_socket.listen(5)

    while True:
        client, addr = server_socket.accept()

        threading.Thread(target=clientThread, args=(client, addr)).start()

    pass

if __name__ == '__main__':
    main()


### 这一部分是另一个判断逻辑
# # 如果本次头部值和上次头部值不同，那么这就不是同一组数据。
# if current_head_value != last_head_value: 
#     # 如果收到的数据长度大于等于头部值，那么这组数据完成了传输，否则没有完成传输
#     data_len = len(data)
#     if last_head_value >0 and data_len >= last_head_value:
#         print ("i recive a image.")
#         toImage(addr, data)
#     else:
#         if data_len > 0:
#             print ("error")

#     # 数据已经接收了，由于不属于同一组，所以进行更新。
#     data = recv_data[4:]

#     last_head_value = current_head_value
# else:
#     #检查数据长度和头部值，判断是否为同一组数据
#     data += recv_data[4:]
#     data_len = len(data)
#     #如果数据长度小于头部值那么为同一组数据，如果大于等于，那么这就是这组数据的最后一个package
#     if data_len >= current_head_value:
#         print ("i recive a image..")
#         toImage(str(addr), data)

#         # 进行重置。
#         data = bytes()