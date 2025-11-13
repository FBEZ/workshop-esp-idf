---
title: "ESP-IDF Base - Esercizio 2.1"
date: "2025-11-12"
series: ["WS00A"]
series_order: 5
showAuthor: false
summary: "Far partire una soft-AP e un server HTTP (guidato)."
---

## Passi dell'esercizio 

1. Creare un nuovo progetto da template
2. Avviare un soft-AP
3. Avviare un server HTTP
4. Connettersi al soft-AP con uno smartphone

## Creare un nuovo progetto a partire da template

Negli ultimi esercizi, abbiamo creato un progetto a partire da un esempio. Questa volta creeremo invece un progetto a partire da un template vuoto.

* Apri VS Code
* `> ESP-IDF: Create Project from Extension Template`
* Nel menù a tendina che appare &rarr; `Choose a container directory`
* Scegli una cartella nella quale verrà creata la cartella del progetto
* Nel menù a tendina che appare &rarr; `template-app`
* Scegli il target (`esp32c3`) e seleziona la porta, come fatto negli esercizi precedenti.

Nella cartella che hai selezionato, sono ora presenti i seguenti file di progetto

```console
.
|-- CMakeLists.txt
|-- README.md
`-- main
    |-- CMakeLists.txt
    `-- main.c
```

Come vedi, la struttura è molto più semplice che nel caso dell'esempio `blink` o `hello_world`. 

## Avviare un soft-AP

Per mantenere l'esercizio il più semplice possibile, in questo tutorial le credenziali dell’access point (AP) saranno definite nel codice.
Non useremo quindi la memoria non volatile (NVS), che viene invece normalmente utilizzata nelle applicazioni Wi-Fi per memorizzare credenziali e dati di calibrazione.

NVS è abilitata per impostazione predefinita. Per evitare avvisi ed errori, dobbiamo disabilitarla tramite `menuconfig`.

### Disabilitare NVS

Per disabilitare NVS, accediamo a `menuconfig` e cerchiamo l’opzione `NVS`:

* `> ESP-IDF: SDK Configuration Editor (menuconfig)` → `NVS`
* Togli la selezione a `PHY` e `Wi-Fi`, come indicato in Fig.1. 

{{< figure
default=true
src="/workshop-esp-idf/workshops/esp-idf-basic/assets/ass_2_1_disable_nvs.webp"
height=500
caption="Fig. 1 - Opzioni NVS da disabilitare"

>}}
* Clicca su `Save`
* Chiudi il tab di `menuconfig`

### Definire i parametri del soft-AP

Spostiamoci ora sul file `main/main.c`. 

Imposteremo i parametri necessari per il soft-AP come `define` all'inizio del sorgente:

```c
#define ESP_WIFI_SSID "<NOMEUTENTE_esp_test>"
#define ESP_WIFI_PASS "test_esp"
#define ESP_WIFI_CHANNEL 1
#define MAX_STA_CONN 2
```

Per evitare sovrapposizioni con gli altri partecipanti, __crea un nome unico per l'SSID__. 

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Questo **non** è il metodo raccomandato per memorizzare le credenziali.
È preferibile conservarle in modo sicuro in NVS o gestirle tramite configurazione usando `menuconfig`.
{{< /alert >}}

### Inizializzare lo stack IP e l’Event Loop

