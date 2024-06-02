import socket
import time
import random
import argparse
import threading

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
runde_counter = 0
ergebnisse = {}  # Dictionary zur Speicherung der Spielergebnisse

def handle_client(client_socket, addr):
    global clients
    with lock:
        clients.append((client_socket, addr))
    print(f"{addr} verbunden.")

def start_round():
    global clients, runde_counter, ergebnisse
    runde_counter += 1
    send_start_message()  # Rundenzähler zuerst inkrementieren
    print(f"Starte Runde {runde_counter}...")
    time.sleep(DAUER_DER_RUNDE)
    send_stop_message()
    receive_results()
    log_results()

def send_start_message():
    for client_socket, _ in clients:
        try:
            client_socket.sendall(f"START:{runde_counter}".encode())  # Rundenzähler senden
        except Exception as e:
            print(f"Fehler beim Senden der START-Nachricht: {e}")

def send_stop_message():
    for client_socket, _ in clients:
        try:
            client_socket.sendall("STOP".encode())
        except Exception as e:
            print(f"Fehler beim Senden der STOP-Nachricht: {e}")

def receive_results():
    global ergebnisse
    results = {}
    for client_socket, addr in clients:
        try:
            client_socket.settimeout(DAUER_DER_RUNDE)
            data = client_socket.recv(1024).decode()
            name, wurf, runde = data.split(":")
            wurf = int(wurf)
            runde = int(runde)
            if runde_counter == runde:
                results[name] = wurf
                print(f"{name} hat in Runde {runde} {wurf} geworfen.")
            else:
                print(f"Der Wurf von {name} gilt nicht. Der Wurf war aus Runde {runde} und wir sind schon in Runde {runde_counter}!")
                print(f"Pass besser auf! Wir sind jetzt in Runde {runde_counter}.")
                # Synchronisiere die Runde des Spielers mit der aktuellen Runde
                try:
                    client_socket.sendall(f"SYNCHRONIZE:{runde_counter}".encode())
                except Exception as e:
                    print(f"Fehler beim Senden der SYNCHRONIZE-Nachricht: {e}")

        except socket.timeout:
            print(f"{addr} hat verschlafen! Wach auf, dann darfst du wieder mitspielen!")
        except Exception as e:
            print(f"Fehler beim Empfangen von {addr}: {e}")

    if results:
        winner = max(results.items(), key=lambda x: x[1])
        print(f"Gewinner der Runde {runde_counter}: {winner[0]} mit einem Wurf von {winner[1]}")
        ergebnisse[runde_counter] = winner  # Ergebnisse für die aktuelle Runde speichern

def log_results():
    with open("ergebnisse_logical.txt", "w") as file:  # Öffne die Datei im Schreibmodus ("w")
        file.truncate()  # Leere den Inhalt der Datei
        for runde, (name, wurf) in ergebnisse.items():
            file.write(f"Gewinner der Runde {runde}: {name} mit einem Wurf von {wurf}\n")


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
