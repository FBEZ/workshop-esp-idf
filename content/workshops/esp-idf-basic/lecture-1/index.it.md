---
title: "ESP-IDF Base - Lezione 1"
date: "2025-11-12"
series: ["WS00A"]
series_order: 1
showAuthor: false
summary: "In questa lezione introduciamo ESP-IDF, il framework ufficiale di Espressif per lo sviluppo di applicazioni IoT, analizzandone l’architettura, i principali componenti e gli strumenti di sviluppo. Esploriamo inoltre l’hardware utilizzato nel workshop, basato sul SoC ESP32-C3, preparando così il terreno per il primo esercizio pratico."
---

## Introduzione a ESP-IDF

ESP-IDF (Espressif IoT Development Framework) è il framework di sviluppo ufficiale per i SoC di Espressif Systems.
Fornisce un ambiente completo per la creazione di applicazioni IoT con funzionalità avanzate di connettività, sicurezza e affidabilità.

Il framework ESP-IDF include FreeRTOS, consentendo agli sviluppatori di creare applicazioni multitasking in tempo reale.
Dispone di un insieme completo di librerie, strumenti e documentazione, fungendo da base per lo sviluppo su dispositivi Espressif.

ESP-IDF include oltre 400 esempi, aiutando gli sviluppatori a iniziare rapidamente i propri progetti.

### Architettura

L’architettura della piattaforma ESP-IDF è principalmente suddivisa in 3 livelli:

* **Piattaforma ESP-IDF**
  Contiene i componenti di base necessari e il sistema operativo. Include FreeRTOS, driver, build system, protocolli, ecc.
* **Middleware**
  Aggiunge nuove funzionalità a ESP-IDF, come framework audio o HMI. In questo workshop non li utilizzeremo.
* **Applicazione AIoT**
  La tua applicazione.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/esp-idf-highlevel.webp" | absURL }}"
height=500
caption="Fig.1 - Panoramica ad alto livello di ESP-IDF"

>}}

Tutti i blocchi costitutivi necessari per la tua applicazione sono inclusi nella piattaforma ESP-IDF.
Visita il progetto ESP-IDF su GitHub per consultare l’elenco aggiornato delle versioni supportate e i relativi periodi di sviluppo attivo e supporto a lungo termine.

{{< github repo="espressif/esp-idf" >}}

### Principali blocchi di ESP-IDF

ESP-IDF è costruito su FreeRTOS e contiene diverse librerie.
Le principali librerie che includerai nei tuoi progetti sono:

1. **FreeRTOS (`freertos`)**: kernel di sistema operativo leggero e real-time, che fornisce multitasking tramite preemptive scheduling, gestione dei task e comunicazione tra task.
2. **Driver (`esp_driver_xxx`)**: librerie per la gestione delle periferiche.
3. **Protocolli (`esp_http`, `esp-tls`, ecc.)**: librerie che implementano protocolli di comunicazione.

Durante gli esercizi imparerai a includere sia librerie interne fornite da ESP-IDF che librerie esterne.
ESP-IDF offre anche un sistema basato su pacchetti (chiamati "componenti") per la gestione delle librerie e le loro dipendenze.

### Componenti

I componenti sono pacchetti che includono librerie, file per la gestione delle dipendenze, metadati e configurazioni.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/esp_idf_components.webp" | absURL }}"
height=300
caption="Fig.2 - Componenti ESP-IDF"

>}}

I componenti vengono utilizzati per aggiungere nuove funzionalità come driver di sensori, protocolli di comunicazione, *board support package* e altre caratteristiche non incluse di default in ESP-IDF.
Alcuni componenti sono già integrati negli esempi ufficiali, e lo stesso ESP-IDF adotta il modello dei componenti esterni per promuovere la modularità.

L’uso dei componenti migliora la manutenibilità e accelera lo sviluppo, permettendo il riuso e la condivisione del codice tra più progetti.

