---
title: "Prerequisiti Windows &#x1FA9F;"
date: "2025-11-12"
summary: "Questa guida presenta i passi preliminari per impostare il setup di lavoro e seguire i workshop. "
---
## Installazione VS Code

* Vai su [sito di download di VS Code](code.visualstudio.com/downloads)
* Scarica ed installa la versione per Windows
![](/workshop-esp-idf/workshops/esp-idf-setup/assets/setup//1_windows_vscode_download.webp)

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
In questa guida viene usato Windows 11 
{{< /alert >}}


* Una volta scaricato il file `.exe`, fai doppio click e segui la procedura di installazione


Finita l'installazione, per aprire VS Code ci sono due strade. 

1. Apri VS Code da menù
2. Apri VS Code da una cartella

Siccome è spesso utile aprire l'editor direttamente nella cartella, seguiremo questa seconda strada. 

#### Apri VS Code da una cartella

* Crea una nuova cartella `tmp`
* Clicca tasto destro del mouse all'interno della cartella in Explorer
* Sul menù seleziona `Show more options`
* Clicca su `Open with Code`
![](/workshop-esp-idf/workshops/esp-idf-setup/assets/setup//1_5_windows_open_with_code.webp)
* Dovresti ora vedere l'interfaccia di VS Code
![](/workshop-esp-idf/workshops/esp-idf-setup/assets/setup//2_vscode_screen.webp)

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
VS Code potrebbe chiederti se ti fidi dell'autore della cartella. Questo aspetto è importante quando vengono usate repo `git`, per il momento non fa differenza. Clicca "Sì". 
{{< /alert >}}

## Installazione prerequisiti

Non ci sono da installare altri prerequisiti. Questi sono infatti gestiti automaticamente durante la configurazione dell'estensione ESP-IDF.

## Prossimi step

> Prosegui con il [prossimo passo](../#installazione-dellestensione-per-vs-code).
