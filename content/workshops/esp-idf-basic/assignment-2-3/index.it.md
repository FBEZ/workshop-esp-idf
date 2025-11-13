---
title: "ESP-IDF Base - Esercizio 2.3 (Opzionale)"
date: "2025-11-12"
series: ["WS00A"]
series_order: 7
showAuthor: false
summary: "Aggiungere una nuova route per lampeggio programmabile (Opzionale)"
---

Questo esercizio è opzionale e dovrebbe essere svolto solo se resta del tempo prima della pausa.


Aggiungi un’altra route al server HTTP degli esercizi precedenti:

* `POST /led/flash` → accetta un JSON `{"periods": [int], "duty_cycles": [int]}` e, per ogni elemento, calcola il tempo acceso (*on-time*) e il tempo spento (*off-time*) del LED e lo controlla di conseguenza.

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Per testare un POST, hai bisogno di un'app che ti permetta di inviare richieste in maniera strutturata. Un esempio potrebbe essere [Teste](https://play.google.com/store/apps/details?id=apitester.org&hl=en-US&pli=1) ma ce ne sono molte altre. Se invece ti colleghi col computer al soft-AP, allora puoi usare lo script python riportato sotto. 
{{< /alert >}}

<details>
<summary>Script python per POST</summary>

* Apri un terminale ESP-IDF in VS Code: `ESP-IDF: Open ESP-IDF Terminal` 
<!-- * Poi installa `requests`:
    ```console
    pip install requests
    ``` -->
* Crea lo script seguente per il testing:

```python
#!/usr/bin/env python3
"""
Send LED flashing parameters to an ESP device via HTTP POST.

Endpoint:
  POST http://192.168.4.1/led/flash
  Body: {"periods": [int, ...], "duty_cycles": [int, ...]}

Each pair (period, duty_cycle) defines one blink pattern.
"""

import requests
import json

# --- Configuration ---
ESP_IP = "192.168.4.1"  # Replace with your module’s IP address
ENDPOINT = f"http://{ESP_IP}/led/flash"

# Example data:
# periods in milliseconds, duty_cycles in percentage
payload = {
    "periods": [1000, 500, 2000],
    "duty_cycles": [50, 75, 25]
}

def send_led_flash(payload):
    """Send POST request to the ESP endpoint with LED flash parameters."""
    try:
        print(f"Sending POST to {ENDPOINT} ...")
        response = requests.post(ENDPOINT, json=payload, timeout=5)
        response.raise_for_status()
        print("✅ Request successful!")
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Error communicating with the ESP:", e)

if __name__ == "__main__":
    print("Payload:", json.dumps(payload, indent=2))
    send_led_flash(payload)

```
</details>

## Traccia della soluzione

* Per prima cosa, verifica che **periods** e **duty_cycles** abbiano la stessa lunghezza e contengano solo numeri positivi.
`duty_cycles` deve contenere valori compresi tra 0 e 100.

* Poi puoi scorrere i due array e calcolare, per ogni elemento all’indice `i`, l’`on_time` e l’`off_time` del LED come segue:

    ```c
    on_time[i] = duty_cycle[i]/100 * periods[i]
    off_time[i] = periods[i]-on_time[i]
    ```

* Infine, puoi comandare il LED secondo la sequenza:

    ```c
    ON: on_time[1]
    OFF: off_time[1]
    ON: on_time[2]
    OFF: off_time[2]
    ...
    ```

## Conclusione

Se sei riuscito ad arrivare a questo punto, significa che hai acquisito una buona comprensione di una semplice implementazione di una **REST API**.
Ora puoi passare alla terza lezione, che spiega la gestione delle librerie esterne e l’uso dei componenti presenti nel **component registry**.

### Prossimo passo

> Prossima lezione → [Lezione 3](../lecture-3/)

> Oppure [torna al menù di navigazione](../#agenda)