Se vuoi creare e pubblicare un tuo componente, ti consigliamo di guardare la presentazione [DevCon23 - Developing, Publishing, and Maintaining Components for ESP-IDF](https://www.youtube.com/watch?v=D86gQ4knUnc) o di leggere l’articolo [How to create an ESP-IDF component](https://developer.espressif.com/blog/2024/12/how-to-create-an-esp-idf-component/).

{{< youtube D86gQ4knUnc >}}

Puoi anche trovare componenti visitando la piattaforma [ESP Registry](https://components.espressif.com).

Nell’[esercizio 3.2](../assignment-3-2/) avrai la possibilità di creare un tuo componente e utilizzarlo nel progetto.

### Framework

ESP-IDF è anche la base per altri framework, tra cui:

* **Arduino per Espressif**
* **ESP-ADF** (Audio Development Framework): progettato per applicazioni audio.
* **ESP-WHO** (AI Development Framework): focalizzato sul riconoscimento facciale.
* **ESP-RainMaker**: semplifica la creazione di dispositivi connessi con funzionalità cloud.
* **ESP-Matter SDK**: SDK ufficiale di Espressif per lo sviluppo di applicazioni Matter.

Per consultare tutti i framework supportati, visita la [pagina GitHub dell’organizzazione Espressif](https://github.com/espressif).


## Sviluppo con ESP-IDF

Oltre alle librerie, ESP-IDF include gli strumenti necessari per compilare, flashare e monitorare il dispositivo.

Puoi sviluppare applicazioni per dispositivi Espressif con qualsiasi editor di testo, come [Gedit](https://gedit-text-editor.org/) o [Notepad++](https://notepad-plus-plus.org/), seguendo la [guida di installazione manuale](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html#manual-installation) presente nella documentazione ufficiale Espressif.

In questo workshop, tuttavia, utilizzeremo un IDE (Integrated Development Environment) per semplificare sia lo sviluppo che la configurazione.
Espressif supporta diversi IDE, ma ci concentreremo su **Visual Studio Code (VS Code)**, che dispone di un’estensione ufficiale chiamata [`ESP-IDF`](https://marketplace.visualstudio.com/items?itemName=espressif.esp-idf-extension).
Questa estensione consente di sviluppare, compilare, caricare e fare debug dei progetti direttamente all’interno dell’editor.

Per darti un’idea, l’estensione ESP-IDF per VS Code gestisce la toolchain e fornisce comandi come:

* `> ESP-IDF: Build Your Project`
* `> ESP-IDF: Set Espressif Device Target`
* `> ESP-IDF: Full clean project`

Il carattere `>` indica la *palette dei comandi* di VS Code, accessibile premendo `F1` o `Ctrl`+`Shift`+`P` (su macOS `Cmd`+`Shift`+`P`).

Tutti questi comandi sono dei wrapper attorno allo strumento principale di ESP-IDF, [`idf.py`](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/tools/idf-py.html).


## Hardware utilizzato nel workshop

In questo workshop utilizzeremo un modulo basato sul [SoC ESP32-C3](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf), chiamato [ESP32-C3-Mini-1-N4](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf).
Puoi individuare l’ESP32-C3-Mini-1-N4 sulla tua scheda del workshop (vedi Fig. 3). Il SoC ESP32-C3 si trova sotto lo shield del modulo.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/lec_1_module.webp" | absURL }}"
height=500
caption="Fig.3 - SoC ESP32-C3, modulo e scheda del workshop"

>}}

### ESP32-C3 SoC

ESP32-C3 è un SoC dotato di processore RISC-V a 32 bit, con supporto Wi-Fi a 2.4 GHz e Bluetooth LE (Low Energy).
Il diagramma a blocchi funzionale è mostrato in Fig. 4.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/esp32-c3-overview.webp" | absURL }}"
height=500
caption="Fig.4 - Diagramma a blocchi ESP32-C3"

>}}

ESP32-C3 offre:

* Processore __RISC-V__ single-core a 160 MHz
* __Wi-Fi__: supporta modalità Station, SoftAP e mista
* __Bluetooth LE__: compatibile con Bluetooth 5 e mesh
* __Memoria integrata__: 400 KB SRAM, 384 KB ROM
* __Meccanismi di sicurezza__: acceleratori crittografici hardware, flash cifrata, bootloader sicuro
* __Ampio set di periferiche__: fino a 22 GPIO programmabili per LED PWM, UART, I2C, SPI, I2S, ADC, USB/JTAG, ecc.

### Modulo ESP32-C3-Mini-1-N4

Espressif offre anche dei moduli che integrano il SoC, memoria flash aggiuntiva, memoria PSRAM, e un’antenna PCB o connettore.
Il vantaggio principale della soluzione modulo è la semplicità d’uso (non serve disegnare la parte RF) e la semplificazione in sede di certificazione. 
Il modulo utilizzato, l'**ESP32-C3-MINI-1-N4**, include 4MB di flash. 

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
Puoi trovare la spiegazione dei part number di Espressif nell'articolo [Espressif part numbers explained: A complete guide - Modules](https://developer.espressif.com/blog/2025/03/espressif-part-numbers-explained/).
{{< /alert >}}

### Scheda del workshop ESP32-C3

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/esp32_c3-_devkit_rust_1_top.webp" | absURL }}"
height=500
caption="Fig.5 - Scheda del workshop"

>}}

#### Schemi elettrici

Puoi trovare tutti gli schemi nella [repository Github del EVK](https://github.com/esp-rs/esp-rust-board/blob/master/hardware/esp-rust-board/schematic/esp-rust-board.pdf).

## Conclusione

Ora che abbiamo una panoramica generale di hardware e firmware, siamo pronti per iniziare il primo esercizio.

### Prossimo passo

> Prossimo esercizio → **[Esercizio 1.1](../assignment-1-1)**

> Oppure [torna al menù di navigazione](../#agenda)

