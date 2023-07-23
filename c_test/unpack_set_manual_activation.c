#include <stdio.h>
#include <stdint.h>

typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t length;
} __attribute__((__packed__)) protocol_header_str;

typedef struct protocol_manual_activation {
    protocol_header_str header;
    uint8_t             actuatorID;
    uint8_t             duration;
} __attribute__((__packed__)) protocol_manual_activation;

int main() {
    uint8_t bytes[] = {0x02, 0x00, 0x01, 0x08, 0x02, 0x0f};

    if (sizeof(bytes) == sizeof(protocol_manual_activation)) {
        protocol_manual_activation manual_activation;

        // Copiar los bytes en la estructura
        memcpy(&manual_activation, bytes, sizeof(protocol_manual_activation));

        // Imprimir los campos de la estructura
        printf("Header:\n");
        printf("  Destination: 0x%02X\n", manual_activation.header.destination);
        printf("  Origin:      0x%02X\n", manual_activation.header.origin);
        printf("  Type:        0x%02X\n", manual_activation.header.type);
        printf("  Length:      0x%02X\n", manual_activation.header.length);
        
        printf("ActuatorID: %u\n", manual_activation.actuatorID);
        printf("Duration:   %u\n", manual_activation.duration);
    } else {
        printf("La cadena no tiene el mismo tamaño que la estructura protocol_manual_activation.\n");
    }

    return 0;
}