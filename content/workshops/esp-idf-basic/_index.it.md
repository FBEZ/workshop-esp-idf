---
title: "ESP-IDF workshop: Base"
date: "2025-11-12"
summary: "Questo workshop è incentrato sulle basi del framework ESP-IDF: compilerai il tuo primo progetto e programmerai il modulo ESP32-C3 montato su un EVK. Durante questa attività, creerai dei componenti per ESP-IDF e farai partire un server HTTP con REST API. "
---

Benvenuto al workshop base su ESP-IDF!

## Introduzione

In questo workshop acquisirai una solida comprensione del framework ESP-IDF, imparando a utilizzare in modo efficace Visual Studio Code (VS Code) e l’estensione ESP-IDF per VS Code. 

Il workshop è diviso in tre parti. 

Nella prima parte, verificheremo che il tuo ambiente di sviluppo sia configurato correttamente, utilizzando come punto di partenza il classico esempio `hello world`.

Nella seconda parte, approfondiremo lo stack di rete e realizzeremo insieme un semplice server HTTP.

La terza parte sarà dedicata a due periferiche molto comuni: GPIO e I2C. Esploreremo inoltre il sistema dei componenti e il component registry, che permette di usare librerie senza dover gestire manualmente le dipendenze o le impostazioni del build system. Nell'ultima esercitazione, combineremo il tutto per creare un semplice gateway di sensori, integrando connettività e controllo delle periferiche in un unico progetto.

Al termine del workshop, avrai le competenze di base necessarie per iniziare a sviluppare le tue applicazioni basate su ESP-IDF.

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Durata stimata: 3 ore.
{{< /alert >}}

## Agenda

Il workshop è diviso in tre parti, ciascuna della durata di circa un’ora. 

* __Parte 1__: Benvenuto e introduzione

  * [Lezione 1](lecture-1/) – Introduzione a ESP-IDF e all’estensione ESP-IDF per VS Code
  * [Esercizio 1.1](assignment-1-1/) – Verifica l’installazione di ESP-IDF e VS Code compilando e caricando l’esempio `hello_world`. Modifica il testo dell’esempio.
  * [Esercizio 1.2](assignment-1-2/) – Crea un nuovo progetto a partire dall’esempio `blink`.

* __Parte 2__: Connettività HTTP

  * [Lezione 2](lecture-2/) – Connettività: protocollo HTTP, HTML e REST API
  * [Esercizio 2.1](assignment-2-1/) – Crea un server HTTP per la gestione della richiesta `GET /index.html/` che restituisca `<h1>Hello LED Control</h1>`.
  * [Esercizio 2.2](assignment-2-2/) – Aggiungi al server HTTP le seguenti route:

    * `GET /led/on` → accende il LED e restituisce il JSON `{"led": "on"}`
    * `GET /led/off` → spegne il LED e restituisce il JSON `{"led": "off"}`
    * `POST /led/blink` → accetta un JSON `{ "times": int, "interval_ms": int }` e fa lampeggiare il LED il numero di volte indicato con l’intervallo specificato. 
  * [Esercizio 2.3](assignment-2-3/) – *(Opzionale)* Aggiungi al server HTTP la route:

    * `POST /led/flash` → accetta il JSON `{"periods": [int], "duty_cycles": [int]}` e, per ogni elemento, calcola i tempi di accensione e spegnimento, pilotando il LED di conseguenza.

* __Parte 3__: Periferiche e integrazione

  * [Lezione 3](lecture-3/) – GPIO, I2C e uso del component registry. 
  * [Esercizio 3.1](assignment-3-1/) – Crea un nuovo componente per pilotare il LED.
  * [Esercizio 3.2](assignment-3-2/) – Aggiungi un componente per la lettura del sensore ambientale a bordo.
  * [Esercizio 3.3](assignment-3-3/) – *(Opzionale)* Aggiungi la rotta:

    * `GET /environment/` → restituisce la lettura del sensore. Scegli il formato JSON più adatto per rappresentare i dati.

## Prerequisiti

Per seguire questo workshop, assicurati di soddisfare i prerequisiti riportati di seguito.

### Software richiesto

