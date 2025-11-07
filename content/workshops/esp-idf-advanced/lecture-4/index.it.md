---
title: "ESP-IDF Avanzato - Lezione 4"
date: "2025-11-12"
series: ["WS00B"]
series_order: 13
showAuthor: false
summary: "In questo articolo esploriamo le funzionalità di sicurezza: aggiornamento OTA, cifratura della flash e bootloader sicuro"
---

## Introduzione

Con la crescente diffusione dei dispositivi IoT nelle abitazioni, i sistemi connessi gestiscono sempre più spesso dati personali, controllano processi fisici e operano in ambienti non affidabili, rendendoli obiettivi interessanti per gli hacker.

In risposta a questi rischi, nuove normative come il Radio Equipment Directive Delegated Act (RED DA) dell’UE stanno alzando gli standard di sicurezza per l’IoT, richiedendo ai produttori di implementare protezioni più solide già in fase di progettazione.

Per soddisfare queste esigenze, tre tecnologie sono diventate la base della sicurezza moderna per l’IoT: **aggiornamenti over-the-air (OTA)**, **cifratura della flash** e **bootloader sicuro**.

* **Aggiornamenti OTA**: consentono ai dispositivi di ricevere aggiornamenti firmware da remoto, permettendo patch di sicurezza e miglioramenti delle funzionalità senza necessità di accesso fisico. Questo è cruciale per mantenere l’integrità del dispositivo durante tutto il suo ciclo di vita, soprattutto una volta che i prodotti sono distribuiti sul campo.

* **Cifratura della flash**: protegge i dati memorizzati nella memoria flash del dispositivo. Questo garantisce che le informazioni sensibili (come chiavi crittografiche o dati degli utenti) rimangano inaccessibili anche se un attaccante ottiene l’accesso fisico al dispositivo.

* **Bootloader sicuro**: verifica l’integrità e l’autenticità del firmware prima dell’esecuzione. Controllando le firme digitali durante il processo di avvio, il secure bootloader impedisce l’esecuzione di codice non autorizzato o dannoso.

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Nei seguenti esercizi, abiliterete queste funzionalità direttamente sul EVK. Se non vi sentite sicuri, potete seguire l’articolo del developer portal sull'[emulazione delle funzionalità di sicurezza usando QEMU](https://developer.espressif.com/blog/trying-out-esp32-c3s-security-features-using-qemu/).
{{< /alert >}}

Queste tre funzionalità costituiscono uno strato di sicurezza fondamentale, aiutando gli sviluppatori a realizzare dispositivi conformi alle nuove normative.

Nel seguito, vedremo ciascuna di queste funzionalità separatamente. Per usare l’OTA, bisogna prima modificare la tabella delle partizioni. Per questo motivo, prima di iniziare, dobbiamo dedicare qualche parola alle tabelle delle partizioni.

## Tabelle delle partizioni

La tabella delle partizioni definisce come la memoria flash è organizzata, specificando a che indirizzi sono memorizzate applicazioni, dati, filesystem e altre risorse. Questa separazione logica permette agli sviluppatori di gestire firmware, dati persistenti e meccanismi di aggiornamento in modo efficiente.

ESP-IDF utilizza la tabella delle partizioni perché consente:

* **Separazione di codice e dati:** Applicazioni e dati persistenti sono isolati, permettendo aggiornamenti firmware senza cancellare i dati dell’utente.
* **Aggiornamenti OTA:** Supporto di più partizioni applicative e gestione dei dati OTA per aggiornamenti firmware remoti.
* **Storage flessibile:** Supporto di filesystem e di regioni personalizzate per certificati, log o configurazioni.

### Struttura e posizione

La tabella delle partizioni è tipicamente caricata all’offset `0x8000` nella flash del dispositivo e occupa `0xC00` byte, supportando fino a 95 voci e includendo un checksum MD5 per la verifica dell’integrità dei dati caricati. 
La tabella stessa occupa un intero settore flash da 4 KB, quindi qualsiasi partizione successiva deve iniziare almeno all’offset `0x9000`. Ogni voce della tabella include un nome (label), un tipo (come `app` o `data`), un sottotipo, un offset e la dimensione nella memoria flash.

### Schemi di partizioni predefiniti

ESP-IDF fornisce diverse tabelle delle partizioni predefinite, selezionabili tramite `menuconfig`:

