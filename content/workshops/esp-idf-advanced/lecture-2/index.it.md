---
title: "ESP-IDF Avanzato - Lezione 2"
date: "2025-11-12"
series: ["WS00B"]
series_order: 6
showAuthor: false
summary: "In questo articolo esploriamo l'event loop. Ne esaminiamo il funzionamento, evidenziamo i vantaggi, spieghiamo come viene utilizzato all'interno di ESP-IDF."
---

## Introduzione

Nei sistemi embedded può essere particolarmente complesso gestire eventi asincroni come la connettività Wi-Fi, Bluetooth o i timer. 

L'event loop aiuta il disaccoppiamento delle parti del firwmare, permettendo ai vari componenti di definire eventi e registrare handler che rispondono quando questi eventi si verificano. 

L'event loop favorisce quindi uno stile di programmazione **event-driven** pulito. 

### Quando è utile un event loop

Gli event loop sono essenziali per gestire eventi asincroni in modo modulare e strutturato. 

Consideriamo un firmware che ha diverse parti: un logger, un modulo UI e un servizio di rete. In questo scenario, tutti questi moduli hanno bisogno di intraprendere un'azione quando una connessione Wi-Fi viene stabilita. 

Una possibile soluzione è che tutti questi moduli interroghino ad intervalli regolari il componente Wi-Fi per vedere se c'è stata una connessione. Questo approccio è detto __polling__ ed in questo casi è piuttosto inefficiente. 

Un'altra soluzione è invece che sia lo stesso componente Wi-Fi a far sapere a tutti i componenti interessati che la connessione è avvenuta generando un evento. Per gestire questa modalità, si utilizza l'event loop.  

L'event loop permette a ciascun componente di registrare un handler indipendente che viene chiamato qualora un particolare evento si verifichi. 

Questo approccio riduce l'accoppiamento tra il componente Wi-Fi e tutti gli altri ed elimina la necessità di complesse interdipendenze tra componenti. Di conseguenza, le applicazioni diventano più modulari, scalabili e facili da mantenere.

Gli event loop sono particolarmente utili quando più componenti devono reagire allo stesso evento in modo indipendente, come nel caso dello scenario precedente. 

## Eventi e funzioni di callback

L'event loop ruota attorno a due concetti chiave:

* **Eventi**
* **Funzioni di callback**

Quando un evento si verifica, il modulo che l'ha generato "posta" l'evento sull'event loop. Quest'ultimo invoca poi la funzione di callback corrispondente. 

Per far funzionare questo meccanismo, è necessario registrare sia l'evento sia la callback associata.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-advanced/assets/lecture_2_event_loop.webp" | absURL }}"
height=400
caption="Diagramma semplificato dell'event loop"

>}}

Molti eventi possono essere raggruppati logicamente, ad esempio tutti gli eventi relativi a Wi-Fi o al MQTT.
Per questo motivo ciascun evento è categorizzato utilizzando due identificatori:

* Una **event base**, che definisce il gruppo di cui l'evento fa parte.
* Un **event ID**, che identifica l'evento specifico all'interno di quel gruppo.

Ad esempio, gli eventi relativi al Wi-Fi ricadono nella event base chiamata `WIFI_EVENT`. `Event ID` specifici all'interno di questa base includono `WIFI_EVENT_STA_START` e `WIFI_EVENT_STA_DISCONNECTED`.

### Event loop di default

ESP-IDF crea e gestisce automaticamente un *event loop di default* per gli eventi di sistema, come appunto il Wi-Fi, la configurazione IP od il Bluetooth. I componenti di sistema postano eventi su questo event loop, e il codice della tua applicazione può registrare funzioni (handler) per elaborarli.

È possibile generare event loop personalizzati ma generalmente, l'event loop di default è sufficiente ed evita overhead aggiuntivo. 

Gli sviluppatori possono infatti postare eventi della propria applicazione anche sull'event loop di default. Maggiori dettagli sulle differenze tra event loop di default e event loop utente sono disponibili nella [documentazione](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_event.html#default-event-loop).

## Esempi di Codice

### Definire un evento

Il seguente codice mostra come definire una event base e gli event ID usando le macro di ESP-IDF:

```c
// In your header file (e.g., my_events.h)
#include "esp_event.h"

ESP_EVENT_DECLARE_BASE(MY_EVENT_BASE);

typedef enum {
    MY_EVENT_ID_1,
    MY_EVENT_ID_2,
    MY_EVENT_ID_3,
} my_event_id_t;
```

```c
// In your source file (e.g., my_events.c)
#include "my_events.h"

ESP_EVENT_DEFINE_BASE(MY_EVENT_BASE);
```

Questo approccio utilizza `ESP_EVENT_DECLARE_BASE()` per dichiarare la event base in un file header e `ESP_EVENT_DEFINE_BASE()` per definirla in un file sorgente. Gli event ID sono tipicamente dichiarati come `enum`. 

Queste macro creano semplicemente variabili globali. Possiamo dare un'occhiata al loro codice per capire cosa fanno:

```c
// Defines for declaring and defining event base
#define ESP_EVENT_DECLARE_BASE(id) extern esp_event_base_t const id
#define ESP_EVENT_DEFINE_BASE(id) esp_event_base_t const id = #id
```

### Definire e registrare un event handler

Il seguente esempio mostra come definire un handler e registrarlo sull'event loop di default per un evento specifico:

```c
// Define the event handler
void run_on_event(void* handler_arg, esp_event_base_t base, int32_t id, void* event_data)
{
    // Event handler logic
}

// Register the handler to the default event loop
esp_event_handler_register(MY_EVENT_BASE, MY_EVENT_ID, &run_on_event, NULL);
```

### Postare un evento sull'event loop di default

Se si vuole generare un evento, è possibile farlo attraverso un `post` sull'event loop di default. 

```c
// Post an event to the default event loop
esp_event_post(MY_EVENT_BASE, MY_EVENT_ID, &event_data, sizeof(event_data), portMAX_DELAY);
```

### Creare e utilizzare un event loop utente

In scenari più avanzati, potresti voler creare un event loop dedicato. 
Di seguito un semplice esempio. 

```c
esp_event_loop_handle_t user_loop;
esp_event_loop_args_t loop_args = {
    .queue_size = 5,
    .task_name = "user_event_task", // Set to NULL to avoid creating a dedicated task
    .task_priority = uxTaskPriorityGet(NULL),
    .task_stack_size = 2048,
    .task_core_id = tskNO_AFFINITY
};

// Create the user event loop
esp_event_loop_create(&loop_args, &user_loop);

// Register a handler with the custom event loop
esp_event_handler_register_with(user_loop, MY_EVENT_BASE, MY_EVENT_ID, &run_on_event, NULL);

// Post an event to the custom loop
esp_event_post_to(user_loop, MY_EVENT_BASE, MY_EVENT_ID, &event_data, sizeof(event_data), portMAX_DELAY);
```

## Conclusione

L'event loop offre un modo versatile di gestire eventi asincroni in modo pulito ed efficiente. 

> Prossimo passo: [Esercizio 2.1](../assignment-2-1/)

> Oppure [torna al menù di navigazione](../#agenda)
> 
## Approfondimenti

* [Panoramica della libreria event loop](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_event.html)
* [API esp_event](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/esp_event.html)
* [Esempio event loop di default](https://github.com/espressif/esp-idf/blob/master/examples/system/esp_event/default_event_loop/README.md)
* [Esempio event loop utente](https://github.com/espressif/esp-idf/blob/master/examples/system/esp_event/user_event_loops/README.md)
