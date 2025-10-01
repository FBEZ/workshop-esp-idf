---
title: "ESP-IDF workshop - Preliminary setup"
date: "2025-11-12"
summary: "This guide outlines the preliminary steps to set up your work environment and follow the workshops."
---

## Introduction

In this guide, we’ll go through how to set up the development environment to work on projects based on the ESP-IDF toolchain.

We’ll use the open-source IDE [VS Code](https://code.visualstudio.com/) and the *ESP-IDF extension for VS Code*, which allows you to configure the toolchain, build projects, and program the flash memory of Espressif modules.

If you don’t have an Espressif EVK available, you can still complete all the steps in this guide except the last one.

For the final step, you’ll need an EVK based on any Espressif SoC. During the workshop, you’ll receive a board based on the `ESP32-C3`, the [`ESP32-C3-DevKit-RUST-1`](https://github.com/esp-rs/esp-rust-board?tab=readme-ov-file#rust-esp-board).

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
The term **ESP-IDF** is used both to refer to the [toolchain itself](https://github.com/espressif/esp-idf?tab=readme-ov-file#espressif-iot-development-framework) and to the [VS Code extension](https://github.com/espressif/vscode-esp-idf-extension?tab=readme-ov-file#esp-idf-extension-for-vs-code).
In this guide, we’ll explicitly use *ESP-IDF toolchain* for the first and *ESP-IDF extension* for the second.
{{< /alert >}}

The guide is divided into 5 parts:

1. Installing VS Code and prerequisites
2. Installing the ESP-IDF extension for VS Code
3. Configuring the ESP-IDF toolchain
4. Building the first project
5. Flashing the module

## Installing VS Code and Prerequisites

This step depends on your operating system. Follow the appropriate guide below:

* 🐧 Linux: [Installing VS Code and prerequisites](./installation_linux/)
* 🪟 Windows: [Installing VS Code](./installation_windows/)
* 🍎 macOS: [Installing VS Code and prerequisites](./installation_macos/)


## Installing the ESP-IDF Extension for VS Code

Once all prerequisites are installed, we can add the ESP-IDF extension to VS Code.
Through the **ESP-IDF extension**, we’ll then install and configure the **ESP-IDF toolchain**.

* Open VS Code
* Click the Extensions icon (four squares) on the left
  ![](./assets/setup/3_extension.webp)
* In the search bar, type `esp-idf`
  ![Search extension](./assets/setup/4_search_idf_extension.webp)
* Click “Install” on the first result, **ESP-IDF**

  * If prompted, click “Accept and Install”

## Configuring the ESP-IDF Toolchain

Once the ESP-IDF extension is installed, run the configuration process to automatically install the entire ESP-IDF toolchain.

* Click on `Configuring the ESP-IDF Extension`
  ![](./assets/setup/5_configurazione.webp)

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
If the configuration page didn’t open automatically, you can:

* Open the command palette (`F1` or `CTRL+SHIFT+P`)

* Type:<br>
  `> ESP-IDF: Configure ESP-IDF Extension`
  {{< /alert >}}

* A new tab opens → Click on `EXPRESS`
  ![](./assets/setup/6_configurazione.webp)

* Open the dropdown menu `Select ESP-IDF version`
  ![](./assets/setup/7_express.webp)

* Select `5.5.1 (release version)`
  ![](./assets/setup/8_choose_idf.webp)

* Click `Install`
  ![](./assets/setup/9_install.webp)

* Wait for the installation to complete
  ![](./assets/setup/10_installation.webp)
  {{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
  The installation can take quite some time.
  {{< /alert >}}

* When it’s done, you’ll see the confirmation screen
  ![](./assets/setup/11_allright.webp)


## Building the First Project

Now that the extension and toolchain are installed, it’s time to test building a project.
We’ll create a new project based on one of the examples included with the ESP-IDF toolchain.

### Create a Project from an Example

* Open the command palette (`F1` or `CTRL+SHIFT+P`)
* Type `ESP-IDF: Show Example Project` and select it
  ![](./assets/setup/12_showExample.webp)
* In the dropdown menu, select `ESP-IDF v5.5.1`
  ![](./assets/setup/13_choose_esp_IDF.webp)
* A tab with a list of example projects appears → select `hello_world`
  ![](./assets/setup/14_hello_world.webp)
* The project description appears in the central tab
* Click `Select location for creating hello_world project`
  ![](./assets/setup/15_selection_location.webp)
* Choose a folder to create the project and click `Select this folder`
* A new VS Code window opens
* You should now see the files for the `hello_world` example project in the right panel
  ![](./assets/setup/16_new_project.webp)

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
If you don’t see the files, make sure the first icon on the left (two overlapping sheets) is selected.
{{< /alert >}}


### Specify the Target

To build and flash the project to your Espressif module, you must tell the compiler which SoC you’re targeting.
In the workshop, we’ll use a board based on the ESP32-C3, so we’ll select that target.

{{< alert icon="lightbulb" iconColor="#179299" cardColor="#9cccce">}}
If you have a different EVK available, select the corresponding target.
{{< /alert >}}

* Open the command palette (`F1` or `CTRL+SHIFT+P`) and type
  `ESP-IDF: Set Espressif Device Target`
  ![](./assets/setup/17_select_target.webp)
* From the dropdown → select `esp32c3`
  ![](./assets/setup/18_esp32c3.webp)
* In the following dropdown → select `ESP32-C3 chip (via builtin USB-JTAG)`
  ![](./assets/setup/19_builtin.webp)


### Build the Project

Now let’s build the project.

* Open the command palette (`F1` or `CTRL+SHIFT+P`)
* Type `ESP-IDF: Build Your Project`
  ![](./assets/setup/20_buildYourProject.webp)
* A terminal will open at the bottom showing build messages
* When the build finishes, you’ll see the memory usage summary
  ![](./assets/setup/21_memory_usage.webp)

If you see the summary screen, both the toolchain and extension were installed correctly.

If you have an Espressif EVK, proceed to the next section to verify USB connectivity.


## Flashing the Module

Once the project is built, it’s time to flash the module.
The ESP-IDF extension for VS Code provides the command:
`> ESP-IDF: Flash (UART) Your Project`

However, the most commonly used command is:

```console
> ESP-IDF: Build, Flash and Start a Monitor on Your Device
```

This command not only builds and flashes the project to the device but also starts a serial monitor directly in the editor terminal.

To flash the module:

1. Select the port your EVK is connected to
2. Run the command:
   `> ESP-IDF: Build, Flash and Start a Monitor on Your Device`

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
On Linux, you may need to add your user to the `dialout` group to access serial ports without admin privileges:

```
sudo usermod -a -G dialout $USER
```

Remember to log out and back in for the changes to take effect.
{{< /alert >}}


### Select the Port the EVK is Connected To

* Connect the board to your computer via USB
* If VS Code is closed, reopen it and open your project folder

  * `File → Open Folder` or `File → Open Recent`
* Open the command palette and type:
  `> ESP-IDF: Select Port to Use (COM, tty, usbserial)`
  ![](./assets/setup/22_select_port_to_use.webp)
* Select the port (Silicon Labs – the USB/UART bridge on the EVK)
  ![](./assets/setup/23_port_selection.webp)
* The port name will now appear in the bottom status bar
  ![](./assets/setup/23_5_icon_below.webp)

{{< alert iconColor="#df8e1d" cardColor="#edcea3">}}
If your operating system doesn’t automatically detect the connected board, refer to the appropriate guide:

* 🪟 [Windows](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-windows)
* 🐧 [Linux](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-linux-and-macos)
* 🍎 [macOS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-linux-and-macos)
  {{< /alert >}}


### Flash the Module and Start the Monitor

* Open the command palette and type:
  `> ESP-IDF: Build, Flash and Start a Monitor on Your Device`
  ![](/workshops/esp-idf-setup/assets/setup/24_flash.webp)
* From the dropdown → select `UART`
  ![](./assets/setup/25_uart.webp)
* Wait for the flashing process to complete and for the monitor to start
* In the terminal, you’ll see the boot messages and the “hello world!” output
  ![](./assets/setup/26_terminal.webp)

If you see the message in the terminal, your setup is working correctly and you’re ready for the workshop and for developing projects based on ESP-IDF.


## Conclusion

In this guide, we covered how to install VS Code, the ESP-IDF extension, and the ESP-IDF toolchain.
We also went through how to create, build, and flash a project to your EVK.
Your development environment is now ready to use.

