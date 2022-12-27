import tkinter as tk
import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.root.title("Messenger")

        # Création de l'interface graphique
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_entry = tk.Entry(self.root)
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.messages_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.messages_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messages_frame.pack()
        self.entry_field = tk.Entry(self.root, bd=0, bg="white", width="29")
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack()
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        # Placement des éléments de l'interface graphique
        self.username_label.pack()
        self.username_entry.pack()
        self.connect_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect(self):
        self.client.connect((self.host, self.port))
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # Envoi du pseudo au serveur
        username = self.username_entry.get()
        self.client.send(bytes(username, "utf-8"))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message:
                    self.messages_list.insert(tk.END, message)
            except:
                continue

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        # Ajout du pseudo devant chaque message
        username = self.username_entry.get()
        message = username + ": " + message
        self.client.send(bytes(message, "utf-8"))
        if message == "{quit}":
            self.client.close()
            self.root.quit()

    def on_closing(self):
        self.send_message("{quit}")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000
    client = Client(HOST, PORT)
    tk.mainloop()

