---
title: "ESP-IDF Base - Esercizio 1.1"
date: "2025-08-05"
series: ["WS00A"]
series_order: 2
showAuthor: false
---

> Creare un nuovo progetto da `hello_world` e cambiare il testo mostrato (Guidato)

## Passi dell'esercizio

In questo esercizio
1. Creerai un progetto a partire dall'esempio `hello_world`
2. Cambierai il testo di uscita. 

Prima di iniziare, assicurati di aver installato tutto il necessario. 

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
In questo workshop utilizzeremo l’estensione ESP-IDF per VS Code.
Se non l’hai ancora installata, segui [queste istruzioni](../esp-idf-setup/). 
{{< /alert >}}

## Passo 1: Creare e testare un progetto da un esempio

In questa sezione, impareremo a:

1. Creare un nuovo progetto a partire da un esempio
2. Compilare il progetto
3. Programmare il modulo e monitorare l'uscita

Tieni presente che la maggior parte dei comandi in VS Code vengono eseguiti tramite la __palette dei comandi__, che puoi aprire premendo `Ctrl`+`Shift`+`P` (oppure `Cmd`+`Shift`+`P` su macOS).

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
In questa guida, i comandi da digitare nella __palette dei comandi__ sono contrassegnati con il simbolo __`>`__.
Di solito è sufficiente scrivere alcune lettere del comando: comparirà un menu a discesa con le opzioni disponibili e basterà cliccare quella richiesta. 
{{< /alert >}}


### Creare un nuovo progetto a partire da un esempio

1. Apri VS Code
2. `> ESP-IDF: Show Example Project`
3. (Se richiesto) Seleziona la versione di ESP-IDF
4. Clicca su `get_started` → `hello_world`
5. Nella nuova scheda, clicca sul pulsante `Select Location for Creating "hello_world" Example`

{{< figure
default=true
src="{{ "/workshops/esp-idf-basic/assets/ass1_1_new_project.webp" | absURL }}"
height=500
caption="Fig.1 - Creazione di un nuovo progetto da esempio"

>}}

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Si aprirà un pop-up che vi chiede se vi fidate dell'autore della cartella. Si tratta di una configurazione utile quando si usa `git`, in questo caso è poco rilevante. 
Clicca __sì__ per proseguire. 
{{< /alert >}}


Si aprirà una nuova finestra con la seguente struttura di file:

{{< figure
default=true
src="{{ "/workshops/esp-idf-basic/assets/ass1_1_hello_world_files.webp" | absURL }}"
height=500
caption="Fig.2 - File dell’esempio `hello_world`"

>}}

Per ora puoi ignorare le cartelle `.vscode`, `.devcontainer` e `build`.
Lavorerai principalmente sul file `main/hello_world_main.c`.


### Compilare il progetto

Per compilare (*build*) il progetto, devi prima indicare al compilatore quale SoC (detto *target*) stai usando. Puoi farlo direttamente dall’IDE:

* `> ESP-IDF: Set Espressif Device Target`
* Nel menu a discesa, scegli `esp32c3` → `ESP32-C3 chip (via builtin USB-JTAG)`

Ora sei pronto per compilare il progetto:

* `> ESP-IDF: Build Your Project`<br>
  *Puoi anche cliccare sulla piccola icona 🔧 nella barra inferiore*

Nella parte inferiore dell’IDE si aprirà un terminale che mostrerà il risultato della compilazione e le dimensioni del file binario generato.

{{< figure
default=true
src="{{ "/workshops/esp-idf-basic/assets/ass1_1_compilation_result.webp" | absURL }}"
height=500
caption="Fig.3 - Risultato della compilazione"

>}}

{{< alert icon="lightbulb" iconColor="#179299" cardColor="#9cccce">}}
Se riscontri problemi in questa fase, può essere utile eseguire una pulizia completa del progetto con il comando
`> ESP-IDF: Full clean project`.
{{< /alert >}}

### Programmare il modulo e monitorare l'uscita

Per vedere il firmware in esecuzione, devi caricarlo sul dispositivo (*flash*) e leggere l’output emesso sulla porta seriale (*monitor*).

* Collega la scheda al computer (se non l'hai già fatto)
* Verifica che il dispositivo venga riconosciuto<br>
   _Se non sai come, controlla le seguenti pagine [windows](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-windows) - [linux/macos](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-linux-and-macos)_
* Prendi nota del nome della porta a cui è stato assegnato il dispositivo Espressif
   * Su **Windows** il nome della porta inizia con `COM`
   * Su **Linux/macOS** il nome della porta inizia con `tty` o `ttyUSB`
* Imposta la porta su VS Code <br>
   `>ESP-IDF: Select Port to Use (COM, tty, usbserial)`

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
Se riscontri problemi, consulta la guida [Establish Serial Connection with ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#establish-serial-connection-with-esp32).
{{< /alert >}}

Ora puoi caricare il programma sul modulo e avviare il monitor: 

* `> ESP-IDF: Build, Flash and Start a Monitor on Your Device`
* Nel menù a tendina, seleziona `UART`

Nel terminale dovresti vedere la stringa `Hello World!` e il conto alla rovescia prima del reset.

<!-- {{< asciinema
key="hello_world"
idleTimeLimit="2"
speed="1.5"
poster="npt:0:09"

>}} -->

## Passo 2: Modificare il testo di output

Trova la stringa di output e modificala in `Hello LED`.

## Soluzione Esercizio

<details>
<summary>Codice Esercizio</summary>

`main/hello_world_main.c`
```c
/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

void app_main(void)
{
    printf("Hello LED!\n");

    /* Print chip information */
    esp_chip_info_t chip_info;
    uint32_t flash_size;
    esp_chip_info(&chip_info);
    printf("This is %s chip with %d CPU core(s), %s%s%s%s, ",
           CONFIG_IDF_TARGET,
           chip_info.cores,
           (chip_info.features & CHIP_FEATURE_WIFI_BGN) ? "WiFi/" : "",
           (chip_info.features & CHIP_FEATURE_BT) ? "BT" : "",
           (chip_info.features & CHIP_FEATURE_BLE) ? "BLE" : "",
           (chip_info.features & CHIP_FEATURE_IEEE802154) ? ", 802.15.4 (Zigbee/Thread)" : "");

    unsigned major_rev = chip_info.revision / 100;
    unsigned minor_rev = chip_info.revision % 100;
    printf("silicon revision v%d.%d, ", major_rev, minor_rev);
    if(esp_flash_get_size(NULL, &flash_size) != ESP_OK) {
        printf("Get flash size failed");
        return;
    }

    printf("%" PRIu32 "MB %s flash\n", flash_size / (uint32_t)(1024 * 1024),
           (chip_info.features & CHIP_FEATURE_EMB_FLASH) ? "embedded" : "external");

    printf("Minimum free heap size: %" PRIu32 " bytes\n", esp_get_minimum_free_heap_size());

    for (int i = 10; i >= 0; i--) {
        printf("Restarting in %d seconds...\n", i);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    printf("Restarting now.\n");
    fflush(stdout);
    esp_restart();
}
```
</details>


### Prossimo passo

> Prossimo esercizio &rarr; [Esercizio 1.2](../assignment-1-2/)

> Oppure [torna al menù di navigazione](../#agenda)