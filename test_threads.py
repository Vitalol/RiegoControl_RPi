import threading
import socket
import os
import sensors.rc_protocol as RCP

def lora_sender():
    """Esta tarea recibe la comunicación por socket y envía los datos.
    """
    # Definir la dirección IP y el puerto del servidor
    IP = "127.0.0.1"  # Dirección IP local del servidor
    PUERTO = 54321    # Puerto para la comunicación

    # Crear el socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular el socket a la dirección y puerto
    server_socket.bind((IP, PUERTO))

    # Establecer el límite máximo de conexiones pendientes en la cola
    server_socket.listen(1)

    print("Esperando conexiones...")

    while True:
        # Aceptar conexiones entrantes
        client_socket, client_address = server_socket.accept()

        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if data:
                print(f"Datos recibidos del cliente: {data.hex()}")

                # Responder al cliente
                respuesta = "¡Hola desde el servidor!"
                client_socket.sendall(respuesta.encode())

        finally:
            # Cerrar la conexión con el cliente
            client_socket.close()


def lora_receiver():
    """Esta tarea va recibiendo lecturas 
    """
    # Definir la dirección IP y el puerto del servidor
    IP = "127.0.0.1"  # Dirección IP local del servidor
    PUERTO = 12345    # Puerto para la comunicación

    # Crear el socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular el socket a la dirección y puerto
    server_socket.bind((IP, PUERTO))

    # Establecer el límite máximo de conexiones pendientes en la cola
    server_socket.listen(1)

    print("Esperando conexiones...")

    while True:
        # Aceptar conexiones entrantes
        client_socket, client_address = server_socket.accept()

        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if data:
                print(f"Datos recibidos del cliente: {data.hex()}")
                RCP.rc_protocol_handle_received_msg(data)
                # Responder al cliente
                respuesta = "¡Hola desde el servidor!"
                client_socket.sendall(respuesta.encode())

        finally:
            # Cerrar la conexión con el cliente
            client_socket.close()

lora_semaphore = threading.Semaphore(1)

sender_thread = threading.Thread(target=lora_sender)
receiver_thread = threading.Thread(target=lora_receiver)

sender_thread.start()
receiver_thread.start()