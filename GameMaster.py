import socket
import threading
import time
import random
import argparse
from datetime import datetime

# Argument Parser
parser = argparse.ArgumentParser(description='Würfelspiel Spielleiter')
parser.add_argument('--host', type=str, default='localhost', help='Host-Adresse')
parser.add_argument('--port', type=int, default=12345, help='Portnummer')
parser.add_argument('--spieler_latenz', type=int, default=5, help='Maximale Spieler-Latenz in Sekunden')
parser.add_argument('--dauer_der_runde', type=int, default=10, help='Dauer der Runde in Sekunden')
args = parser.parse_args()

HOST = args.host
PORT = args.port
SPIELER_LATENZ = args.spieler_latenz
DAUER_DER_RUNDE = args.dauer_der_runde

clients = []
lock = threading.Lock()


def handle_client(client_socket, addr):
    global clients
    with lock:
        clients.append((client_socket, addr))
    print(f"{addr} verbunden.")


def start_round():
    global clients
    print("Starte Runde...")
    start_time = time.time()
    send_start_message()
    time.sleep(DAUER_DER_RUNDE)
    send_stop_message()

    receive_results(start_time)


def send_start_message():
    current_timestamp = time.time()
    current_time = datetime.fromtimestamp(current_timestamp)
    print(current_time)
    for client_socket, _ in clients:
        try:
            client_socket.sendall("START".encode())
        except Exception as e:
            print(f"Fehler beim Senden der START-Nachricht: {e}")


def send_stop_message():
    for client_socket, _ in clients:
        try:
            client_socket.sendall("STOP".encode())
        except Exception as e:
            print(f"Fehler beim Senden der STOP-Nachricht: {e}")


def receive_results(start_time):
    results = {}

    for client_socket, addr in clients:
        try:
            client_socket.settimeout(DAUER_DER_RUNDE)
            data = client_socket.recv(1024).decode()
            wurf_time_str, name, wurf = data.split(":")
            wurf_time = float(wurf_time_str)
            wurf = int(wurf)

            if wurf_time - start_time <= DAUER_DER_RUNDE:
                # Speichere den letzten Wurf eines Spielers in der aktuellen Runde
                results[name] = wurf
                print(f"{name} hat {wurf} geworfen.")
            else:
                print(f"Wurf von {name} kam zu spät und wird nicht berücksichtigt.")
        #except socket.timeout:
        #    print(f"Timeout für Spieler {addr}. Kein Wurf empfangen.")
        except Exception as e:
            print(f"Fehler beim Empfangen von {addr}: {e}")

    if results:
        winner = max(results.items(), key=lambda x: x[1])
        print(f"Gewinner der Runde: {winner[0]} mit einem Wurf von {winner[1]}")
        with open('ergebnisse.txt', 'a') as file:
            file.write(f"{winner[0]}: {winner[1]}\n")



def accept_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server läuft und hört auf {HOST}:{PORT}")

    connection_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    connection_thread.start()

    while True:
        start_round()


if __name__ == "__main__":
    main()
