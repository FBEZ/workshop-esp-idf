---
title: "ESP-IDF Base - Lezione 3"
date: "2025-11-12"
series: ["WS00A"]
series_order: 8
showAuthor: false
summary: "In questa lezione vedremo come includere librerie che fanno parte dell'ESP-IDF, librerie esterne e componenti dal ESP component registry"
---

## Introduzione

Come abbiamo visto in precedenza, ESP-IDF contiene diverse librerie, da FreeRTOS (il sistema operativo real time) ai driver delle periferiche e alle librerie dei protocolli.
Per questioni di spazio, includere librerie per ogni possibile protocollo, algoritmo o driver all’interno di ESP-IDF non è possibile.

Se hai bisogno di un protocollo specifico, è molto probabile che si trovi su Github l'implementazione in C. In questo caso, la sfida sarà portarlo in ESP-IDF, occupandosi di individuare tutte le dipendenze e informare il build system di quali file debbano essere compilati e linkati.

Per risolvere questi problemi, Espressif ha sviluppato un **sistema di componenti** simile ai package manager delle distribuzioni GNU/Linux.
I componenti permettono di gestire sia le dipendenze che il linker e per usare un component ESP-IDF è sufficiente includere l'header file per iniziare ad usarlo. 

Come nel caso dei pacchetti Linux, esiste anche un **component manager** e un **component registry**, dove puoi trovare tutti i pacchetti ufficiali di Espressif. Una volta inclusi i componenti, lo strumento `idf.py` scaricherà il componente e preparerà l’ambiente per il suo utilizzo.

Per ulteriori informazioni, consigliamo di guardare il talk [DevCon23 - Developing, Publishing, and Maintaining Components for ESP-IDF](https://www.youtube.com/watch?v=D86gQ4knUnc).

{{< youtube D86gQ4knUnc >}}

In questa lezione esploreremo le differenze tra l’uso delle librerie integrate e quelle fornite dal component registry. Vedremo anche come creare un componente per rendere il codice riutilizzabile.

In particolare, vedremo come:

1. Includere e usare le librerie `gpio` e `i2c` (incluse nell'ESP-IDF)
2. Usare il componente `button` dal registry
3. Creare un nuovo componente

Durante gli esercizi, l’obiettivo sarà controllare il LED e il sensore I2C (SHTC3) sulla scheda (vedi Fig. 1).

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_3_led_gpio.webp"
caption="Fig.1 - GPIO collegato al LED"

>}}

## Librerie incluse

Vediamo come usare le librerie incluse nell'ESP-IDF. Di solito ciò comporta tre passaggi principali:

1. Informare il build system della libreria *(includere l’header file e aggiornare `CMakeLists.txt`)*
2. Configurare le impostazioni della libreria
3. Usare la libreria chiamando le sue funzioni

### GPIO

Un GPIO (General-Purpose Input/Output) è un’interfaccia digitale su un microcontrollore o processore che permette di leggere segnali in ingresso (come pulsanti) o controllare dispositivi in uscita (come LED) tramite pin programmabili. I pin possono essere configurati singolarmente come input o output.

Sulla nostra scheda, abbiamo un LED collegato al GPIO8 (vedi Fig. 1) che useremo per l’esempio.

#### Inclusione della libreria

Per includere la libreria `gpio`, dobbiamo prima includere l’header e informare il build system dove trovarlo.

```c
#include "driver/gpio.h"
```

e poi aggiungere a `CMakeLists.txt`:

```cmake
REQUIRES esp_driver_gpio
```

