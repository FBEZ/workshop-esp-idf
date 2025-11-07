---
title: "ESP-IDF Base - Esercizio 3.1"
date: "2025-11-12"
series: ["WS00A"]
series_order: 9
showAuthor: false
summary: "Creare un componente `led-toggle` e rifattorizzare l'esempio `hello_led`"
---

Questo esercizio prevede due obiettivi: 

1. Creare un componente `led-toggle`
2. Rifattorizzare l’esempio `hello_led` utilizzando il componente creato

## Creare un componente `led-toggle` (guidato)

Il primo compito è creare un componente `led-toggle`.

### Creare un nuovo componente

* Apri il progetto dell'esercizio 2.2 in VS Code
* Crea un nuovo componente: `> ESP-IDF: Create New ESP-IDF Component`
* Digita `led_toggle` nel campo di testo che appare in alto (vedi Fig.1)

{{< figure
default=true
src="/workshop-esp-idf/workshops/esp-idf-basic/assets/ass3_1_new_component.webp"
caption="Fig.1 - Creare un nuovo componente"

>}}

Il progetto conterrà ora la cartella `components` e tutti i file necessari:

```bash
.
└── hello_led/
    ├── components/
    │   └── led_toggle/
    │       ├── include/
    │       │   └── led_toggle.h
    │       ├── CMakeLists.txt
    │       └── led_toggle.c
    ├── main
    └── build
```

### Creare la funzione toggle

* Aggiungi l'interfaccia pubblica del tuo componente all’interno di `led_toggle.h`:

    ```c
    #include "driver/gpio.h"

    typedef struct {
        int gpio_nr;
        bool status;
    }led_gpio_t;

    esp_err_t led_config(led_gpio_t * led_gpio);
    esp_err_t led_drive(led_gpio_t * led_gpio, bool level);
    esp_err_t led_toggle(led_gpio_t * led_gpio);
    ```

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
`esp_err` è un enum (quindi un int) usato per restituire codici di errore. Puoi controllarne i valori [nella documentazione](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/error-codes.html).
Questo enum viene utilizzato anche con il logging e macro come `ESP_ERR_CHECK`, che troverai in quasi tutti gli esempi ESP-IDF.
{{< /alert >}}

* Aggiungi la direttiva REQUIRES al `CMakeList.txt` del componente `led_toggle`
   ```console
   idf_component_register(SRCS "led_toggle.c"
                    REQUIRES esp_driver_gpio
                    INCLUDE_DIRS "include")
   ```

* In `led_toggle.c`, implementa la logica del modulo:

    ```c
    #include <stdio.h>
    #include "led_toggle.h"
    #include "esp_err.h"

    esp_err_t led_config(led_gpio_t * led_gpio){

        gpio_config_t io_conf = {};
        io_conf.intr_type = GPIO_INTR_DISABLE;
        io_conf.mode = GPIO_MODE_OUTPUT;
        io_conf.pin_bit_mask =  (1ULL<<led_gpio->gpio_nr);
        io_conf.pull_down_en = 0;
        io_conf.pull_up_en = 0;
        return gpio_config(&io_conf);
    }

    esp_err_t led_drive(led_gpio_t * led_gpio,bool level){
        led_gpio->status = level;
        return gpio_set_level(led_gpio->gpio_nr, level); // accende il LED
    }

    esp_err_t led_toggle(led_gpio_t * led_gpio){
        //TBD
        return 0;
    }
    ```


* Ora nel `app_main` includi l'header appropriato
* configura la periferica (mediante funzione `config_led`)
* Testa che tutto funzioni correttamente attraverso la funzione `drive_led`


## Rifattorizzare il codice `hello_led`

Per questa seconda parte dell'esercizio dovrai:

1. Implementare la funzione `toggle_led`
2. Rifattorizzare il codice `hello_led` per utilizzare il componente appena creato.


## Conclusione

Ora puoi creare i tuoi componenti, rendendo il codice più facile da mantenere e condividere.
Nel prossimo esercizio affronterai un tipico problema di sviluppo e utilizzerai le competenze appena apprese.

<details>
<summary>Soluzione Esercizio</summary>

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
#include "led_toggle.h"

#define OUTPUT_LED GPIO_NUM_7

static const char* TAG = "main";



led_gpio_t my_led = {
    .gpio_nr = OUTPUT_LED,
    .status = false
};

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
    led_drive(&my_led,true);

    const char* resp_str = "{\"led\": \"on\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t led_off_handler(httpd_req_t *req)
{
    led_drive(&my_led,false);

    const char* resp_str = "{\"led\": \"off\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}


static esp_err_t led_toggle_handler(httpd_req_t *req)
{
    led_toggle(&my_led);

    const char* resp_str = "{\"led\": \"toggled\"}";
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

static const httpd_uri_t led_toggle_uri = {
    .uri       = "/led/toggle",
    .method    = HTTP_GET,
    .handler   = led_toggle_handler,
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
    led_config(&my_led);
    httpd_handle_t server = start_webserver();
    /* Registrazione URI/Handler */
    httpd_register_uri_handler(server,&hello_world_uri);
    httpd_register_uri_handler(server, &led_on_uri);
    httpd_register_uri_handler(server, &led_off_uri);
    httpd_register_uri_handler(server, &led_toggle_uri);
}
```
</details>

### Prossimo passo

> Prossimo esercizio → [Esercizio 3.2](../assignment-3-2/)

> Oppure [torna al menù di navigazione](../#agenda)