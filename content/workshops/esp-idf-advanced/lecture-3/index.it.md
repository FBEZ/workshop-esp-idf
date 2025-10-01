---
title: "ESP-IDF Avanzato - Lezione 3"
date: "2025-11-12"
series: ["WS00B"]
series_order: 9
showAuthor: false
summary: "In questo articolo trattiamo l’analisi delle dimensioni e i core dump. Scoprirai cosa fanno, perché sono importanti e come usarli per costruire applicazioni più efficienti e affidabili."
---

## Introduzione

In questa lezione tratteremo di due strumenti molto utili nello sviluppo embedded:

* **Analisi delle dimensioni** (size analysis): Comprendere e gestire l’uso della memoria della tua applicazione.
* **Core dump**: Catturare lo stato del sistema dopo un crash per un debug post-crash dettagliato.

## Analisi delle dimensioni

La size analysis è il processo di stima di quanta memoria flash e RAM il firmware consuma. Questo aiuta a garantire che l’applicazione rientri nelle specifiche di memoria del moduli e lasci abbastanza memoria disponibile per operazioni runtime come la gestione dei task, dei buffer e delle periferiche.

### Eseguire l’analisi delle dimensioni

Quando compili un progetto con ESP-IDF, il sistema di build fornisce automaticamente un riepilogo dell’uso della memoria. Dopo aver eseguito:

* `ESP-IDF: Build Your Project`

Vedrai un output simile a questo:

```
Total sizes:
 DRAM .data size:   1234 bytes
 DRAM .bss  size:   5678 bytes
 IRAM   size:       9101 bytes
 Flash code size:   11213 bytes
 Flash rodata size: 1415 bytes
```

Questa suddivisione dà indicazioni su dove l’applicazione sta consumando risorse. Per un'analisi più dettagliata, l'ESP-IDF offre comandi aggiuntivi:

* `idf.py size`: Fornisce un riepilogo della memoria allocata staticamente.
* `idf.py size-components`: Mostra l’uso della memoria per componente.
* `idf.py size-files`: Suddivide l’uso per file sorgente.
* `idf.py size-symbols`: Elenca l’uso della memoria a livello di simbolo (utile per individuare funzioni o variabili pesanti).

Questi strumenti aiutano a identificare i punti critici dell'uso della memoria e guidano l’ottimizzazione del codice.

Una volta conosciuto com'è utilizzata la memoria dal tuo firmware, puoi iniziare ad agire sia la configurazione che sul codice per diminuirne il consumo. 
Dopo le modifiche, ripeti la size analysis per valutarne l'impatto. 

## Core dump

Un **core dump** è uno snapshot della memoria del dispositivo e dello stato del processore al momento del crash. Include:

* Stack di chiamate di tutti i task
* Contenuto dei registri CPU
* Regioni di memoria rilevanti

Questi dati permettono agli sviluppatori di analizzare cosa è andato storto, anche dopo il reset del dispositivo. Questo rende i core dump uno strumento prezioso per diagnosticare bug difficili da riprodurre.

### Abilitare e usare i core dump

Per abilitare i core dump su un dispositivo Espressif con ESP-IDF, devi:

1. Abilitare il core dump in `menuconfig`
2. Generare e analizzare il Core Dump
   Quando si verifica un crash, il chip Espressif salva il core dump sulla flash o lo mostra su UART. Puoi analizzarlo usando:

   ```sh
   idf.py coredump-info
   ```

Questi comandi decodificano il core dump e presentano un backtrace leggibile, lo stato delle variabili e dei registri. Questo rende più semplice identificare la causa del fallimento.

I core dump sono uno strumento prezioso da usare insieme al debug.

## Conclusione

Padroneggiare l'analisi delle dimensioni e i core dump è estremamente utile per gli sviluppatori embedded. L’analisi delle dimensioni aiuta a garantire che l’applicazione rimanga nei limiti delle risorse e funzioni in modo efficiente, mentre i core dump forniscono un potente meccanismo per la diagnostica post-crash.

Integrando questi strumenti nel tuo flusso di sviluppo, sarà più semplice costruire applicazioni robuste e ad alte prestazioni.

> Passo successivo: [Esercizio 3.1](../assignment-3-1/)

> Oppure [torna al menù di navigazione](../#agenda)

## Approfondimenti

* [Guida ESP-IDF Core Dump](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/core_dump.html)