* **Single factory app, no OTA**: Contiene una singola partizione per l'applicazione e partizioni dati di base (NVS, PHY init).
* **Factory app, two OTA definitions**: Aggiunge il supporto agli aggiornamenti over-the-air (OTA), con due partizioni app OTA e uno slot dati OTA. Useremo questa tabella delle partizioni predefinita nell’[esercizio 4.1](../assignment-4-1/)

Ad esempio, lo schema "Factory app, two OTA definitions" appare così:

```
Name      Type   SubType  Offset    Size
nvs       data   nvs      0x9000    0x4000
otadata   data   ota      0xd000    0x2000
phy_init  data   phy      0xf000    0x1000
factory   app    factory  0x10000   1M
ota_0     app    ota_0    0x110000  1M
ota_1     app    ota_1    0x210000  1M
```

Il bootloader utilizza la tabella delle partizioni per individuare l’applicazione da avviare e le aree dati per NVS, calibrazione PHY e gestione OTA.

### Tabella delle partizioni personalizzata

Per applicazioni avanzate, gli sviluppatori possono definire tabelle delle partizioni personalizzate in formato CSV. Questo permette di aggiungere partizioni extra, come spazio NVS aggiuntivo oppure un  filesystem (SPIFFS o FAT). Il CSV personalizzato è specificato nella configurazione del progetto e gli strumenti ESP-IDF lo trasformano in tabella di partizione e lo utilizzano di conseguenza.

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
Nel caso si usi una tabella delle partizioni personalizzata, conviene aumentare la dimensione delle partizioni OTA al massimo spazio disponibile, una volte note le dimensioni delle altre partizioni: in questo modo si avrà più spazio disponibile per gli aggiornamenti OTA futuri. 
{{< /alert >}}

Testeremo questa opzione nell’[esercizio 4.2](../assignment-4-2/).

## Aggiornamenti Over-the-Air (OTA) sui dispositivi Espressif

Gli aggiornamenti Over-the-Air (OTA) consentono di aggiornare il firmware dei dispositivi embedded da remoto senza necessità di accesso fisico. Questa capacità è particolarmente importante nelle implementazioni IoT, dove i dispositivi sono spesso presenti su aree ampie, possibilmente difficili da raggiungere. L’OTA assicura che i dispositivi rimangano aggiornati con le ultime funzionalità, correzioni dei bug e patch di sicurezza anche dopo la vendita.

Durante il processo OTA, il dispositivo Espressif scarica il firmware da una posizione specificata, come illustrato in Fig.1.

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/lecture_4_ota_diagram.webp" | absURL }}"
width=350
caption="Fig.1 -- Diagramma base OTA"
>}}

I principali vantaggi dell’OTA includono:

* **Manutenzione remota:**: Aggiornare il firmware senza interventi in loco.
* **Sicurezza migliorata:**: Correggere rapidamente vulnerabilità note.
* **Aggiornamenti delle funzionalità:**: Fornire nuove funzionalità senza interruzioni agli utenti.
* **Costi di manutenzione ridotti:**: Evitare costosi richiami o interventi manuali.

### Implementazione OTA con ESP-IDF

ESP-IDF offre supporto integrato per OTA tramite due metodi principali:

* **API nativa**: Utilizzando il componente `app_update` per il controllo completo del processo di aggiornamento.
* **API semplificata**: Utilizzando il componente `esp_https_ota` per un’interfaccia di alto livello che gestisce automaticamente download HTTPS e caricamento del firmware scaricato.

Nella maggior parte dei casi, l’applicazione deve interagire solo con l’interfaccia pubblica dei componenti `esp_https_ota` e `app_update`. In Fig.2 è possibile vedere un diagramma semplificato dei componenti del processo OTA.

{{< figure
default=true
src="{{ "/workshops/esp-idf-advanced/assets/lecture_4_ota.webp" | absURL }}"
height=500
caption="Fig.2 -- Componenti chiave OTA (diagramma semplificato)"
>}}

Un tipico processo OTA include:

1. Scaricare la nuova immagine firmware via Wi-Fi o Ethernet.
2. Scrivere la nuova immagine in una partizione OTA non utilizzata nella flash.
3. Aggiornare la partizione dati OTA (`otadata`) per impostare il nuovo firmware come versione attiva.
4. Riavviare il dispositivo per applicare l’aggiornamento.

{{< alert icon="lightbulb" iconColor="#179299"  cardColor="#9cccce">}}
Per usare OTA, è necessario aggiungere una tabella delle partizioni appropriata.
{{< /alert >}}

