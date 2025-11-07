---
title: "ESP-IDF Avanzato - Lezione 1"
date: "2025-11-12"
series: ["WS00B"]
series_order: 2
showAuthor: false
summary: "In questa lezione esploreremo il build system di ESP-IDF, che si basa su CMake e Ninja. Approfondiremo il concetto di componenti, il ruolo del Component Manager e dei Board Support Package (BSP) per l’astrazione dell’hardware. Infine, vedremo come creare componenti personalizzati e gestire le configurazioni attraverso i file sdkconfig e i profili di build, per ottenere compilazioni più flessibili e riproducibili."
---

## Introduzione

Il build system dell'ESP-IDF è basato su **CMake** e **Ninja**. CMake si occupa di configurare il progetto e generare i file necessari per la compilazione, mentre Ninja gestisce il processo di build vero e proprio con un sovraccarico molto ridotto rispetto al tradizionale `make`.

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-advanced/assets/lecture_1_build_system.webp" | absURL }}"
height=500
caption="Build system tool chain"
    >}}

Per semplificare lo sviluppo, ESP-IDF fornisce uno strumento da riga di comando chiamato `idf.py`. 
Questo tool funge da interfaccia per CMake e Ninja, gestendo sia la configurazione e la compilazione del progetto, che il flashing del firmware sul dispositivo (tramite `esptool.py`). `idf.py` offre inoltre un menu di configurazione (`menuconfig`) che consente di personalizzare le impostazioni del progetto, e di salvarle in un unico file chiamato `sdkconfig`. 
Gli IDE come VS Code ed Espressif IDE (Eclipse) forniscono solitamente interfacce grafiche che semplificano l’uso di `idf.py` ma che di fatto sono dei wrapper intorno a questo tool. 

In questo workshop utilizzeremo l'estensione ESP-IDF per VS Code.

## Sviluppo modulare

Per gestire lo sviluppo di applicazioni complesse, ESP-IDF offre un sistema di componenti, accompagnato da un potente component manager.

### Componenti ESP-IDF

In ESP-IDF, molte librerie sono organizzate in componenti, ossia codice modulare e indipendente che fornisce una funzionalità specifica. Esempi di moduli gestiti come componenti sono driver o protocolli. Questa struttura semplifica il riutilizzo del codice, la sua organizzazione e la manutenzione in applicazioni complesse.

Ad esempio, la gestione di un sensore può essere effettuata da un componente dedicato, il quale incapsula tutta la logica di comunicazione e di elaborazione dei dati, evitando così di riscrivere codice in ogni progetto.

Un tipico componente include:

* Codice sorgente
* File header
* File `CMakeLists.txt` per la configurazione di build
* File `idf_component.yml` che descrive le dipendenze e le informazioni di versione

{{< figure
default=true
src="{{ "/workshop-esp-idf/workshops/esp-idf-basic/assets/esp_idf_components.webp" | absURL }}"
height=200 
caption="Fig.1 - Struttura di un componente"
>}}


Questa struttura consente di integrare e gestire facilmente i componenti nei progetti ESP-IDF, supportando lo sviluppo modulare e la condivisione del codice. Ulteriori informazioni possono essere trovato alla 
pagina [gestione e utilizzo dei componenti](https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/advanced-development/component-management.html).

### Component manager

Il component manager è uno strumento progettato per semplificare la gestione dei componenti nei progetti ESP-IDF. Questo tool consente agli sviluppatori di:

