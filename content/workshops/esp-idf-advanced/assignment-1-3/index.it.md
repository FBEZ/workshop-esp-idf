---
title: "ESP-IDF Avanzato - Esercizio 1.3"
date: "2025-11-12"
series: ["WS00B"]
series_order: 5
showAuthor: false
summary: "Supporto per configurazioni multiple tramite sdkconfig (Guidato)"
---

In questo esercizio, creerai due versioni di `sdkconfig`, una di produzione e una di debug.

L’unica differenza tra le due sarà il logging: la versione debug mostrerà tutti i log, mentre quella di produzione li sopprimerà tutti.

## Obiettivi del compito

Il tuo progetto deve avere i seguenti file di configurazione:

1. `sdkconfig.defaults`: contenente solo la configurazione di target `esp32-c3`
2. `sdkconfig.prod`: contenente la configurazione per la soppressione dei log (sia dell’app che del boot loader)
3. `sdkconfig.debug`: contenente la configurazione per abilitare i log
4. file `profile` per semplificare il comando di build

La struttura finale della cartella del progetto sarà

```bash
.
|-- main
|   |-- CMakeLists.txt
|   |-- app_main.c
|   `-- idf_component.yml
|-- profiles
|   |-- debug
|   `-- prod
|-- sdkconfig
|-- sdkconfig.debug
|-- sdkconfig.defaults
|-- sdkconfig.old
`-- sdkconfig.prod
```

## Passaggi dell'esercizio

1. Creare la versione di produzione di `sdkconfig` (guidato)
2. Creare un file profile (guidato)
3. Creare la versione debug di `sdkconfig`

### Creare la versione di produzione (guidato)

Per creare la configurazione di debug, dobbiamo prima trovare le impostazioni dei log.

#### Modificare la configurazione in `menuconfig`

* Apri il `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`<br>
  * Nel campo di ricerca, inserisci "log" 
  * Deseleziona i campi seguenti<br>

    * Bootloader Config &rarr; Bootloader log verbosity
    * Log → Log Level &rarr; Default log verbosity

#### Creare il file `sdkconfig.prod`

Il modo più semplice per trovare i nomi delle configurazioni modificate è eseguire lo strumento `save-defconfig`, che genererà un file `sdkconfig.defaults` contenente __solo i parametri modificati__.

* `ESP-IDF: Save Default Config File (save-defconfig)`

* Apri il nuovo `sdkconfig.defaults` <br>

  ```bash
  CONFIG_LOG_DEFAULT_LEVEL_NONE=y
  CONFIG_BOOTLOADER_LOG_LEVEL_NONE=y
  ```

* Copia le due configurazioni e incollale in un file `sdkconfig.prod`

#### Compilazione

* Apri un terminale: `> ESP-IDF: Open ESP-IDF Terminal`
* Per compilare la versione di produzione digita
  ```bash
  idf.py -B build-production -DSDKCONFIG=build-production/sdkconfig -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.prod" build
  ```

Questo creerà una cartella `build-production` per la versione "production".

* Per caricare il progetto sul modulo, digita:

  ```bash
  idf.py -B build-debug -p <YOUR_PORT> flash monitor
  ```

### Creare file Profile

Per semplificare il processo creeremo un file *profile*.

* Crea una cartella `profiles`
* Crea un file `prod` all’interno della cartella
* Aggiungi i parametri CLI<br>

  ```bash
  -B build-production -DSDKCONFIG=build-production/sdkconfig -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.prod"
  ```

Ora possiamo compilare la versione di produzione usando

```bash
idf.py @profiles/prod build
```

### Versione Debug

Ora puoi fare lo stesso per la configurazione di debug.
Per questo passaggio del compito, devi creare e scrivere:

1. `sdkconfig.debug`
2. `profiles/debug`

## Codice soluzione del compito

<details>
<summary>Mostra codice soluzione</summary>

**`skdconfig.defaults`**

```bash
# This file was generated using idf.py save-defconfig. It can be edited manually.
# Espressif IoT Development Framework (ESP-IDF) 5.4.2 Project Minimal Configuration
#
CONFIG_IDF_TARGET="esp32c3"
```

**`skdconfig.prod`**

```bash
CONFIG_LOG_DEFAULT_LEVEL_NONE=y
CONFIG_BOOTLOADER_LOG_LEVEL_NONE=y
```

**`skdconfig.debug`**

```bash
CONFIG_LOG_DEFAULT_LEVEL_INFO=y
```

</details>

Puoi trovare l’intero progetto di soluzione nella cartella [assignment_1_3](https://github.com/FBEZ-docs-and-templates/devrel-advanced-workshop-code/tree/main/assignment_1_3) del repository GitHub.

> Passo successivo: [Lezione 2](../lecture-2/)

> Oppure [torna al menù di navigazione](../#agenda)