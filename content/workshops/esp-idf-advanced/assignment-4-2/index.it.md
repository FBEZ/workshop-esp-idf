---
title: "ESP-IDF Avanzato - Esercizio 4.2"
date: "2025-11-12"
series: ["WS00B"]
series_order: 9
showAuthor: false
summary: "Creare una tabella di partizioni personalizzata"
---

In questo esercizio, imposterai una tabella di partizioni personalizzata usando VS Code.

## Obiettivi esercizio

Per prima cosa, devi abilitare la tabella di partizioni personalizzata in `menuconfig`.

* Apri `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`<br>
  → `Partition Table` → `Custom Partition Table CSV`
* Apri l'editor: `> ESP-IDF: Open Partition Table Editor UI`
* Copia la tabella di partizioni precedente
   ```bash
     # Name, Type, SubType, Offset, Size, Flags
     nvs,data,nvs,0x9000,16K,
     otadata,data,ota,0xd000,8K,
     phy_init,data,phy,0xf000,4K,
     factory,app,factory,0x10000,1M,
     ota_0,app,ota_0,0x110000,1M,
     ota_1,app,ota_1,0x210000,1M,
   ```
* Aggiungi una partizione `spiffs`

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/assignment_4_2_partition_table.webp" | absURL }}"
height=500
caption="Tabella di partizioni personalizzata"
>}}

* Compila la tabella di partizioni: `> ESP-IDF: Build Partition Table`
* Flash della tabella di partizioni: `> ESP-IDF: Flash (UART) Your Project`
* Rileggi la tabella delle partizioni.

<details>
<summary>Risultato lettura tabella delle partizioni</summary>

```bash
Parsing binary partition input...
Verifying table...
# ESP-IDF Partition Table
# Name, Type, SubType, Offset, Size, Flags
nsv,data,nvs,0x9000,16K,
otadata,data,ota,0xd000,8K,
phy_init,data,phy,0xf000,4K,
factory_app,app,factory,0x10000,1M,
ota_0,app,ota_0,0x110000,1M,
ota_1,app,ota_1,0x210000,1M,
fs,data,spiffs,0x310000,64K,
```

</details>

> Prossimo passo: [Esercizio 4.3](../assignment-4-3)

> Oppure [torna al menù di navigazione](../#agenda)