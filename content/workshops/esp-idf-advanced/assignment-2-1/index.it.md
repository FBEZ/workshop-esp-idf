---
title: "ESP-IDF Avanzato - Esercizio 2.1"
date: "2025-11-12"
series: ["WS00B"]
series_order: 7
showAuthor: false
summary: "Event loop: Gestire sensore di temperatura e allarme tramite eventi (guidato)"
---

In questo esercizio, separeremo il codice dell'allarme e della temperatura, utilizzando l'event loop di default. 

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Nel codice dell'esercizio precedente, abbiamo già utilizzando indirettamente questo event loop per catturare eventi MQTT e Wi-Fi.
{{< /alert >}}

## Obiettivi dell'esercizio

1. Creare gli eventi<br>

   * `TEMP_EVENT_BASE` - `temp_event_id`
   * `ALARM_EVENT_BASE` - `alarm_event_id_t`
2. Creare le funzioni handler<br>

   * `alarm_event_handler`
   * `temp_event_handler`
3. Registrare le funzioni handler
4. Creare i due timer<br>

   * `esp_timer_create`
   * `esp_timer_start_periodic`
5. Creare le funzioni callback dei timer per inviare l'evento ogni 5s e 200ms<br>

   * `temp_timer_callback`
   * `alarm_timer_callback`
6. Creare un loop di sleep infinito nel main

## Creare gli eventi

* Definisci le due basi degli eventi a livello globale (ossia fuori da qualsiasi funzione)

    ```c
    ESP_EVENT_DEFINE_BASE(TEMP_EVENT_BASE);
    ESP_EVENT_DEFINE_BASE(ALARM_EVENT_BASE);
    ```

* Definisci il loro `event_id` come `enum` che in questo caso contengono un solo valore.

    ```c
    typedef enum {
        TEMP_EVENT_MEASURE,
    } temp_event_id_t;

    typedef enum {
        ALARM_EVENT_CHECK,
    } alarm_event_id_t;
    ```

## Creare le funzioni handler

* Crea le due funzioni handler degli eventi che si occupano di inviare i dati sul canale MQTT.

    ```c
    static void temp_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {
        float temp;
        if (temperature_sensor_read_celsius(sensor, &temp) == ESP_OK) {
            cloud_manager_send_temperature(cloud, temp);
        } else {
            ESP_LOGW("APP", "Failed to read temperature");
        }
    }

    static void alarm_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {
        if (is_alarm_set(alarm)) {
            ESP_LOGI("APP", "ALARM ON!!");
            cloud_manager_send_alarm(cloud);
        }
    }
    ```

## Registrare le funzioni handler

* In `app_main` registra la due funzioni, specificando la base e l'id dell'evento a cui sono collegate:

```c
ESP_ERROR_CHECK(esp_event_handler_register(TEMP_EVENT_BASE, TEMP_EVENT_MEASURE, temp_event_handler, NULL));
ESP_ERROR_CHECK(esp_event_handler_register(ALARM_EVENT_BASE, ALARM_EVENT_CHECK, alarm_event_handler, NULL));
```

## Creare i timer

La vera fonte degli eventi in questo esercizio sono i timer. Dobbiamo quindi avviarne due, uno per l'allarme ed uno per la temperatura. 

* Creare ed avvia i timer per temperatura e allarme:

    ```c
    // Creare e avviare timer periodici (app_main)

    // Timer temperatura
        const esp_timer_create_args_t temp_timer_args = {
            .callback = &temp_timer_callback,
            .name = "temp_timer"
        };
        esp_timer_handle_t temp_timer;
        ESP_ERROR_CHECK(esp_timer_create(&temp_timer_args, &temp_timer));
        ESP_ERROR_CHECK(esp_timer_start_periodic(temp_timer, TEMPERATURE_MEAS_PERIOD_US));

    // Timer allarme
    const esp_timer_create_args_t alarm_timer_args = {
        .callback = &alarm_timer_callback,
        .name = "alarm_timer"
    };
    esp_timer_handle_t alarm_timer;
    ESP_ERROR_CHECK(esp_timer_create(&alarm_timer_args, &alarm_timer));
    ESP_ERROR_CHECK(esp_timer_start_periodic(alarm_timer, ALARM_CHECK_PERIOD_US));
    ```

Le due macro `ALARM_CHECK_PERIOD_US` e `TEMPERATURE_MEAS_PERIOD_US` possono essere aggiunte come define all’inizio del codice o come parametro del modulo.

