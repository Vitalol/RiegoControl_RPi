#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    const char* IP = "127.0.0.1";  // Dirección IP del servidor
    const int PUERTO = 12345;     // Puerto del servidor
    char buf[1024];

    // Inicializar Winsock
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        perror("WSAStartup");
        return 1;
    }

    // Crear el socket TCP/IP
    SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == INVALID_SOCKET) {
        perror("socket");
        WSACleanup();
        return 1;
    }

    // Configurar la dirección del servidor
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(IP);
    server_addr.sin_port = htons(PUERTO);

    // Conectar al servidor
    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        perror("connect");
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    const char* mensaje = "Hola, servidor!";
    if (send(sockfd, mensaje, strlen(mensaje), 0) == SOCKET_ERROR) {
        perror("send");
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    int bytes_leidos = recv(sockfd, buf, sizeof(buf) - 1, 0);
    if (bytes_leidos == SOCKET_ERROR) {
        perror("recv");
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    buf[bytes_leidos] = '\0';
    printf("Respuesta del servidor: %s\n", buf);

    // Cerrar el socket y finalizar Winsock
    closesocket(sockfd);
    WSACleanup();
    return 0;
}