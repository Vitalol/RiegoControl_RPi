#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct protocol_header_str {
    uint8_t destination;
    uint8_t origin;
    uint8_t type;
    uint8_t lenght;
} __attribute__((__packed__)) protocol_header_str;

typedef struct scheduler_dates_t {
    uint32_t month_days;  // Wich days of the month
    uint8_t  week_days;   // Wich days of the week
    uint8_t  hour;        // At wich hour
    uint8_t  minute;      // At wich minute
} scheduler_dates_t;

typedef struct protocol_set_scheduler_str {
    protocol_header_str header;
    uint8_t             actuatorID;
    scheduler_dates_t   schedule;
} __attribute__((__packed__)) protocol_set_scheduler_str;


int main()
{
uint8_t bytes[] = {0x02, 0x00, 0x03, 0x08, 0x02, 0x1e, 0x00, 0x00, 0x00, 0x55, 0x11, 0x1e};

    // Estructura para copiar los bytes
    protocol_set_scheduler_str scheduler;

    // Copiar los bytes en la estructura
    memcpy(&scheduler, bytes, sizeof(protocol_set_scheduler_str));

    // Imprimir los valores copiados
    printf("actuatorID: %u\n", scheduler.actuatorID);
    printf("destination: %u\n", scheduler.header.destination);
    printf("origin: %u\n", scheduler.header.origin);
    printf("type: %u\n", scheduler.header.type);
    printf("lenght: %u\n", scheduler.header.lenght);
    printf("month_days: %u\n", scheduler.schedule.month_days);
    printf("week_days: %u\n", scheduler.schedule.week_days);
    printf("hour: %u\n", scheduler.schedule.hour);
    printf("minute: %u\n", scheduler.schedule.minute);


    return 0;
}