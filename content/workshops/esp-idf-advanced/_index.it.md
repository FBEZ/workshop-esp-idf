---
title: "ESP-IDF workshop: Avanzato"
date: "2025-11-12"
series: ["WS00B"]
series_order: 1
showAuthor: false
summary: "Questo workshop tratta le funzionalità avanzate di ESP-IDF e si concentra sullo sviluppo modulare, sull'event loop, sui core dump, sulla size analysis e sulla cifratura della flash."
--- 

Benvenuto al workshop ESP-IDF avanzato!

## Introduzione

In questo workshop incontreremo alcuni aspetti più avanzati del framework ESP-IDF, tra cui lo sviluppo modulare tramite componenti, l'event loop, i core dump e le funzionalità di sicurezza.

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Tempo stimato: 3 ore.
{{< /alert >}}

## Agenda

Il workshop è suddiviso in quattro parti. 

* Parte 1: **Componenti**

  * [Lezione 1](lecture-1/) – Cos’è un componente, come crearlo e come supportare più versioni hardware tramite BSP e configurazioni multiple
  * [Esercizio 1.1](assignment-1-1/) – Refactoring del codice creando il componente `alarm`
  * [Esercizio 1.2](assignment-1-2/) – Refactoring del codice creando il componente `cloud_manager`
  * [Esercizio 1.3](assignment-1-3/) – Configurazioni multiple utilizzando `sdkconfig`

* Parte 2: **Event Loop**

  * [Lezione 2](lecture-2/) – Informazioni base sugli event loop in ESP-IDF, uso degli eventi dei timer e separazione delle responsabilità
  * [Esercizio 2.1](assignment-2-1/) – Refactoring del codice per utilizzare l'event loop
  * [Esercizio 2.2](assignment-2-2/) – Aggiungere un evento GPIO all’event loop

* Parte 3: **Prestazioni e analisi dei crash**

  * [Lezione 3](lecture-3/) – Size analysis ed uso del core dump per debug
  * [Esercizio 3.1](assignment-3-1/) – Analizzare le dimensioni dell’applicazione e suggerire ottimizzazioni
  * [Esercizio 3.2](assignment-3-2/) – Analizzare un crash utilizzando i core dump (guidato)
  * [Esercizio 3.3](assignment-3-3/) – Analizzare un crash utilizzando i core dump (opzionale)

* Parte 4: **OTA e Funzionalità di Sicurezza**

  * [Lezione 4](lecture-4/) – Fondamenti di OTA, configurazione della tabella delle partizioni, bootloader sicuro, flash cifrata
  * [Esercizio 4.1](assignment-4-1/) – Modificare la tabella delle partizioni per supportare OTA
  * [Esercizio 4.2](assignment-4-2/) – Utilizzare una tabella delle partizioni personalizzata
  * [Esercizio 4.3](assignment-4-3/) – Abilitare la cifratura della flash


## Prerequisiti

Per seguire questo workshop, assicurati di soddisfare i prerequisiti elencati di seguito.

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

### Conoscenze base

* Buona conoscenza di:
  * Programmazione in C e del linker
  * Funzioni di callback e puntatori a funzione
  * Protocollo MQTT e il suo utilizzo
* Programmazione embedded
  * Flashing / Programmazione, linking
  * Familiarità con le periferiche MCU come GPIO e I2C
  * Esperienza di base con ESP-IDF
* Installazione degli strumenti (VS Code+ estensione ESP-IDF)

> Si consiglia vivamente di installare VS Code e il plugin ESP-IDF prima dell’inizio del workshop. Tuttavia, se riscontri problemi, ci sarà un po' tempo durante il primo esercizio per completare l’installazione.
<!-- 
#### Tabella di Riferimento

| Prerequisito           | Descrizione                                                                                         | Riferimento                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Tipi di memoria MCU    | Differenza tra Flash, RAM ed EEPROM                                                                 | [L. Harvie (Medium)](https://medium.com/@lanceharvieruntime/embedded-systems-memory-types-flash-vs-sram-vs-eeprom-93d0eed09086)   |
| PSRAM                  | Cos’è la PSRAM                                                                                      | [M. Hawthorne (Technipages)](https://www.technipages.com/what-is-psdram-pseudo-static-ram/)                                       |
| Periferiche seriali MCU | Differenza tra SPI, I2C, UART                                                                      | [nextpcb.com](https://www.nextpcb.com/blog/spi-i2c-uart)                                                                          |
| Plugin ESP-IDF per VS Code| Estensione ufficiale Espressif per VS Code                                                       | [Installazione vscode-esp-idf-extension](https://github.com/espressif/vscode-esp-idf-extension?tab=readme-ov-file#how-to-use)     |
| Tabella delle partizioni | Cos’è una tabella delle partizioni e perché è utile                                               | [Articolo Wikipedia sul partizionamento del disco](https://en.wikipedia.org/wiki/Disk_partitioning)                               | -->

<!-- | YAML                   | Formato di serializzazione leggibile usato per la gestione delle dipendenze tramite `idf_component.yml` | [Wikipedia](https://en.wikipedia.org/wiki/YAML), [datacamp.com](https://www.datacamp.com/blog/what-is-yaml)                     | -->

## Prossimo passo

La prima lezione si basa sul codice in [`assignment_1_1_base`](https://github.com/FBEZ-docs-and-templates/devrel-advanced-workshop-code/tree/main/assignment_1_1_base). 

Se durante le esercitazioni non riuscirai a completare un esercizio, potrai comunque continuare scaricando la soluzione appropriata secondo lo schema seguente:

```goat
assignment_1_1_base ---> assignment_1_1 ---> assignment_1_2 -+-> assignment_1_3
                                                  |
                                                  +-> assignment_2_1 ---> assignment_2_2 ---> assignment_3_1

assignment_3_2_base --------------------------------> assignment 3_2 ---> assignment 4_1 ---> assignment 4_2
```

<br>

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Anche se completi con successo tutti gli esercizi, dovrai comunque scaricare almeno `assignment_1_1_base` e `assignment_3_2_base`.
{{< /alert >}}

> Il tuo prossimo passo è **[Lezione 1](lecture-1/)**.


   <!-- * [Esercizio 4.4](assignment-4-4/) -->

## Conclusione

Congratulazioni! Sei arrivato alla fine di questo workshop. Speriamo sia stata un’esperienza utile e l’inizio di un percorso più lungo. Grazie per aver seguito il workshop avanzato su ESP-IDF.

