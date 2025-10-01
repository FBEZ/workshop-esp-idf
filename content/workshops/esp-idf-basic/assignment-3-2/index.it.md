---
title: "ESP-IDF Base - Esercizio 3.2"
date: "2025-11-12"
series: ["WS00A"]
series_order: 10
showAuthor: false
summary: "Leggere i valori di umidità e temperatura dal sensore sulla scheda"
---

In questo esercizio leggerai i valori di umidità e temperatura dal sensore presente sulla scheda.

Puoi creare un nuovo progetto a partire dall'esempio `hello_world` o continuare sul codice dell'esercizio precedente.

Per questo esercizio, dovrai:

1. Individuare il part number del sensore sulla tua scheda
2. Trovare il codice del driver per pilotare il sensore
3. Leggere temperatura e umidità dal sensore e stamparle sulla porta seriale usando `printf`.

{{< alert icon="lightbulb" iconColor="#179299" cardColor="#9cccce">}}
Non è richiesto sviluppare il driver: concentrati sul modo più rapido per risolvere il problema e su quanto trattato nella lezione precedente.
{{< /alert>}}


### Suggerimento 
<details>
<summary>Mostra suggerimento</summary>

* L'indirizzo è sulla pagina [Github del EVK](https://github.com/esp-rs/esp-rust-board)
* Per installare una dipendenza, apri un terminale ESP-IDF:<br> 
   ```console
    > ESP-IDF: Open ESP-IDF Terminal
   ```
* Usa poi l'`idf.py`
  ```console
  idf.py add-dependency "nome_della_repo_nel_registry"
  ```
* Ricordati di modificare le impostazioni nel `menuconfig`
</details>

## Conclusione

Ora che sei in grado di leggere il sensore sulla scheda, sei pronto per passare all’ultimo esercizio del workshop e mettere tutto insieme.

### Prossimo passo

> Prossimo esercizio &rarr; [Esercizio 3.3](../assignment-3-3/)

> Oppure [torna al menù di navigazione](../#agenda)