import socket
import threading

# 参数
LOCAL_HOST = "0.0.0.0"  # 代理服务器监听的地址
LOCAL_PORT = 9223  # 代理服务器监听的端口
REMOTE_HOST = "127.0.0.1"  # 目标服务器的地址
REMOTE_PORT = 9222  # 目标服务器的端口


def handle_client(client_socket):
    # 连接到远程服务器
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((REMOTE_HOST, REMOTE_PORT))

    # 两个线程，一个用来把客户端的数据转发到远程服务器，
    # 另一个用来把远程服务器的数据转发回客户端

    def forward_data(src_socket, dst_socket):
        try:
            while True:
                data = src_socket.recv(4096)
                if len(data) == 0:
                    break
                dst_socket.send(data)
        except Exception:
            pass
        finally:
            src_socket.close()
            dst_socket.close()

    # 创建线程来转发数据
    threading.Thread(target=forward_data, args=(client_socket, remote_socket)).start()
    threading.Thread(target=forward_data, args=(remote_socket, client_socket)).start()


def start_proxy():
    # 创建监听套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((LOCAL_HOST, LOCAL_PORT))
        server_socket.listen(5)
        print(f"[*] 代理服务器启动，监听 {LOCAL_HOST}:{LOCAL_PORT}")

        # 主循环，接受客户端连接
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"[*] 接收到来自 {addr} 的连接")

                # 为每个客户端连接创建一个新线程
                client_handler = threading.Thread(
                    target=handle_client, args=(client_socket,)
                )
                client_handler.start()

            except socket.error as e:
                print(f"[!] 处理客户端连接时发生错误：{e}")

    except socket.error as e:
        print(f"[!] 无法绑定到 {LOCAL_HOST}:{LOCAL_PORT}. 错误信息: {e}")
    finally:
        server_socket.close()  # 确保在发生异常时也能关闭套接字
