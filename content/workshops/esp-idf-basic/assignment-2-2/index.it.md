---
title: "ESP-IDF Base - Esercizio 2.2"
date: "2025-11-12"
series: ["WS00A"]
series_order: 6
showAuthor: false
summary: "Aggiungere ulteriori route al server HTTP per controllare il led da remoto"
---

Il secondo esercizio consiste nell’aggiungere le seguenti route al server HTTP che abbiamo creato nell'esercizio precedente:

* `GET /led/on` → accende il LED e restituisce JSON {"led": "on"}
* `GET /led/off` → spegne il LED e restituisce JSON {"led": "off"}
<!-- * `POST /led/blink` → accetta JSON `{ "times": int, "interval_ms": int }` per far lampeggiare il LED il numero di volte specificato con l’intervallo indicato, e restituisce JSON `{"blink": "done"}` -->

## Traccia della soluzione

Per controllare il led, puoi usare il codice dell'esercizio 1.2, riportato qui per convenienza. 

* Includi l'header opportuno:

  ```c
  #include "driver/gpio.h"
  ```
* Specifica il pin da usare (a seconda della scheda che stai usando)

  ```c
   #define OUTPUT_LED GPIO_NUM_7
  ```
* Crea una funzione di configurazione (da chiamare dalla funzione `app_main`)

  ```c
   static void configure_led(void)
   {
       ESP_LOGI(TAG, "LED Configured!\n");
       gpio_reset_pin(OUTPUT_LED);
       /* Set the GPIO as push/pull output */
       gpio_set_direction(OUTPUT_LED, GPIO_MODE_OUTPUT);
   }
  ```
* Crea la funzione per pilotare il led:
    ```c
    static void led_control(int level){
        gpio_set_level(OUTPUT_LED, level);
    }
    ```

## Codice della soluzione

<details>  
<summary>Mostra codice soluzione</summary>

```c
#include <stdio.h>
#define ESP_WIFI_SSID "TEST_WORKSHOP"
#define ESP_WIFI_PASS "test_esp"
#define ESP_WIFI_CHANNEL 1
#define MAX_STA_CONN 2
#include "esp_wifi.h"
#include "string.h"
#include "esp_log.h"
#include "esp_http_server.h"
#include "driver/gpio.h"

#define OUTPUT_LED GPIO_NUM_7

static const char* TAG = "main";

static void configure_led(void)
{
  ESP_LOGI(TAG, "LED Configurato!\n");
  gpio_reset_pin(OUTPUT_LED);
  /* Imposta il GPIO come output push/pull */
  gpio_set_direction(OUTPUT_LED, GPIO_MODE_OUTPUT);
}

static void led_control(int level){
        gpio_set_level(OUTPUT_LED, level);
    }

static esp_err_t hello_get_handler(httpd_req_t *req)
{
    const char* resp_str = "<h1>Hello World</h1>";
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

/* Handler definitions */

static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                  int32_t event_id, void* event_data){
    printf("Evento n°: %ld!\n", event_id);
}


static esp_err_t led_on_handler(httpd_req_t *req)
{
    led_control(1);

    const char* resp_str = "{\"led\": \"on\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t led_off_handler(httpd_req_t *req)
{
    led_control(0);

    const char* resp_str = "{\"led\": \"off\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

/* URI definitions */

static const httpd_uri_t hello_world_uri= {
    .uri       = "/",               
    .method    = HTTP_GET,          
    .handler   = hello_get_handler, 
    .user_ctx  = NULL               
};

static const httpd_uri_t led_on_uri = {
    .uri       = "/led/on",
    .method    = HTTP_GET,
    .handler   = led_on_handler,
    .user_ctx  = NULL
};

static const httpd_uri_t led_off_uri = {
    .uri       = "/led/off",
    .method    = HTTP_GET,
    .handler   = led_off_handler,
    .user_ctx  = NULL
};

void wifi_init_softap(){
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_ap();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT(); // sempre iniziare da qui

    esp_wifi_init(&cfg);

    esp_event_handler_instance_register(WIFI_EVENT,
                                        ESP_EVENT_ANY_ID,
                                        &wifi_event_handler,
                                        NULL,
                                        NULL);

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = ESP_WIFI_SSID,
            .ssid_len = strlen(ESP_WIFI_SSID),
            .channel = ESP_WIFI_CHANNEL,
            .password = ESP_WIFI_PASS,
            .max_connection = MAX_STA_CONN,
            .authmode = WIFI_AUTH_WPA2_PSK,
            .pmf_cfg = {
                .required = true,
            },
        },
    };

    esp_wifi_set_mode(WIFI_MODE_AP);
    esp_wifi_set_config(WIFI_IF_AP, &wifi_config);
    esp_wifi_start();

    ESP_LOGI(TAG, "wifi_init_softap completata. SSID:%s password:%s canale:%d",
             ESP_WIFI_SSID, ESP_WIFI_PASS, ESP_WIFI_CHANNEL);
}

httpd_handle_t start_webserver() {
    httpd_handle_t server = NULL;
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    if (httpd_start(&server, &config) == ESP_OK) {
        ESP_LOGI(TAG, "Server avviato con successo, registrazione degli handler URI...");
        return server;
    }

    ESP_LOGE(TAG, "Impossibile avviare il server");
    return NULL;
}


void app_main(void)
{
    wifi_init_softap();
    configure_led();
    httpd_handle_t server = start_webserver();

    /* Registrazione URI/Handler */
    httpd_register_uri_handler(server,&hello_world_uri);
    httpd_register_uri_handler(server, &led_on_uri);
    httpd_register_uri_handler(server, &led_off_uri);
}
```

</details>

### Conclusione

Ora abbiamo una chiara panoramica di come collegare le richieste ricevute tramite REST API al controllo fisico del dispositivo.
Nell’ultimo esercizio del workshop (il 3.3) lavorerai su un’applicazione simile ma più complessa. 

### Prossimo passo

Se hai ancora tempo, puoi provare il prossimo esercizio opzionale.

> Prossimo esercizio (opzionale) → [Esercizio 2.3](../assignment-2-3/)

Altrimenti, puoi passare alla terza lezione.

> Prossima lezione → [Lezione 3](../lecture-3/)

> Oppure [torna al menù di navigazione](../#agenda)