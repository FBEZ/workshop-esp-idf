---
title: "ESP-IDF Base - Esercizio 3.2"
date: "2025-11-12"
series: ["WS00A"]
series_order: 10
showAuthor: false
summary: "Leggere i valori di umidità e temperatura dal sensore sulla scheda"
---

In questo esercizio leggerai i valori di temperatura dal sensore presente sulla scheda.

Puoi creare un nuovo progetto a partire dall'esempio `hello_world` o continuare sul codice dell'esercizio precedente.

A seconda della scheda che stai usando, segui una delle due tracce sotto. 


__Scheda con sensore a bordo__

1. Individua il part number del sensore sulla tua scheda
2. Trova il codice del driver per pilotare il sensore
3. Leggi temperatura (e umidità se disponibile) dal sensore e stamparle sulla porta seriale usando `printf`.

{{< alert icon="lightbulb" iconColor="#179299" cardColor="#9cccce">}}
Non è richiesto sviluppare il driver: concentrati sul modo più rapido per risolvere il problema e su quanto trattato nella lezione precedente.
{{< /alert>}}

__Scheda senza sensore a bordo__

1. Trova la pagina di documentazione del sensore interno del chip
2. Includi e configura il sensore interno. 
3. Leggi la temperatura interna del chip e stampa sulla porta seriale usando `printf`. 


### Suggerimento 
<details>
<summary>Mostra suggerimento sensore su scheda</summary>

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


<details>  
<summary>Mostra suggerimento sensore interno</summary>  

* Le informazioni necessarie sono sulla [Programming guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/temp_sensor.html#api-reference)

</details>


## Conclusione

Ora che sei in grado di leggere il sensore sulla scheda, sei pronto per passare all’ultimo esercizio del workshop e mettere tutto insieme.

### Prossimo passo

> Prossimo esercizio &rarr; [Esercizio 3.3](../assignment-3-3/)

> Oppure [torna al menù di navigazione](../#agenda)