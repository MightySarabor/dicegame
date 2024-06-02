import socket
import time
import random
import argparse

# Argument Parser
parser = argparse.ArgumentParser(description='Würfelspiel Spieler')
parser.add_argument('--server', type=str, default='localhost', help='Server-Adresse')
parser.add_argument('--port', type=int, default=12345, help='Portnummer')
parser.add_argument('--spielerlatenz', type=int, default=5, help='Maximale Spieler-Latenz in Sekunden')
parser.add_argument('name', type=str, help='Name des Spielers')
args = parser.parse_args()

SERVER = args.server
PORT = args.port
SPIELER_LATENZ = args.spielerlatenz
NAME = args.name

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    while True:
        message = client_socket.recv(1024).decode()
        if message == "START":
            time.sleep(random.uniform(5, SPIELER_LATENZ))
            wurf = random.randint(1, 100)
            wurf_time = time.time()
            client_socket.sendall(f"{wurf_time}:{NAME}:{wurf}".encode())
        elif message == "STOP":
            continue

if __name__ == "__main__":
    main()
