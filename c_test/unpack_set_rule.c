#include <stdio.h>
#include <stdint.h>
#include <string.h>


typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t length;
} __attribute__((__packed__)) protocol_header_str;

typedef struct rule_str {
    uint8_t type;
    float   value;
    uint8_t rule;  // 0 Larger or equal 1 Le
} __attribute__((__packed__)) rule_str;

typedef struct protocol_set_rule_str {
    protocol_header_str header;
    uint8_t             actuatorID;
    rule_str            rule;
} __attribute__((__packed__)) protocol_set_rule_str;

int main() {
     uint8_t bytes[] = {0x01, 0x00, 0x07, 0x0a, 0x02, 0x01, 0x00, 0x00, 0x70, 0x41, 0x01};


    if (sizeof(bytes) == sizeof(protocol_set_rule_str)) {
        protocol_set_rule_str set_rule;

        // Copiar los bytes en la estructura
        memcpy(&set_rule, bytes, sizeof(protocol_set_rule_str));

        // Imprimir los campos de la estructura
        printf("Header:\n");
        printf("  Destination: 0x%02X\n", set_rule.header.destination);
        printf("  Origin:      0x%02X\n", set_rule.header.origin);
        printf("  Type:        0x%02X\n", set_rule.header.type);
        printf("  Length:      0x%02X\n", set_rule.header.length);

        printf("ActuatorID: %u\n", set_rule.actuatorID);
        printf("Rule Type:  0x%02X\n", set_rule.rule.type);
        printf("Value:      %f\n", set_rule.rule.value);
        printf("Rule:       0x%02X\n", set_rule.rule.rule);
    } else {
        printf("La cadena no tiene el mismo tamaño que la estructura protocol_set_rule_str.\n");
    }

    return 0;
}