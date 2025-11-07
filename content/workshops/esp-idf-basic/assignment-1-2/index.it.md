---
title: "ESP-IDF Base - Esercizio 1.2"
date: "2025-11-12"
series: ["WS00A"]
series_order: 3
showAuthor: false
summary: "Creare un nuovo progetto basato sull'esempio `blink` e far lampeggiare il led sulla scheda."
---


## Obiettivi dell'esercizio

1. Creazione di un nuovo progetto a partire dall'esempio  `blink`
2. Modifica del GPIO di uscita di default via `menuconfig`
3. Lampeggio del LED della scheda

## Traccia della soluzione

In questo esercizio creerai un nuovo progetto partendo da un altro esempio della cartella `get_started` &rarr; `blink`.

Nell’esempio `blink`, è necessario specificare il GPIO a cui è collegato il LED. Il valore predefinito è `GPIO8`, ma sulla tua scheda è diverso. Dovrai modificare questo valore di configurazione tramite `menuconfig`.

* Crea il progetto dall’esempio come fatto nell’esercizio precedente.
* Modifica il numero del GPIO dell’esempio tramite `menuconfig`:

  * Trova il GPIO a cui è collegato il LED sulla tua scheda.
  * `> ESP-IDF: SDK Configuration Editor (menuconfig)` → `Example Configuration` → `Blink GPIO number`
* Compila, programma e monitora l’esempio.
* Verifica che il LED lampeggi. La porta di uscita è corretta? Consulta [lo schema della scheda](https://github.com/esp-rs/esp-rust-board/blob/master/hardware/esp-rust-board/schematic/esp-rust-board.pdf) per verificarlo.

{{< figure
default=true
src="/workshop-esp-idf/workshops/esp-idf-basic/assets/esp32_c3-_devkit_rust_1_top.webp"
height=500
caption="Fig.1 - Vista superiore della scheda"

>}}

## Attività opzionale

* (Bonus) Rinomina il file principale in `hello_led_main.c` e la cartella del progetto in `hello_led`. Hai riscontrato errori?

  * Dove si trova il problema?


<details>
<summary>Soluzione</summary>

Il linker non sa di dover compilare anche il file `hello_led_main.c`. È necessario cambiare il file `CMakefile.txt` che contiene le informazioni dei file da includere. 

Affronteremo l'argomento del build system nel workshop ESP-IDF avanzato. Per il momento, la soluzione consiste nel cambiare l'istruzione `idf_component_register` in `CMakelists.txt`. 

```console
idf_component_register(SRCS "hello_led_main.c"
                       INCLUDE_DIRS ".")
```
</details>
 
## Conclusione

Ora hai una buona comprensione del processo di creazione, compilazione e caricamento sulla memoria di un progetto ESP-IDF. 
Nella prossima lezione, ci concentreremo su quello che solitamente è il tema principale di un’applicazione Espressif — *la connettività*.

### Prossimo passo

> Prossima lezione → **[Lezione 2](../lecture-2/)**

> Oppure [torna al menù di navigazione](../#agenda)