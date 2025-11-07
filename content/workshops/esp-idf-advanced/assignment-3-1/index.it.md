---
title: "ESP-IDF Avanzato - Esercizio 3.1"
date: "2025-11-12"
series: ["WS00B"]
series_order: 10
showAuthor: false
summary: "Ridurre la dimensione del binario lavorando sulla configurazione. (guidato)"
---
In questo Esercizio, analizzerai la dimensione dell'immagine binaria e ottimizzerai l'uso della memoria della tua applicazione.

## Obiettivi dell'esercizio

1. Compilare il progetto originale per individuare eventuali sezioni sovradimensionate o sospette (es. .text, .data, .rodata) che potrebbero nascondere codice non ottimizzato.
2. Modificare la configurazione per ridurre la dimensione.
3. Ricompilare il progetto per verificare i miglioramenti.

## Compilare il progetto originale

* Riapri il codice dell'ultimo esercizio (che può essere indifferentemente il 2.1 o il 2.2)
* `> ESP-IDF: Full Clean Project`
* `> ESP-IDF: Build Your Project`

Otterrai la tabella riepilogativa di Fig.1 per l'immagine binaria.
{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/assignment_3_1_size_before.webp" | absURL }}"
height=300
caption="Fig.1 - Analisi della dimensione"
>}}

#### Rimozione dei log

* Rimuovere l'output dei log nel `menuconfig`<br>
  _Se non ricordi come fare, dai un'occhiata all'[Esercizio 1.3](../assignment-1-3/#modificare-la-configurazione-in-menuconfig)_
* `> ESP-IDF: Build Your Project` 

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/assignment_3_1_size_after_log.webp" | absURL }}"
height=500
caption="Fig.2 - Calcolo della dimensione dopo aver rimosso i log"
>}}

La dimensione del binario è diminuita di 77kb rispetto a prima.

#### Certificate Bundle

* Apri di nuovo il `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`
* Deseleziona `Certificate Bundle` → `Enable trusted root certificate bundle`
* `> ESP-IDF: Build Your Project`

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/assignment_3_1_size_after_bundle.webp" | absURL }}"
height=500
caption="Fig.3 - Calcolo della dimensione dopo aver rimosso il certificate bundle"
>}}

#### Opzioni MQTT non usate

* Aprire menuconfig: `> ESP-IDF: SDK Configuration Editor (menuconfig)`
* Deselezionare `ESP-MQTT Configurations` → `Enable MQTT over SSL`
* Deselezionare `ESP-MQTT Configurations` → `Enable MQTT over Websocket`
* `> ESP-IDF: Build Your Project`

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/assignment_3_1_size_after_ssl.webp" | absURL }}"
height=500
caption="Fig.4 - Calcolo della dimensione dopo aver rimosso il supporto MQTT SSL e Websocket"
>}}

Abbiamo guadagnato altri 6,7kb.

## Conclusione

In questo esercizio, abbiamo visto come verificare la dimensione del binario e come utilizzare il `menuconfig` per rimuovere opzioni non utilizzate al fine di migliorare l'uso della memoria della nostra applicazione.

> Prossimo passo: [Esercizio 3.2](../assignment-3-2/)

> Oppure [torna al menù di navigazione](../#agenda)