* Aggiungere componenti come dipendenze dei progetti.
* Scaricare e aggiornare automaticamente componenti dal [registro dei componenti ESP](https://components.espressif.com) o da repository git.
* Gestire in modo affidabile versioni e dipendenze dei componenti.

Durante la compilazione, il component manager scarica tutti i componenti necessari (incluse le rispettive dipendenze) e li colloca nella cartella `managed_components`. Questo approccio semplifica l’estensione delle funzionalità e incoraggia il riutilizzo del codice generato dalla comunità degli sviluppatori Espressif.

### Board Support Packages (BSP) in ESP-IDF

Un tipo particolare di componente ESP-IDF è il **Board Support Package (BSP)**, un componente che incapsula l’inizializzazione hardware per una specifica scheda di sviluppo. I BSP forniscono driver pre-configurati e un’API coerente per l’accesso alle periferiche integrate come LED, pulsanti, display, pannelli touch, codec audio e schede SD. Come ogni altro componente ESP-IDF, un BSP può essere integrato in un progetto tramite il component manager, usando il comando `idf.py add-dependency` che modificherà il `idf_component.yml`.

Su un EVK base come la ESP32-C6-DevKit, il BSP semplifica la configurazione dei componenti come il pulsante e il LED indirizzabile presenti sulla scheda. Su piattaforme più complesse (ad es. ESP32-S3-BOX-3), il BPS include l’inizializzazione periferiche come display e dispositivi audio. 

I principali vantaggi dell’uso di un BSP sono:

* Inizializzazione delle periferiche: i BSP gestiscono la configurazione di basso livello (GPIO, I2C, SPI, ecc.) per l’hardware supportato.
* Astrazione riutilizzabile: i BSP espongono un’API comune, consentendo il riutilizzo del codice tra progetti e varianti di schede.
* Avvio rapido: i BSP permettono di iniziare immediatamente lo sviluppo dell'applicazione, perché le periferiche sono già pronte all'uso. 

#### BSP personalizzati

Per schede non supportate o personalizzate, è possibile utilizzare BSP generici (es. `esp_bsp_generic`, `esp_bsp_devkit`) e regolare le mappature hardware tramite `menuconfig`. Questo approccio consente ai BSP di fungere da livello di astrazione hardware flessibile, sia per hardware ufficiale che personalizzato.

## Come creare un componente

Vediamo ora come creare un componente `led_toggle` partendo dall’esempio `hello_world`.

Dopo aver creato un progetto dall’esempio `hello_world`, la struttura file del progetto sarà la seguente:

```bash
.
├── CMakeLists.txt
├── main
│   ├── CMakeLists.txt
│   └── hello_world_main.c
├── pytest_hello_world.py
├── README.md
├── sdkconfig
├── sdkconfig.ci
└── sdkconfig.old
``` 

Per creare un componente, apri la palette dei comandi e digita:

* `> ESP-IDF: Create a new ESP-IDF Component`<br>
  &rarr; `led_toggle`

Ora la struttura del progetto diventa:

```bash
.
├── CMakeLists.txt
├── components   # <--- nuova cartella
│   └── led_toggle
│       ├── CMakeLists.txt
│       ├── include
│       │   └── led_toggle.h
│       └── led_toggle.c
├── main
│   ├── CMakeLists.txt
│   └── hello_world_main.c
├── pytest_hello_world.py
├── README.md
├── sdkconfig
├── sdkconfig.ci
└── sdkconfig.old
```

Come puoi vedere, è stata creata una nuova cartella `components` e al suo interno si trova il componente `led_toggle`.

Nella cartella componente ritroviamo

1. `CMakeLists.txt` che contiene la configurazione utilizzata dal sistema di build
2. Cartella `include` che contiene gli header (inclusi automaticamente dal linker)
3. File `.c` ossia il codice effettivo del componente

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Affinché il build system trovi i componenti appena aggiunti, è necessario fare un "full clean". In VS Code, puoi eseguire<br>
`> ESP-IDF: Full Clean Project`.
{{< /alert >}}

Supponiamo di avere il seguente file header del componente:

```c
// led_toggle.h
#include "driver/gpio.h"

typedef struct {
    int gpio_nr;
    bool status;
}led_gpio_t;

esp_err_t led_config(led_gpio_t * led_gpio);
esp_err_t led_drive(led_gpio_t * led_gpio);
```

Dopo una full clean, puoi semplicemente includerlo nel file principale e richiamarne le funzioni:

```c
#include "led_toggle.h"
//[...]
void app_main(void)
{
    printf("Hello world!\n");

    led_gpio_t led_board = { .gpio_nr = 5, .status = true };

    led_config(led_board)
    led_drive(led_board)
}
```

## Gestione della configurazione nei progetti ESP-IDF

I progetti ESP-IDF gestiscono la configurazione tramite due file: `sdkconfig` e `sdkconfig.defaults`.

* `sdkconfig` contiene la configurazione attiva del progetto. Viene generato e aggiornato automaticamente dagli strumenti di configurazione come `idf.py menuconfig`, registrando tutte le opzioni selezionate.
* `sdkconfig.defaults` fornisce un insieme di valori predefiniti per le opzioni di configurazione. È utile per impostare configurazioni iniziali coerenti per nuovi build o diversi ambienti (sviluppo, test, produzione).

Puoi generare un file `sdkconfig.defaults` che rifletta la configurazione corrente digitando il seguente comando nella palette dei comandi di VS Code

```
> ESP-IDF: Save Default SDKCONFIG File (save-defconfig)
```

Questo comando è un wrapper intorno a:

```sh
idf.py save-defconfig
```

Il comando salva nel file `sdkconfig.defaults` tutti i valori di configurazione *che differiscono* da quelli predefiniti.

### Ottimizzazione delle prestazioni

I componenti e le librerie sono spesso configurabili attraverso delle impostazioni che vengono modificate via `menuconfig`. Le impostazioni predefinite di ESP-IDF rappresentano un compromesso tra prestazioni, utilizzo di risorse e disponibilità di funzionalità.

Per i sistemi di produzione, gli sviluppatori possono avere obiettivi specifici di ottimizzazione (es. riduzione dell’uso di memoria, aumento della velocità o riduzione del consumo energetico). Questi obiettivi si ottengono selezionando e regolando le opzioni di configurazione appropriate nel `menuconfig`. 

A tal fine, la documentazione ufficiale fornisce una [guida all’ottimizzazione delle prestazioni](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/index.html) con strategie e suggerimenti per raggiungere gli obiettivi desiderati.

### Uso di più file `sdkconfig` 

ESP-IDF supporta più file di default (`sdkconfig.xxx`), che possono essere specificati tramite la variabile d’ambiente `SDKCONFIG_DEFAULTS` o all’interno del `CMakeLists.txt` del progetto. I file vengono elencati separati da punti e virgola e applicati in ordine: se esistono chiavi sovrapposte, i valori dei file successivi sovrascrivono quelli precedenti. Questo approccio a livelli consente di:

* Mantenere impostazioni condivise in un file comune
* Sovrascriverle con impostazioni specifiche per ambiente o prodotto

È inoltre possibile definire *default specifici per chip* tramite file come `sdkconfig.defaults.<chip>`, ad esempio `sdkconfig.defaults.esp32s3`. Questi vengono considerati solo se esiste un file `sdkconfig.defaults` (anche vuoto). Tale meccanismo consente un controllo fine delle configurazioni per diverse varianti di chip Espressif all’interno dello stesso progetto.

### Gestione degli scenari di build con i profili

I file di profilo consentono di racchiudere le impostazioni di compilazione per scenari specifici (es. sviluppo, debug, produzione) in file riutilizzabili. Questi file contengono di fatto gli argomenti di riga di comando del `idf.py`.

Consideriamo il caso di due compilazioni differenti per produzione e debug:

* `profiles/prod` – build di produzione
* `profiles/debug` – build di debug

Per compilare usando un profilo:

```sh
idf.py @profiles/prod build
```

È anche possibile combinare file di profilo con ulteriori argomenti da riga di comando per maggiore flessibilità. Questo approccio promuove coerenza e semplicità nel passaggio tra diversi ambienti di compilazione.
Per maggiori dettagli, puoi fare riferimento all'[ESP-IDF multi-config](https://github.com/espressif/esp-idf/blob/master/examples/build_system/cmake/multi_config/README.md).

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
L’estensione ESP-IDF per VS Code consente di definire più configurazioni tramite file JSON. È previsto che questo approccio venga unificato con quello da CLI nel prossimo futuro. Puoi consultare i dettagli nella [documentazione](https://docs.espressif.com/projects/vscode-esp-idf-extension/en/latest/additionalfeatures/multiple-projects.html#use-multiple-build-configurations-in-the-same-workspace-folder).
{{< /alert >}}

### Esempio pratico: isolare build di sviluppo e produzione

Per mantenere configurazioni separate per sviluppo e produzione:

1. Crea un file `sdkconfig.defaults` per lo sviluppo.
2. Crea file specifici per la produzione, come `sdkconfig.prod_common` e `sdkconfig.prod1`.
3. Compila con la configurazione di produzione usando:

   ```sh
   idf.py -B build_prod1 -D SDKCONFIG_DEFAULTS="sdkconfig.prod_common;sdkconfig.prod1" build
   ```

Questo crea una directory di build isolata (`build_prod1`) e applica la configurazione specificata. In questo modo puoi mantenere build riproducibili e indipendenti per diversi ambienti.

Approfondiremo questo argomento nell’[esercizio 1.3](../assignment-1-3/).

## Conclusione

Il sistema di build ESP-IDF fornisce una base versatile per lo sviluppo di applicazioni embedded. Grazie a componenti modulari, dipendenze gestite e supporto per Board Support Package (BSP) riutilizzabili, gli sviluppatori possono creare progetti scalabili e manutenibili. Strumenti come `idf.py`, il Component Manager e le configurazioni basate su profili semplificano sia lo sviluppo che la distribuzione di codice. 
Padroneggiando questi strumenti, sarai in grado di creare firmware robusti per un’ampia varietà di piattaforme hardware ed applicazioni. 

> Passaggio successivo: [Esercizio 1.1](../assignment-1-1/)

> Oppure [torna al menù di navigazione](../#agenda)


## Approfondimenti

* [Cos’è l’ESP Component Registry?](https://developer.espressif.com/blog/2024/10/what-is-the-esp-registry/)
* [Documentazione di IDF Component Manager ed ESP Component Registry](https://docs.espressif.com/projects/idf-component-manager/en/latest/index.html)