#### Esempio di codice con `esp_https_ota`

L’utilizzo di `esp_https_ota` è semplice e richiede generalmente poche righe di codice.

```c
#include "esp_https_ota.h"

esp_err_t do_firmware_upgrade()
{
    esp_http_client_config_t config = {
        .url = "https://example.com/firmware.bin",
        .cert_pem = (char *)server_cert_pem_start,
    };
    esp_https_ota_config_t ota_config = {
        .http_config = &config,
    };
    esp_err_t ret = esp_https_ota(&ota_config);
    if (ret == ESP_OK) {
        esp_restart();
    } else {
        return ESP_FAIL;
    }
    return ESP_OK;
}
```

Questo codice scarica una nuova immagine firmware e, se l’operazione ha successo, riavvia il dispositivo per avviare il nuovo firmware. Per un utilizzo più avanzato, consultare la [documentazione ESP-IDF OTA](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html).

#### Layout della tabella delle partizioni OTA

L’OTA richiede un layout specifico della tabella delle partizioni. Questa deve avere almeno le seguenti partizioni:

* **Partizione NVS:** Per lo storage non volatile.
* **Partizione otadata:** Per tracciare quale partizione firmware è attiva.
* **Due partizioni app OTA:** Per immagini firmware attive/passive.

Un esempio di tabella delle partizioni valida è il seguente:

```
Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     ,        0x6000,
otadata,  data, ota,     ,        0x2000,
phy_init, data, phy,     ,        0x1000,
ota_0,    app,  ota_0,   ,        1M,
ota_1,    app,  ota_1,   ,        1M,
```

Questo layout garantisce aggiornamenti sicuri: il nuovo firmware viene scritto nella partizione inattiva e solo dopo la verifica di integrità viene contrassegnato come attivo per il successivo avvio. La partizione otadata occupa due settori flash (0x2000 byte) per prevenire corruzioni in caso di interruzione di corrente durante l’aggiornamento.

Oltre ai campi già menzionati (`data`,`nvs`), questa tabella contiene un campo `otadata` (con tipologia `data`,`ota`) che gioca un ruolo fondamentale negli aggiornamenti OTA.

#### Partizione otadata

La **partizione otadata** è una partizione speciale nella tabella delle partizioni, necessaria per progetti che utilizzano aggiornamenti firmware Over-The-Air (OTA). La sua funzione principale è memorizzare le informazioni su quale slot OTA (come `ota_0` o `ota_1`) deve essere avviato dal dispositivo. La sua dimensione tipica è `0x2000` byte (due settori flash).

L’uso della partizione `otadata` è il seguente:

* Al primo avvio (o dopo un erase), la partizione `otadata` è vuota (tutti i byte impostati a 0xFF). In questo stato, il bootloader avvia il firmware nella partizione `app_factory` se presente, oppure il primo slot OTA se non lo è.
* Dopo un aggiornamento OTA riuscito, la partizione `otadata` viene aggiornata per indicare quale slot OTA avviare al prossimo riavvio.
* La partizione è progettata per essere robusta contro interruzioni di corrente: utilizza due settori e un campo contatore per determinare l’ultimo dato valido se i settori non sono coerenti.

## Cifratura della Flash

La cifratura della flash è una funzionalità di sicurezza fondamentale, progettata per proteggere il contenuto della memoria flash. Quando abilitata, tutti i dati memorizzati nella flash vengono cifrati, rendendo estremamente difficile per soggetti non autorizzati estrarre informazioni sensibili, anche nel caso di accesso fisico al dispositivo.

### Funzionamento della cifratura della Flash

Al primo avvio, il firmware viene caricato in chiaro e poi cifrato in loco. Il processo di cifratura utilizza algoritmi come XTS-AES-128, XTS-AES-256 o AES-256, a seconda della serie del SoC Espressif. La chiave crittografica è memorizzata in modo sicuro nei blocchi eFuse del chip e __non è accessibile via software__, garantendo una protezione robusta delle chiavi. 

L’accesso alla flash è trasparente: qualsiasi regione mappata in memoria viene automaticamente decrittata in lettura e cifrata in scrittura, senza necessità di modificare il codice applicativo.

L'impostazione predefinita prevede che le partizioni critiche come bootloader, tabella partizioni, partizione chiavi NVS, otadata e tutte le partizioni applicative siano cifrate. Altre partizioni possono essere selettivamente cifrandole segnalandole con il flag `encrypted` nella tabella partizioni.

