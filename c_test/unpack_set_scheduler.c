#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t length;
} __attribute__((__packed__)) protocol_header_str;

typedef struct scheduler_dates_t {
    uint32_t month_days;  // Wich days of the month
    uint8_t  week_days;   // Wich days of the week
    uint8_t  hour;        // At wich hour
    uint8_t  minute;      // At wich minute
    uint32_t duration;    // for how long
} __attribute__((__packed__)) scheduler_dates_t;

typedef struct protocol_set_scheduler_str {
    protocol_header_str header;
    uint8_t             actuatorID;
    scheduler_dates_t   schedule;
} __attribute__((__packed__)) protocol_set_scheduler_str;


int main() {
   
    uint8_t bytes[] = { 0x01, 0x00, 0x03, 0x08, 0x02, 0x00, 0x00, 0x00, 0x00, 0x2a, 0x0f, 0x1e, 0x0f, 0x00, 0x00, 0x00};

    if (sizeof(bytes) == sizeof(protocol_set_scheduler_str)) {
        protocol_set_scheduler_str set_scheduler;

        // Copiar los bytes en la estructura
        memcpy(&set_scheduler, bytes, sizeof(protocol_set_scheduler_str));

        // Imprimir los campos de la estructura
        printf("Header:\n");
        printf("  Destination: 0x%02X\n", set_scheduler.header.destination);
        printf("  Origin:      0x%02X\n", set_scheduler.header.origin);
        printf("  Type:        0x%02X\n", set_scheduler.header.type);
        printf("  Length:      0x%02X\n", set_scheduler.header.length);

        printf("ActuatorID:   %u\n", set_scheduler.actuatorID);
        printf("Month Days:   %u\n", set_scheduler.schedule.month_days);
        printf("Week Days:    %u\n", set_scheduler.schedule.week_days);
        printf("Hour:         %u\n", set_scheduler.schedule.hour);
        printf("Minute:       %u\n", set_scheduler.schedule.minute);
        printf("Duration:     %u\n", set_scheduler.schedule.duration);
    } else {
        printf("La cadena no tiene el mismo tamaño que la estructura protocol_set_scheduler_str.\n");
    }

    return 0;
}