* **VS Code** installato sul proprio computer
* **[Estensione ESP-IDF per VS Code](https://docs.espressif.com/projects/vscode-esp-idf-extension/en/latest/)** aggiunta a VS Code
* **ESP-IDF** installato sulla propria macchina<br>
  *Può essere installato tramite VS Code oppure utilizzando l’[ESP-IDF Installer Manager](https://docs.espressif.com/projects/idf-im-cli/en/latest/index.html)*

### Hardware richiesto

* Scheda ESP-C3-DevKit-RUST-1 o ESP-C3-DevKit-RUST-2 (se l'attività è in presenza, la scheda verrà fornita durante il workshop)<br>
  *È possibile utilizzare anche una scheda ESP32-C3-DevKit-M/C, ma sarà necessario adattare la configurazione dei pin GPIO di conseguenza.*

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Se l'evento si svolge in presenza, si consiglia vivamente di installare **VS Code** e il **plugin ESP-IDF** **prima** dell’inizio del workshop.
In caso di problemi, sarà comunque previsto un breve momento durante il primo esercizio per completare l’installazione.
{{< /alert >}}

### Conoscenze di base

* Elettronica di base
  * Resistenze, condensatori, alimentatori DC/DC
  * Lettura di uno schema elettrico
* Programmazione embedded di base
  * Cos'é la memoria flash
  * Differenza tra compilazione e caricamento del firmware
  * Conoscenza delle principali periferiche di un microcontrollore (principalmente GPIO e I2C)
* Nozioni base del linguaggio C
  * Cos'è un header file
  * Concetti di compilatore / linker
  * Uso di `define`, `struct` e `typedef`
* Formati [JSON](https://it.wikipedia.org/wiki/JSON) e [YAML](https://it.wikipedia.org/wiki/YAML)
* HTML e i suoi principali tag (`<html>`, `<body>`, `<h1>`, `<h2>`, `<p>`)
* Nozioni base sui metodi di richiesta HTTP (`GET`, `POST`) e sul concetto di URI e *route*
<!-- 
#### Tabella prerequisiti

| Prerequisito              | Descrizione                                                                                                             | Riferimento                                                                                                                                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tipi di memoria MCU       | Differenza tra Flash, RAM ed EEPROM                                                                                     | [L. Harvie (Medium)](https://medium.com/@lanceharvieruntime/embedded-systems-memory-types-flash-vs-sram-vs-eeprom-93d0eed09086)                                                      |
| Periferiche seriali MCU   | Differenza tra SPI, I2C e UART                                                                                          | [nextpcb.com](https://www.nextpcb.com/blog/spi-i2c-uart)                                                                                                                             |
| File header e linker      | A cosa servono i file header e qual è il ruolo del linker                                                               | [CBootCamp](https://gribblelab.org/teaching/CBootCamp/12_Compiling_linking_Makefile_header_files.html), [themewaves](https://themewaves.com/understanding-linkers-in-c-programming/) |
| JSON                      | Formato di dati indipendente dal linguaggio, derivato da JavaScript. Base delle REST API                                | [Wikipedia](https://en.wikipedia.org/wiki/JSON)                                                                                                                                      |
| YAML                      | Formato di serializzazione dati leggibile dall’uomo, usato per la gestione delle dipendenze tramite `idf_component.yml` | [Wikipedia](https://en.wikipedia.org/wiki/YAML), [datacamp.com](https://www.datacamp.com/blog/what-is-yaml)                                                                          |
| Tag HTML                  | Introduzione ai principali tag HTML                                                                                     | [Freecodecamp](https://www.freecodecamp.org/news/introduction-to-html-basics/)                                                                                                       |
| Metodi di richiesta HTTP  | Introduzione e differenze tra i metodi HTTP (GET, POST, ecc.)                                                           | [Restfulapi.net](https://restfulapi.net/http-methods/)                                                                                                                               |
| Plugin ESP-IDF per VS Code | Estensione ufficiale Espressif per Visual Studio Code                                                                   | [Installazione VS Code-esp-idf-extension](https://github.com/espressif/VSCode-esp-idf-extension?tab=readme-ov-file#how-to-use)                                                        | -->

## Prossimo passo

> Il prossimo passo è **[Lezione 1](lecture-1/)**.

## Conclusione

Congratulazioni! Sei arrivato alla fine di questo workshop.
Ci auguriamo che sia stata un’esperienza utile e l’inizio di un percorso di approfondimento dei tool di Espressif.  

Ora sei in grado di creare, compilare e caricare nuovi progetti, utilizzare librerie e componenti esterni, creare i tuoi componenti e controllare tutto tramite un’interfaccia HTTP.
Hai quindi acquisito le basi fondamentali per sviluppare un’applicazione IoT.

