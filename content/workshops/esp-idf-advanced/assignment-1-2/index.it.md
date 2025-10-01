---
title: "ESP-IDF Avanzato - Esercizio 1.2"
date: "2025-11-12"
series: ["WS00B"]
series_order: 4
showAuthor: false
summary: "Creare un componente `cloud_manager` e rifattorizzare il codice per usarlo."
---

In questa seconda parte, separeremo la logica di connessione dalla funzione principale. Il vantaggio di questo approccio è che rende possibile cambiare in maniera trasparente il tipo di connessione (ad esempio passando da MQTTS a HTTP) senza dover modificare la logica del `main`. 

In questo compito, rifattorizzeremo il codice di connessione a Wi-Fi e MQTT per adattarlo a un nuovo componente.

## Obiettivi dell'esercizio

Crea un componente `cloud_manager` con

* La seguente interfaccia pubblica:
    ```c
    cloud_manager_t *cloud_manager_create(void);
    esp_err_t cloud_manager_connect(cloud_manager_t *manager);
    esp_err_t cloud_manager_disconnect(cloud_manager_t *manager);
    esp_err_t cloud_manager_send_temperature(cloud_manager_t *manager, float temp);
    esp_err_t cloud_manager_send_alarm(cloud_manager_t *manager);
    void cloud_manager_delete(cloud_manager_t *manager);
    ```
* I seguenti parametri da impostare tramite `menuconfig`:
    * URL del Broker (spostalo dal main al componente `cloud_manager`)
    * Il canale su cui viene pubblicata la temperatura (`sensor/temperature` di default)
    * Il canale su cui viene pubblicato l’allarme (`sensor/alarm` di default)

## Traccia della soluzione

### Crea un nuovo componente e completa `cloud_manager.h`

   * Aggiungi i metodi suggeriti<br>
   * Aggiungi una dichiarazione opaca `typedef struct cloud_manager_t cloud_manager_t;`

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
In `cloud_manager.h` devi importare solo `esp_err.h`
{{< /alert >}}

### Completa `cloud_manager.c`<br>

   * Implementa `cloud_manager_t` come: <br>

     ```c
       struct cloud_manager_t {
       esp_mqtt_client_handle_t client;
       esp_mqtt_client_config_t mqtt_cfg;
       };
     ```
   * In `cloud_manager_create` ritorna semplicemente l’oggetto inizializzato.
   * In `cloud_manager_connect` inizializza la connessione. Puoi usare la funzione `example_connect`.
* Aggiungi quanto segue al `CMakeList.txt` del componente `cloud_manager`<br>

   ```bash
    PRIV_REQUIRES mqtt nvs_flash esp_netif protocol_examples_common
   ```
* In `app_main.c`<br>

   * Inizializza e connetti il `cloud_manager`

     ```c
     cloud_manager_t *cloud = cloud_manager_create();
     ESP_ERROR_CHECK(cloud_manager_connect(cloud));
     ```
   * Chiama le funzioni di publishing nella posizione appropriata

## Soluzione dell'esercizio

<details>
<summary>Mostra il codice</summary>

#### `cloud_manager.h`

```c
#pragma once

#include "esp_err.h"

typedef struct cloud_manager_t cloud_manager_t;

/**
 * @brief Crea una nuova istanza del cloud manager
 */
cloud_manager_t *cloud_manager_create(void);

/**
 * @brief Connette il cloud manager (avvia MQTT)
 */
esp_err_t cloud_manager_connect(cloud_manager_t *manager);

/**
 * @brief Disconnette il cloud manager
 */
esp_err_t cloud_manager_disconnect(cloud_manager_t *manager);

/**
 * @brief Invia un valore di temperatura al cloud
 */
esp_err_t cloud_manager_send_temperature(cloud_manager_t *manager, float temp);

/**
 * @brief Invia un evento di allarme al cloud
 */
esp_err_t cloud_manager_send_alarm(cloud_manager_t *manager);

/**
 * @brief Libera la memoria
 */
void cloud_manager_delete(cloud_manager_t *manager);
```

#### `cloud_manager.c`

