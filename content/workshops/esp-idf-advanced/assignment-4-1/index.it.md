---
title: "ESP-IDF Avanzato - Esercizio  4.1"
date: "2025-11-12"
series: ["WS00B"]
series_order: 15
showAuthor: false
summary: "Modifica della tabella delle partizioni in Factory app, due definizioni OTA (guidato)"
---

Per eseguire l'OTA, abbiamo bisogno di una tabella delle partizioni con almeno due partizioni.

## Obiettivi dell'esercizio

1. Controllare la tabella delle partizioni corrente
2. Cambiare la tabella delle partizioni
3. Controllare la nuova tabella delle partizioni

## Controllare la tabella delle partizioni corrente

Per controllare la tabella delle partizioni attualmente caricata sul modulo è necessario:

* Leggere la flash e salvare la tabella delle partizioni in un file `.bin`
* Convertire il file `.bin` in un formato leggibile

### Leggere la flash salvando la tabella delle partizioni in un file `.bin`

* Leggi la flash con `esptool.py`:

  ```bash
  esptool.py -p <YOUR-PORT> read_flash 0x8000 0x1000 https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/partition_table.bin
  ```

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
`<YOUR-PORT>` è la stessa porta che usi per flashare il dispositivo (es. `/dev/tty.usbmodem1131101` o `COM25`).
{{< /alert >}}

Con questo comando viene creato un file `partition_table.bin`.

### Convertire in file `.bin` in un formato leggibile

* Nel terminale, usa il comando `gen_esp32part.py`.

  ```bash
  python $IDF_PATH/components/partition_table/gen_esp32part.py https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/partition_table.bin
  ```

Otterrai questo output:

```bash
Parsing binary partition input...
Verifying table...
# ESP-IDF Partition Table
# Name, Type, SubType, Offset, Size, Flags
nvs,data,nvs,0x9000,24K,
phy_init,data,phy,0xf000,4K,
factory,app,factory,0x10000,1M,
coredump,data,coredump,0x110000,64K,
```

## Cambiare la tabella delle partizioni

Ora cambiamo la tabella delle partizioni, usando l'opzione di default più appropriata da selezionare tramite `menuconfig`.

* Apri `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`<br>
  → `Partition Table` → `Factory app, two OTA definitions`

Dato che ora stiamo usando due OTA, la configurazione flash di default di 2MB non è sufficiente, quindi dobbiamo cambiarla

* Apri `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`<br>
  → `Serial Flasher Config` → `Flash Size` → `4MB`

## Controllare la nuova tabella delle partizioni

Ripetiamo gli stessi passaggi di prima:

* `esptool.py -p <YOUR-PORT> read_flash 0x8000 0x1000 https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/partition_table.bin`
* `python $IDF_PATH/components/partition_table/gen_esp32part.py https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/partition_table.bin`

* Ottenendo così 
    ```bash
    Parsing binary partition input...
    Verifying table...
    # ESP-IDF Partition Table
    # Name, Type, SubType, Offset, Size, Flags
    nvs,data,nvs,0x9000,16K,
    otadata,data,ota,0xd000,8K,
    phy_init,data,phy,0xf000,4K,
    factory,app,factory,0x10000,1M,
    ota_0,app,ota_0,0x110000,1M,
    ota_1,app,ota_1,0x210000,1M,
    ```

## Conclusione

In questo esercizio hai cambiato la tabella delle partizioni da `Single factory app, no ota` al default `Factory app, two ota definitions`.
Entrambi questi schemi di tabella delle partizioni sono forniti come valori di default da ESP-IDF.
Nel [prossimo esercizio](../assignment-4-2) creerai una tabella delle partizioni personalizzata.

> Passo successivo: [Esercizio 4.2](../assignment-4-2/)

> Oppure [torna al menù di navigazione](../#agenda)