### Modalità development e release

La cifratura della flash può essere abilitata in modalità "Development" o "Release".

* In **modalità development**, è possibile ricaricare firmware in chiaro per test, ma non è sicuro per la produzione.
* In **modalità release**, non è possibile ricaricare il firmware in chiaro.

È fortemente consigliato usare la modalità release per dispositivi in produzione per prevenire l’estrazione o la modifica non autorizzata del firmware.

### Note importanti

* Non interrompere l’alimentazione durante il passaggio di cifratura iniziale al primo avvio, poiché potrebbe corrompere la flash e richiedere di caricare nuovamente il firmware.
* Abilitare la cifratura flash aumenta la dimensione del bootloader, il che può richiedere un aggiornamento dell’offset della tabella delle partizioni. Lo vedremo in dettaglio nell’[esercizio 4.3](../assignment-4-3)

## Bootloader sicuro

I dispositivi Espressif offrono una funzionalità chiamata **secure boot**. Questo meccanismo costituisce la base della sicurezza del dispositivo, proteggendolo dall’esecuzione di codice non autorizzato e dalla manomissione del firmware.

Un **bootloader sicuro** è un programma speciale che verifica l’autenticità e l’integrità del firmware prima di consentirne l’esecuzione sul dispositivo. Questo avviene controllando le firme crittografiche associate al bootloader e alle immagini applicative. Se una parte del codice è stata modificata o non è firmata da una chiave affidabile, il dispositivo rifiuta di eseguirla.

Questo processo stabilisce una **catena di certificazione** (chain of trust):

* Il bootloader hardware (in ROM) verifica il bootloader software.
* Il bootloader software verifica poi il firmware applicativo.

Questo garantisce che solo il codice firmato dal produttore del dispositivo (o da un’altra entità fidata) possa essere eseguito, proteggendo da malware, aggiornamenti non autorizzati e manomissioni fisiche della memoria flash del dispositivo. La chiave privata della firma è mantenuta segreta, mentre la chiave pubblica è memorizzata in modo sicuro nella memoria eFUSE del dispositivo, rendendolo inaccessibile a software e attaccanti esterni. 

### Come Usare il bootloader sicuro

Abilitare il bootloader sicuro sui dispositivi Espressif comporta i seguenti passaggi:

1. **Abilitare il secure boot nella configurazione:**

   * Usare `menuconfig` per abilitare il secure boot sotto "Security Features".

2. **Generare o specificare una chiave per la firma:**

   * Se non esiste una chiave per firmare il firmware, generarne una usando il comando fornito (es. `idf.py secure-generate-signing-key`). In produzione, generare le chiavi con strumenti affidabili come OpenSSL.

3. **Compilare e caricare il bootloader:**

   * Compilare il bootloader con secure boot abilitato:

     ```sh
     idf.py bootloader
     ```
   * Caricare manualmente il bootloader usando il comando mostrato dal processo di build.

4. **Compilare e caricare l’applicazione:**

   * Compilare e caricare l’applicazione e la tabella delle partizioni:

     ```sh
     idf.py flash
     ```
   * L’immagine dell’applicazione sarà firmata automaticamente usando la chiave specificata.

5. **Verificare l’attivazione del secure boot:**

   * Al primo avvio, il dispositivo abiliterà il secure boot, brucerà gli eFUSE necessari e verificherà le firme. Puoi monitorare l’output seriale per confermare l’attivazione riuscita.

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
Una volta abilitato il secure boot, il bootloader non può essere ricaricato (a meno di usare una modalità speciale "reflashable", non consigliata per la produzione). Conservare sempre al sicuro la chiave privata, poiché la sua compromissione invalida l’intero processo di secure boot
{{< /alert >}}

<!-- Testeremo il bootloader sicuro nell’[Esercizio 4.4](assignment-4-3) -->

## Conclusione

In questo articolo, abbiamo esplorato tre pilastri fondamentali della sicurezza moderna per l’IoT: aggiornamenti OTA, cifratura della flash e bootloader sicuri. Insieme, queste funzionalità assicurano che i dispositivi possano essere aggiornati in modo sicuro, proteggere i dati sensibili a riposo e verificare l’integrità del firmware a partire dal momento dell’accensione. 

Nei prossimi esercizi, testerete queste funzionalità in prima persona.

> Prossimo passo: [esercizio 4.1](../assignment-4-1/)

> Oppure [torna al menù di navigazione](../#agenda)