Nota che il file header e il percorso richiesto possono essere diversi: quando includi una libreria, verifica sempre la [programming guide](https://docs.espressif.com/projects/esp-idf/en/v5.4.1/esp32c3/index.html).

Per trovare il path da usare nella direttiva `REQUIRES` devi seguire i seguenti passi:

* Scegliere il core usato (nel nostro caso ESP32-C3) nel riquadro in alto a sinistra. 
* Trovare la pagina della periferica (GPIO)
* Trovare la sezione [API Reference](https://docs.espressif.com/projects/esp-idf/en/v5.4.1/esp32c3/api-reference/peripherals/gpio.html#api-reference-normal-gpio)

#### Configurazione

Le periferiche hanno molte impostazioni (input/output, frequenza, ecc.), di conseguenza è sempre necessario configurarle prima dell’uso.

Per il GPIO, una configurazione base è:

```c
// inizializza la struttura a zero
gpio_config_t io_conf = {};
// disabilita interrupt
io_conf.intr_type = GPIO_INTR_DISABLE;
// modalità output
io_conf.mode = GPIO_MODE_OUTPUT;
// bit mask dei pin da configurare, es. GPIO18/19
io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
// disabilita pull-down
io_conf.pull_down_en = 0;
// disabilita pull-up
io_conf.pull_up_en = 0;
// applica la configurazione al GPIO
gpio_config(&io_conf);
```

In questo workshop useremo i GPIO come output. Non parleremo quindi di:

* Interrupt (attivare una funzione quando l’input cambia)
* Pull-up e pull-down (valore di default dell’input)

L’unico campo che ha bisogno di spiegazione è il `pin_bit_mask`.
La configurazione si applica all’intera periferica GPIO. Per poter applicare una configurazione un sottoinsieme di pin, bisogna specificarli tramite una [bit mask](https://en.wikipedia.org/wiki/Mask_%28computing%29).

Supponiamo di voler configurare il pin 10. La `bit mask` può essere generata in questo modo:

```c
#define GPIO_OUTPUT_LED   10
#define GPIO_OUTPUT_PIN_SEL  (1ULL<<GPIO_OUTPUT_LED) // es. 0000000000000000000000000000010000000000
```

Nel caso in cui volessimo invece applicare la configurazione a più GPIO, si usa l’operatore `OR`:

```c
#define GPIO_OUTPUT_LED   10
#define GPIO_OUTPUT_EXAMPLE   12
#define GPIO_OUTPUT_PIN_SEL  ((1ULL<<GPIO_OUTPUT_LED) | (GPIO_OUTPUT_EXAMPLE)) // es. 0000000000000000000000000001010000000000
```

#### Uso

Una volta configurato la periferica, possiamo usare la funzione [`gpio_set_level`](https://docs.espressif.com/projects/esp-idf/en/v5.4.1/esp32c3/api-reference/peripherals/gpio.html#_CPPv414gpio_set_level10gpio_num_t8uint32_t) per impostare l’uscita a `0` o `1`.

```c
gpio_set_level(GPIO_OUTPUT_LED, 1); // accende il LED
gpio_set_level(GPIO_OUTPUT_LED, 0); // spegne il LED
```

### I2C

I2C (Inter-Integrated Circuit) è un protocollo di comunicazione che utilizza solo due fili (SDA per i dati e SCL per il clock) per trasmettere dati tra dispositivi.
Di solito serve a collegare un microcontrollore a un sensore o attuatore esterno.
L'I2C permette a più periferiche di comunicare con un microcontrollore usando gli stessi fili ed indirizzi univoci, garantendo interconnessioni efficienti e scalabili.

#### Inclusione della libreria

Consultando la [programming guide](https://docs.espressif.com/projects/esp-idf/en/v5.4.1/esp32c3/api-reference/peripherals/i2c.html#api-reference) otteniamo l’header:

```c
#include "driver/i2c_master.h"
```

e il nome per la direttiva `REQUIRES` del `CMakeLists.txt`:

```cmake
REQUIRES esp_driver_i2c
```

#### Configurazione

La configurazione per questa periferica ha la forma seguente:

```c
i2c_master_bus_config_t bus_config = {
    .i2c_port = I2C_NUM_0,
    .sda_io_num = I2C_MASTER_SDA_IO,
    .scl_io_num = I2C_MASTER_SCL_IO,
    .clk_source = I2C_CLK_SRC_DEFAULT,
    .glitch_ignore_cnt = 7,
    .flags.enable_internal_pullup = true,
};
i2c_new_master_bus(&bus_config, bus_handle);

i2c_device_config_t dev_config = {
    .dev_addr_length = I2C_ADDR_BIT_LEN_7,
    .device_address = SHTC3_SENSOR_ADDR,
    .scl_speed_hz = 400000,
};
i2c_master_bus_add_device(*bus_handle, &dev_config, dev_handle);
```

I valori per la nostra scheda sono (vedi Fig. 1):

```c
#define I2C_MASTER_SDA_IO 7
#define I2C_MASTER_SCL_IO 8
#define SHTC3_SENSOR_ADDR 0x70
```

Le altre macro sono definite internamente.

## Component Registry

### Usare un componente dal registry - button

Per vedere come gestire una libreria esterna, utilizzeremo il componente `button` attraverso il component registry. 

* Vai al [component registry](https://components.espressif.com/)
* Cerca il componente button ([espressif/button](https://components.espressif.com/components/espressif/button/versions/4.1.3))
* Copia l’istruzione a sinistra (vedi Fig.2) - `idf.py add-dependency "espressif/button^4.1.3"`
* In VS Code: `> ESP-IDF: Open ESP-IDF Terminal` e incolla il comando

{{< figure
default=true
src="/workshops/esp-idf-basic/assets//lec_3_registry.webp"
caption="Fig.2 - Componente espressif/button"

>}}

Riceverai un messaggio simile a:

```bash
Executing action: add-dependency
NOTICE: Successfully added dependency "espressif/button": "^4.1.3" to component "main"
NOTICE: If you want to make additional changes to the manifest file at path <user_path>/blink/main/idf_component.yml manually, please refer to the documentation: https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/manifest_file.html
```

Un nuovo file `idf_component.yml` è stato creato nel progetto con il seguente contenuto:

```yaml
dependencies:
  espressif/led_strip: ^2.4.1
  espressif/button: ^4.1.3
```

Puoi aggiungere dipendenze direttamente in questo file, ma è consigliato usare l’utility `idf.py add-dependency`.

Per usare il componente, includi l’header appropriato e chiama le funzioni indicate nella documentazione.

### Creare un componente

Per istruzioni dettagliate su come creare un componente tramite CLI, puoi consultare l’articolo [How to create an ESP-IDF component](https://developer.espressif.com/blog/2024/12/how-to-create-an-esp-idf-component/) sul Developer Portal di Espressif.

In questa lezione vedremo invece come creare un componente con VS Code.
I passi da seguire sono simili a quelli via CLI:

1. Crea un nuovo progetto
2. Crea un nuovo componente con `> ESP-IDF: Create New ESP-IDF Component`
3. Assegna un nome al componente (es. `led_toggle`)

Il progetto conterrà ora una cartella `components` con tutti i file necessari:

```bash
.
└── project_folder/
    ├── components/
    │   └── led_toggle/
    │       ├── include/
    │       │   └── led_toggle.h
    │       ├── CMakeList.txt
    │       └── led_toggle.c
    ├── main
    └── build
```

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Ogni volta che crei o scarichi un componente, è necessario eseguire un **full clean** del progetto chiamando:

`> ESP-IDF: Full Clean Project`
{{< /alert >}}

Puoi quindi includere il tuo componente nel file principale come `led_toggle.h`.

## Conclusione

In questa breve lezione abbiamo esplorato due principali modalità per includere librerie esterne: direttamente tramite `


### Prossimo passo

> Prossimo passo: [Esercizio 3.1](../assignment-3-1/)

> Oppure [torna al menù di navigazione](../#agenda)