* Per semplicità, definisci le due macro in `app_main.c`

    ```c
    #define TEMPERATURE_MEAS_PERIOD_US (5 * 1000000)
    #define ALARM_CHECK_PERIOD_US      (200 * 1000)
    ```

## Creare le funzioni callback dei timer

Nel codice precedente, abbiamo dato come `.callback` le funzioni `temp_timer_callback` e `alarm_timer_callback`.
Queste funzioni vengono chiamate quando il timer scade.

* Scrivi le funzioni callback per postare i relativi eventi

    ```c
    static void temp_timer_callback(void* arg) {
        esp_event_post(TEMP_EVENT_BASE, TEMP_EVENT_MEASURE, NULL, 0, 0);
    }

    static void alarm_timer_callback(void* arg) {
        esp_event_post(ALARM_EVENT_BASE, ALARM_EVENT_CHECK, NULL, 0, 0);
    }
    ```

L'event loop si occuperà di chiamare la funzione corretta quando l'evento viene attivato.

## Sleep nel main

L’ultima cosa da fare è lasciare che il main continui a girare mentre gli eventi vengono attivati. 

* Aggiungi un loop idle al `app_main`

    ```c
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
    ```

## Codice soluzione dell'esercizio

<details>
<summary>Mostra codice completo</summary>

```c
#include "cloud_manager.h"
#include "temperature_sensor.h"
#include "alarm.h"
#include "esp_log.h"
#include "esp_event.h"
#include "esp_timer.h"

#define TEMPERATURE_MEAS_PERIOD_US (5 * 1000000)
#define ALARM_CHECK_PERIOD_US      (200 * 1000)

ESP_EVENT_DEFINE_BASE(TEMP_EVENT_BASE);
ESP_EVENT_DEFINE_BASE(ALARM_EVENT_BASE);

static bool previous_alarm_set = false;

typedef enum {
    TEMP_EVENT_MEASURE,
} temp_event_id_t;

typedef enum {
    ALARM_EVENT_CHECK,
} alarm_event_id_t;

static temperature_sensor_t *sensor = NULL;
static alarm_t *alarm = NULL;
static cloud_manager_t *cloud = NULL;

static void temp_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {
    float temp;
    if (temperature_sensor_read_celsius(sensor, &temp) == ESP_OK) {
        cloud_manager_send_temperature(cloud, temp);
    } else {
        ESP_LOGW("APP", "Failed to read temperature");
    }
}

static void alarm_event_handler(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data) {

    bool alarm_state = is_alarm_set(alarm);
    if (alarm_state && !previous_alarm_set) {
        printf("ALARM ON!!\n");
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
    ESP_LOGI("APP", "Starting...");

    ESP_ERROR_CHECK(esp_event_loop_create_default());

    sensor = temperature_sensor_create();
    alarm = alarm_create();
    cloud = cloud_manager_create();

    printf("Connecting...\n");
    ESP_ERROR_CHECK(cloud_manager_connect(cloud));
    printf("Connected!\n");

    // Register event handlers
    ESP_ERROR_CHECK(esp_event_handler_register(TEMP_EVENT_BASE, TEMP_EVENT_MEASURE, temp_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(ALARM_EVENT_BASE, ALARM_EVENT_CHECK, alarm_event_handler, NULL));

    // Create and start periodic timers
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
    ESP_ERROR_CHECK(esp_timer_start_periodic(alarm_timer, ALARM_CHECK_PERIOD_US));

    // The main task can now just sleep
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    // Cleanup (unreachable in this example)
    cloud_manager_disconnect(cloud);
    cloud_manager_delete(cloud);
    temperature_sensor_delete(sensor);
    alarm_delete(alarm);
}
```

</details>

Puoi trovare l’intero progetto della soluzione nella cartella [assignment_2_1](/workshop/esp-idf-advanced/assets) del repository GitHub.

## Conclusione

L’utilizzo di un event loop separa la gestione dell’allarme e del sensore di temperatura. In questa esercizio, avremmo potuto ottenere lo stesso risultato usando le callback dei timer e evitando il sovraccarico dell’event loop. In generale però, gli eventi possono provenire da fonti diverse e l’event loop offre un approccio unificato per separare la logica dell’applicazione.


### Prossimo passo

> Se hai ancora tempo: [Esercizio 2.2](../assignment-2-2). 

Nell'esercizio 2.2 si aggiunge un’ulteriore fonte di evento attivata stavolta da un GPIO.

> Altrimenti: [Lezione 3](../lecture-3/)

> Oppure [torna al menù di navigazione](../#agenda)