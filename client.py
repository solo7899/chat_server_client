import socket
import threading 
import sys

HOST, PORT = "127.0.0.1", 5555
RUNNING = True


def receive(client: socket.socket, nickname: str):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "NickName":
                client.send(nickname.encode("utf-8"))
                continue
            print(message)
            
        except Exception as e :
            print(f"Error occured!!!\n\t Error: {e}")
            client.close()
            global RUNNING
            RUNNING = False
            break

def write(client : socket.socket, nickname: str):
    while RUNNING:
        message = f'{nickname} : {input("> ")}'
        client.send(message.encode("utf-8"))

def stop():
    for t in threading.enumerate():
        if t is threading.main_thread():
            continue
        t.join()
        

def main():
    nickname = input("Enter a nickname: ")
    while not nickname.strip():
        nickname = input("Enter a nickname: ")

    client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    recieve_message = threading.Thread(target=receive, args=(client, nickname))
    recieve_message.start()

    write_message = threading.Thread(target=write, args=(client, nickname))
    write_message.start()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        RUNNING = False
        stop()
        sys.exit()