---
title: "ESP-IDF Base - Esercizio 3.3"
date: "2025-11-12"
series: ["WS00A"]
series_order: 11
showAuthor: false
summary: "Aggiungere la route al server HTTP per mostrare da remoto i dati ambientali"
---


In questo esercizio, combinerai tutto ciò che hai fatto fino ad ora aggiungendo le due route seguenti al tuo server HTTP.


1. `GET /environment/` che restituisce un oggetto `json`:

```json
{
   'temperature': float,
   'humidity': float
}
```

1. (Opzionale) `POST /startblink/` che fa lampeggiare il LED in base alla lettura della temperatura:

   * Lampeggia il numero delle decine (es. 29 gradi → 2) con 400ms acceso e 200ms spento
   * Pausa di 1 secondo
   * Lampeggia il numero delle unità (es. 29 gradi → 9) con 400ms acceso e 200ms spento


## Conclusione

Hai creato una semplice applicazione IoT, combinando la lettura dei sensori con la connettività HTTP, permettendo a servizi esterni di interagire con la tua applicazione.

### Prossimo passo

> Prossimo passo → [Conclusione](../#conclusione)

> Oppure [torna al menù di navigazione](../#agenda)