---
title: "ESP-IDF Avanzato - Esercizio  2.2"
date: "2025-08-05"
series: ["WS00B"]
series_order: 8
showAuthor: false
summary: "Event loop: aggiungere un evento GPIO esterno"
---

In questo esercizio estenderai la funzionalità dell'Esercizio 2.1 introducendo una sorgente di eventi aggiuntiva: quando viene premuto **GPIO9**, un evento "alarm" viene inviato al sistema.

Il codice per rilevare la pressione di un GPIO è fornito di seguito.

## Obiettivi dell'esercizio

* Integrare la logica aggiuntiva nell'event loop esistente.
* Usare lo stesso `ALARM_EVENT_BASE` già utilizzato per il trigger dell'allarme.
* Creare un nuovo event_id `ALARM_EVENT_BUTTON` per differenziarlo da `ALARM_EVENT_CHECK`.


## Suggerimenti

* Esiste una versione alternativa di `esp_event_post` chiamata `esp_event_isr_post`.

### Codice per leggere il GPIO
```c
#include "driver/gpio.h"
#include "esp_attr.h"
#include "esp_log.h"

#define GPIO_INPUT_IO_9    9
#define ESP_INTR_FLAG_DEFAULT 0

static const char *TAG = "example";

// ISR handler
static void gpio_isr_handler(void* arg) {
    uint32_t gpio_num = (uint32_t) arg;
    ESP_EARLY_LOGI(TAG, "GPIO[%d] interrupt triggered", gpio_num);
}

void app_main(void)
{
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_NEGEDGE,      // Falling edge interrupt
        .mode = GPIO_MODE_INPUT,             // Set as input mode
        .pin_bit_mask = (1ULL << GPIO_INPUT_IO_9),
        .pull_up_en = GPIO_PULLUP_ENABLE,    // Enable pull-up
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
    };
    gpio_config(&io_conf);

    // Install GPIO ISR service
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    // Hook ISR handler for specific GPIO pin
    gpio_isr_handler_add(GPIO_INPUT_IO_9, gpio_isr_handler, (void*) GPIO_INPUT_IO_9);

    ESP_LOGI(TAG, "GPIO 9 configurato come input con interrupt su fronte di discesa");
}
```

## Codice soluzione dell'Esercizio

<details>
<summary>Mostra il codice completo</summary>

