---
title: "Windows prerequisites 🪟"
date: "2025-11-12"
summary: "This guide outlines the preliminary steps to set up your work environment and follow the workshops."
---

## VS Code Installation

* Go to the [VS Code download site](code.visualstudio.com/downloads)
* Download and install the Windows version
  ![](/workshops/esp-idf-setup/assets/setup//1_windows_vscode_download.webp)

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
This guide uses Windows 11.
{{< /alert >}}

* Once the `.exe` file is downloaded, double-click it and follow the installation steps.

After installation, there are two ways to open VS Code:

1. Open VS Code from the Start menu
2. Open VS Code from a folder

Since it’s often useful to open the editor directly from a folder, we’ll follow the second method.

#### Open VS Code from a Folder

* Create a new folder called `tmp`
* Right-click inside the folder in File Explorer
* From the menu, select `Show more options`
* Click on `Open with Code`
  ![](/workshops/esp-idf-setup/assets/setup//1_5_windows_open_with_code.webp)
* You should now see the VS Code interface
  ![](/workshops/esp-idf-setup/assets/setup//2_vscode_screen.webp)

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
VS Code may ask whether you trust the author of the folder. This is important when using `git` repositories, but for now it doesn’t matter. Click “Yes.”
{{< /alert >}}

## Installing Prerequisites

No additional prerequisites need to be installed. These will be automatically handled during the setup of the ESP-IDF extension.

## Next Steps

> Continue with the [next step](../#installing-the-esp-idf-extension-for-vs-code).
