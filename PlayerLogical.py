import socket
import time
import random
import argparse
import threading

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
AKTUELLE_RUNDE = 0

def main():
    global AKTUELLE_RUNDE
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    while True:
        message = client_socket.recv(1024).decode()
        if message.startswith("START"):
            _, runde = message.split(":")
            AKTUELLE_RUNDE = int(runde)
            time.sleep(random.uniform(0, SPIELER_LATENZ))
            wurf = random.randint(1, 100)
            client_socket.sendall(f"{NAME}:{wurf}:{AKTUELLE_RUNDE}".encode())
        elif message == "STOP":
            continue
        elif message.startswith("SYNCHRONIZE"):
            _, runde = message.split(":")
            AKTUELLE_RUNDE = int(runde)

if __name__ == "__main__":
    main()