Il componente Wi-Fi di Espressif si basa su un [event loop](https://it.wikipedia.org/wiki/Event_loop) per gestire eventi asincroni.
Per avviare il soft-AP, dobbiamo:

1. Includere `esp_wifi.h`, `string.h` ed `esp_log.h`
2. Inizializzare lo stack IP (`esp_netif_init` e `esp_netif_create_default_wifi_ap`)
3. Avviare il [loop degli eventi predefinito](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_event.html#default-event-loop)
4. Creare e registrare una funzione di gestione eventi.

Per mantenere il codice ordinato, racchiuderemo tutto nella funzione `wifi_init_softap`:

```c
#include "esp_wifi.h"
#include "string.h"
#include "esp_log.h"
// ...

void wifi_init_softap()
{
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
```

### Registrare le funzioni di gestione degli eventi per il soft-AP

* Crea una funzione per gestire gli eventi Wi-Fi<br>
  _Siccome è usata da `wifi_init_softap`, questa funzione va definita prima_

```c
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                  int32_t event_id, void* event_data){
    printf("Evento n°: %ld!\n", event_id);
}
```
* Chiama la funzione `wifi_init_softap()` all'interno di `app_main()`<br>
   ```c
   void app_main(void)
    {
        wifi_init_softap();
    }
   ```
* `> ESP-IDF: Build, Flash and Start a Monitor on Your Device`

Dovresti vedere comparire diversi numeri evento nel terminale.

```console
[...]
I (576) wifi:Init max length of beacon: 752/752
Evento n°: 43!
I (576) esp_netif_lwip: DHCP server started on interface WIFI_AP_DEF with IP: 192.168.4.1
Evento n°: 12!
I (586) main: wifi_init_softap completata. SSID:TEST_WORKSHOP password:test_esp canale:1
I (596) main_task: Returned from app_main()
```

## Connettersi al soft-AP con uno smartphone

Prendi il tuo smartphone, apri la lista delle reti Wi-Fi e seleziona l’SSID che hai creato all'inizio (Fig. 2).

{{< figure
default=true
src="/workshop-esp-idf/workshops/esp-idf-basic/assets/ass_2_1_ap_list.webp"
height=500
caption="Fig. 2 - Elenco degli Access Point"
>}}

Nel terminale dovrebbe comparire `Evento n°: 14!`, che corrisponde a `WIFI_EVENT_AP_STACONNECTED`. 

```console
I (7146) wifi:new:<1,0>, old:<1,1>, ap:<1,1>, sta:<255,255>, prof:1, snd_ch_cfg:0x0
I (7146) wifi:station: ba:fa:31:4c:4f:3a join, AID=1, bgn, 20
Evento n°: 43!
Evento n°: 14!
```
Per verificare la corrispondenza tra numero e codice, puoi fare riferimento al codice su [GitHub](https://github.com/espressif/esp-idf/blob/c5865270b50529cd32353f588d8a917d89f3dba4/components/esp_wifi/include/esp_wifi_types_generic.h#L964). Ricorda che i valori delle `enum` partono da 0. 

I codici che vedi, indicato che una stazione (cioè il tuo smartphone) si è connessa al soft-AP (cioè al modulo Espressif).

## Avviare un server HTTP

La libreria HTTP server dell'ESP-IDF si chiama `esp_http_server`.
Per utilizzarla, è necessario includerla e configurare il server.

### Includere la libreria

1. Includi l’header `esp_http_server.h`:

   ```c
   #include "esp_http_server.h"
   ```
2. Per poter usare la libreria dei log (`ESP_LOGI`), definiamo la stringa TAG:
   ```c
   static const char* TAG = "main";
   ```
<!-- 
1. Aggiungi `esp_http_server` alla lista `PRIV_REQUIRES` nel tuo `CMakeLists.txt`, in modo che il sistema di build includa i componenti necessari.

```cmake
idf_component_register(SRCS "blink_example_main.c"
                       PRIV_REQUIRES esp_wifi esp_http_server esp_driver_gpio
                       INCLUDE_DIRS ".")
``` -->

### Configurare il server HTTP

* Creiamo una funzione per l’inizializzazione del server:

    ```c
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
    ```

* Nella funzione `app_main`, avviamo il server:

    ```c
    httpd_handle_t server = start_webserver();
    ```

### Gestione delle URI HTTP

Quando un utente visita la route `/`, vogliamo restituire una semplice pagina HTML. 

* Registriamo la route con `httpd_register_uri_handler`:

    ```c
    httpd_register_uri_handler(server,&hello_world_uri);
    ```

* Indichiamo la struttura `httpd_uri_t` che definisce le proprietà della route:

    ```c
    static const httpd_uri_t hello_world_uri= {
        .uri       = "/",               
        .method    = HTTP_GET,          
        .handler   = hello_get_handler, 
        .user_ctx  = NULL               
    };
    ```
* Specifichiamo la funzione handler che restituisce la pagina HTML

    ```c
    static esp_err_t hello_get_handler(httpd_req_t *req)
    {
        const char* resp_str = "<h1>Hello World</h1>";
        httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
        return ESP_OK;
    }
    ```

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Anche in questo caso, l'ordine in cui dovrai scrivere le funzioni è inverso, ossia prima la `hello_get_handler` e ultima la `httpd_register_uri_handler`.
In alternativa, puoi definire la firma di queste funzioni in cima al file `main.c`.
{{< /alert >}}


### Connessione al server

Il modulo Espressif fa da AP e ha un suo indirizzo, solitamente `192.168.4.1`. Vogliamo ora collegarci a questo indirizzo (e alla sua route `/`) per vedere la pagina HTML che abbiamo creato nella funzione `httpd_resp_send`. 

* Verifica l'indirizzo dell'AP. Puoi farlo cercando nel terminale, la riga seguente:

    ```bash
    I (766) esp_netif_lwip: DHCP server started on interface WIFI_AP_DEF with IP: 192.168.4.1
    ```
* Apri il browser sul dispositivo connesso e inserisci l’indirizzo IP trovato al punto precedente.
  
Dovresti vedere la pagina HTML mostrata in Fig.3, generata dalla funzione `hello_get_handler`.

{{< figure
default=true
src="/workshop-esp-idf/workshops/esp-idf-basic/assets/ass_2_1_result.webp"
height=100
caption="Fig.3 – Pagina HTML visualizzata"

>}}

## Codice dell’esercizio

<details>
<summary>Mostra soluzione</summary>

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


static const char* TAG = "main";

static esp_err_t hello_get_handler(httpd_req_t *req)
{
    const char* resp_str = "<h1>Hello World</h1>";
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}


static const httpd_uri_t hello_world_uri= {
    .uri       = "/",               
    .method    = HTTP_GET,          
    .handler   = hello_get_handler, 
    .user_ctx  = NULL               
};


static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                  int32_t event_id, void* event_data){
    printf("Evento n°: %ld!\n", event_id);
}

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
    httpd_handle_t server = start_webserver();
    httpd_register_uri_handler(server,&hello_world_uri);
}

```

</details>

## Conclusione

Ora sei in grado di configurare un dispositivo Espressif in modalità Soft-AP o STA e creare un server HTTP in grado di restituire contenuti HTML. 

Allo stesso modo puoi anche restituire risposte JSON per una REST API, come vedremo negli esercizi successivi. 

### Passaggio successivo

> Prossimo esercizio: [Esercizio 2.2](../assignment-2-2/)

> Oppure [torna al menù di navigazione](../#agenda)