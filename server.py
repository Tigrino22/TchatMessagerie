import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message)
                else:
                    self.clients.remove(client)
            except:
                continue

    def receive(self):
        while True:
            client, address = self.server.accept()
            print("Connected with: ", address)
            client.send(bytes("Welcome to the chatroom!", "utf-8"))
            self.clients.append(client)
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        receive_thread.join()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000
    server = Server(HOST, PORT)
    server.start()