```c
#include <stdio.h>
#include <string.h>
#include "cloud_manager.h"
#include "esp_log.h"
#include "mqtt_client.h"
#include "nvs_flash.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"

static const char *TAG = "cloud_manager";

struct cloud_manager_t {
    esp_mqtt_client_handle_t client;
    esp_mqtt_client_config_t mqtt_cfg;
};

// Event handler for MQTT
static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;

    switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG, "Connesso al broker MQTT");
        esp_mqtt_client_subscribe(client, CONFIG_TEMPERATURE_CHANNEL, 0);
        esp_mqtt_client_subscribe(client, CONFIG_ALARM_CHANNEL, 0);
        break;

    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGI(TAG, "Disconnesso dal broker MQTT");
        break;

    case MQTT_EVENT_PUBLISHED:
        ESP_LOGI(TAG, "Messaggio pubblicato (msg_id=%d)", event->msg_id);
        break;

    case MQTT_EVENT_ERROR:
        ESP_LOGE(TAG, "MQTT_EVENT_ERROR");
        break;

    default:
        break;
    }
}

cloud_manager_t *cloud_manager_create(void)
{
    cloud_manager_t *manager = calloc(1, sizeof(cloud_manager_t));
    if (!manager) return NULL;


    manager->mqtt_cfg = (esp_mqtt_client_config_t){
        .broker.address.uri = CONFIG_BROKER_URL,
    };

    return manager;
}

esp_err_t cloud_manager_connect(cloud_manager_t *manager)
{

    if(manager == NULL){return ESP_ERR_INVALID_ARG;}
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    manager->client = esp_mqtt_client_init(&manager->mqtt_cfg);
    esp_mqtt_client_register_event(manager->client, ESP_EVENT_ANY_ID, mqtt_event_handler, manager);
    ESP_ERROR_CHECK(example_connect());
    return esp_mqtt_client_start(manager->client);
}

esp_err_t cloud_manager_disconnect(cloud_manager_t *manager)
{
    if (!manager || !manager->client) return ESP_ERR_INVALID_ARG;
    return esp_mqtt_client_stop(manager->client);
}

esp_err_t cloud_manager_send_temperature(cloud_manager_t *manager, float temp)
{
    if (!manager || !manager->client) return ESP_ERR_INVALID_ARG;

    char payload[64];
    snprintf(payload, sizeof(payload), "%.2f", temp);
    ESP_LOGI(TAG, "Temperatura: %.2f °C", temp);
    int msg_id = esp_mqtt_client_publish(manager->client, CONFIG_TEMPERATURE_CHANNEL, payload, 0, 1, 0);
    return msg_id >= 0 ? ESP_OK : ESP_FAIL;
}

esp_err_t cloud_manager_send_alarm(cloud_manager_t *manager)
{
    if (!manager || !manager->client) return ESP_ERR_INVALID_ARG;

    const char *alarm_payload = "ALARM ON!";
    int msg_id = esp_mqtt_client_publish(manager->client, CONFIG_ALARM_CHANNEL, alarm_payload, 0, 1, 0);
    return msg_id >= 0 ? ESP_OK : ESP_FAIL;
}

void cloud_manager_delete(cloud_manager_t *manager)
{
        if (manager) {
        free(manager);
    }

}
```

#### `Kconfig`

```bash
menu "Configurazione Cloud MQTT"

    config BROKER_URL
        string "URL del Broker"
        default "mqtt://test.mosquitto.org/"
        help
            URL del broker a cui connettersi
    config TEMPERATURE_CHANNEL
        string "Canale MQTT per pubblicare la temperatura"
        default "/sensor/temperature"
        help
            Il canale nel broker MQTT dove viene pubblicata la temperatura
    config ALARM_CHANNEL
        string "Canale MQTT per pubblicare l'allarme"
        default "/sensor/alarm"
        help
            Il canale nel broker MQTT dove viene pubblicato l'allarme

endmenu
```

</details>

Puoi trovare l’intero progetto soluzione nella cartella [assignment_1_2](/workshop/esp-idf-advanced/assets) della repository GitHub.

> Prossimo passo: [Esercizio 1.3](../assignment-1-3/)

> Oppure [torna al menù di navigazione](../#agenda)