```c
#include "cloud_manager.h"
#include "temperature_sensor.h"
#include "alarm.h"
#include "esp_log.h"
#include "esp_event.h"
#include "esp_timer.h"
#include "driver/gpio.h"
#include "esp_attr.h"

#define TEMPERATURE_MEAS_PERIOD_US (5 * 1000000)
#define ALARM_CHECK_PERIOD_US      (200 * 1000)

#define GPIO_INPUT_IO_9    9
#define ESP_INTR_FLAG_DEFAULT 0


static const char *TAG = "assignment2_2";

// EVENTI
ESP_EVENT_DEFINE_BASE(TEMP_EVENT_BASE);
ESP_EVENT_DEFINE_BASE(ALARM_EVENT_BASE);

static bool previous_alarm_set = false;

typedef enum {
    TEMP_EVENT_MEASURE,
} temp_event_id_t;

typedef enum {
    ALARM_EVENT_CHECK,
    ALARM_EVENT_BUTTON
} alarm_event_id_t;


// GPIO

// ISR handler
static void gpio_isr_handler(void* arg) {
    uint32_t gpio_num = (uint32_t) arg;
    // Ora che pubblichiamo l'evento, rimuoviamo il log:
    // Non è consigliato fare log o print dentro una ISR
    //
    // ESP_EARLY_LOGI(TAG, "GPIO[%d] interrupt triggered", gpio_num);
    esp_event_isr_post(ALARM_EVENT_BASE, ALARM_EVENT_BUTTON, NULL, 0, 0);
}

static temperature_sensor_t *sensor = NULL;
static alarm_t *alarm = NULL;
static cloud_manager_t *cloud = NULL;

static void temp_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {
    float temp;
    if (temperature_sensor_read_celsius(sensor, &temp) == ESP_OK) {
        cloud_manager_send_temperature(cloud, temp);
    } else {
        ESP_LOGW("APP", "Impossibile leggere la temperatura");
    }
}

static void alarm_event_button_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {

    ESP_LOGI("APP", "ALLARME ATTIVO!!");
    cloud_manager_send_alarm(cloud);

}


static void alarm_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {

    bool alarm_state = is_alarm_set(alarm);
    if (alarm_state && !previous_alarm_set) {
        ESP_LOGI("APP", "ALLARME ATTIVO!!");
        cloud_manager_send_alarm(cloud);
    }
    previous_alarm_set = alarm_state;
}

static void temp_timer_callback(void* arg) {
    esp_event_post(TEMP_EVENT_BASE, TEMP_EVENT_MEASURE, NULL, 0, 0);
}

static void alarm_timer_callback(void* arg) {
    esp_event_post(ALARM_EVENT_BASE, ALARM_EVENT_CHECK, NULL, 0, 0);
}

void app_main(void)
{
    ESP_LOGI("APP", "Avvio...");

    ESP_ERROR_CHECK(esp_event_loop_create_default());

    sensor = temperature_sensor_create();
    alarm = alarm_create();
    cloud = cloud_manager_create();

    ESP_LOGI("APP", "Connessione in corso...");
    ESP_ERROR_CHECK(cloud_manager_connect(cloud));
    ESP_LOGI("APP", "Connesso!");

    // Registrazione degli handler degli eventi
    ESP_ERROR_CHECK(esp_event_handler_register(TEMP_EVENT_BASE, TEMP_EVENT_MEASURE, temp_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(ALARM_EVENT_BASE, ALARM_EVENT_CHECK, alarm_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(ALARM_EVENT_BASE, ALARM_EVENT_BUTTON, alarm_event_button_handler, NULL));

    // Creazione e avvio dei timer periodici
    const esp_timer_create_args_t temp_timer_args = {
        .callback = &temp_timer_callback,
        .name = "temp_timer"
    };
    esp_timer_handle_t temp_timer;
    ESP_ERROR_CHECK(esp_timer_create(&temp_timer_args, &temp_timer));
    ESP_ERROR_CHECK(esp_timer_start_periodic(temp_timer, TEMPERATURE_MEAS_PERIOD_US));

    const esp_timer_create_args_t alarm_timer_args = {
        .callback = &alarm_timer_callback,
        .name = "alarm_timer"
    };
    esp_timer_handle_t alarm_timer;
    ESP_ERROR_CHECK(esp_timer_create(&alarm_timer_args, &alarm_timer));


    // GPIO

     gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_NEGEDGE,      // Falling edge interrupt
        .mode = GPIO_MODE_INPUT,             // Set as input mode
        .pin_bit_mask = (1ULL << GPIO_INPUT_IO_9),
        .pull_up_en = GPIO_PULLUP_ENABLE,    // Enable pull-up
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
    };
    gpio_config(&io_conf);

    // Installazione del servizio ISR per GPIO
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    // Collegamento dell'handler ISR per il pin specifico
    gpio_isr_handler_add(GPIO_INPUT_IO_9, gpio_isr_handler, (void*) GPIO_INPUT_IO_9);

    // Il task principale può ora dormire
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    // Pulizia (non raggiungibile in questo esempio)
    cloud_manager_disconnect(cloud);
    cloud_manager_delete(cloud);
    temperature_sensor_delete(sensor);
    alarm_delete(alarm);
}
```

</details>

Puoi trovare l'intero progetto della soluzione nella cartella [assignment_2_2](/workshop/esp-idf-advanced/assets/assignment_2_2) sul repository GitHub.

### Prossimo passo

> Prossimo passo: [Lezione 3](../lecture-3/)

> Oppure [torna al menù di navigazione](../#agenda)