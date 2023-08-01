#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define MAX_MEASURES_NUM 3
#define PROTOCOL_NONE                 0
#define PROTOCOL_MSG_SET_TIME         1
#define PROTOCOL_MSG_DEFAULT_RULE     2
#define PROTOCOL_MSG_SET_SCHEDULER    3
#define PROTOCOL_MSG_SEND_MEASURE     4
#define PROTOCO_MSG_MANUAL_ACTIVATION 5
#define PROTOCOL_MSG_ACTUATION_RULE   6
#define PROTOCOL_MSG_SET_RULE         7

typedef struct measure_t {
    float   value;
    uint8_t type;
}__attribute__((__packed__)) measure_t;

typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t length;
}__attribute__((__packed__)) protocol_header_str;


typedef struct protocol_send_measure_str {
    protocol_header_str header;
    uint8_t             measures_num;
    measure_t           measures[MAX_MEASURES_NUM];
}__attribute__((__packed__)) protocol_send_measure_str;


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


    protocol_send_measure_str  test_msg = {0};


    test_msg.header.destination = 0;
    test_msg.header.origin = 2;
    test_msg.header.type = PROTOCOL_MSG_SEND_MEASURE;
    test_msg.measures_num = 1;
    test_msg.header.length = 0;

    test_msg.header.length = sizeof(protocol_header_str) +
        test_msg.measures_num * sizeof(measure_t) + 1;
    
    test_msg.measures[0].value = 10;
    test_msg.measures[0].type = 1;


    
    if (send(sockfd, (const char *)&test_msg, test_msg.header.length, 0) == SOCKET_ERROR) {
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