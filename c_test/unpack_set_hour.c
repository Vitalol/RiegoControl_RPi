#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t length;
} __attribute__((__packed__)) protocol_header_str;

typedef struct protocol_set_hour_str {
    protocol_header_str header;
    int32_t              time;
} __attribute__((__packed__)) protocol_set_hour_str;
int main() {
    char cadena[] = {0x02, 0x00, 0x01, 0x08, 0x8b, 0x2e, 0xb8, 0x64};

    if (sizeof(cadena) == sizeof(protocol_set_hour_str)) {
        protocol_set_hour_str estructura;

        // Copiar la cadena de bytes en la estructura
        memcpy(&estructura, cadena, sizeof(protocol_set_hour_str));

        // Imprimir los campos de la estructura
        printf("Header:\n");
        printf("  Destination: 0x%02X\n", estructura.header.destination);
        printf("  Origin:      0x%02X\n", estructura.header.origin);
        printf("  Type:        0x%02X\n", estructura.header.type);
        printf("  Length:      0x%02X\n", estructura.header.length);
        
        printf("Time: %ld\n", estructura.time);
    } else {
        printf("La cadena no tiene el mismo tamaño que la estructura protocol_set_hour_str.\n");
    }

    return 0;
}