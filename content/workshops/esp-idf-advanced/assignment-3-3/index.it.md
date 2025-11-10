---
title: "ESP-IDF Avanzato - Esercizio 3.3"
date: "2025-11-12"
series: ["WS00B"]
series_order: 12
showAuthor: false
summary: "Analizzare il core dump"
---

Se hai ancora tempo, prova a trovare l’altro bug nel codice utilizzando nuovamente le informazioni fornite dal core dump.

## Traccia della soluzione

Crea il file del core dump come hai fatto nel precedente esercizio.

* Aspetta che si verifichi il crash
* Ferma il monitor (`CTRL + ]`)
* Esegui `idf.py coredump-info > https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/coredump.txt`
* Apri il file `https://github.com/espressif/developer-portal-codebase/tree/main/content/workshops/esp-idf-advanced/coredump.txt`

<details>
<summary>Espandi il secondo core dump</summary>

```bash
Executing action: coredump-info
Serial port /dev/cu.usbmodem1131101
Connecting...
Detecting chip type... ESP32-C3
===============================================================
==================== ESP32 CORE DUMP START ====================

Crashed task handle: 0x3fc9ff18, name: 'sys_evt', GDB name: 'process 1070202648'
Crashed task is not in the interrupt context

================== CURRENT THREAD REGISTERS ===================
ra             0x4200dc68	0x4200dc68 <temperature_sensor_read_celsius+10>
sp             0x3fc9fe40	0x3fc9fe40
gp             0x3fc94600	0x3fc94600 <country_info_24ghz+200>
tp             0x3fc9ff10	0x3fc9ff10
t0             0x4005890e	1074104590
t1             0x0	0
t2             0xffffffff	-1
fp             0x0	0x0
s1             0x3fc9f13c	1070199100
a0             0x3fcacc14	1070255124
a1             0x3fc9fe5c	1070202460
a2             0x0	0
a3             0x0	0
a4             0x3fcacb34	1070254900
a5             0x0	0
a6             0x4200d4c2	1107350722
a7             0x9800000	159383552
s2             0x0	0
s3             0x0	0
s4             0xffffffff	-1
s5             0x0	0
s6             0xffffffff	-1
s7             0x3fcacb44	1070254916
s8             0x0	0
s9             0x0	0
s10            0x0	0
s11            0x0	0
t3             0x0	0
t4             0x604f	24655
t5             0x0	0
t6             0x0	0
pc             0x0	0x0

==================== CURRENT THREAD STACK =====================
#0  0x00000000 in ?? ()
#1  0x4200dc68 in temperature_sensor_read_celsius (sensor=<optimized out>, temperature=temperature@entry=0x3fc9fe5c) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/components/temperature_sensor/temperature_sensor.c:150
#2  0x4200d4d4 in temp_event_handler (handler_arg=<optimized out>, base=<optimized out>, id=<optimized out>, event_data=<optimized out>) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/main/app_main.c:50
#3  0x420b1942 in handler_execute (loop=loop@entry=0x3fc9f13c, handler=<optimized out>, post=<error reading variable: Cannot access memory at address 0x0>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:136
#4  0x420b228e in esp_event_loop_run (event_loop=event_loop@entry=0x3fc9f13c, ticks_to_run=ticks_to_run@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:696
#5  0x420b2386 in esp_event_loop_run_task (args=0x3fc9f13c, args@entry=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:106
#6  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

======================== THREADS INFO =========================
  Id   Target Id          Frame
* 1    process 1070202648 0x00000000 in ?? ()
  2    process 1070198548 0x403851d4 in esp_cpu_wait_for_intr () at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_hw_support/cpu.c:64
  3    process 1070254080 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  4    process 1070196668 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  5    process 1070209148 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  6    process 1070222780 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  7    process 1070191796 0x40387998 in vPortClearInterruptMaskFromISR (prev_int_level=1) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:515


       TCB             NAME PRIO C/B  STACK USED/FREE
---------- ---------------- -------- ----------------
0x3fc9ff18          sys_evt    20/20         352/2460
0x3fc9ef14             IDLE      0/0         208/1312
0x3fcac800        mqtt_task      5/5         624/5516
0x3fc9e7bc             main      1/1         336/3752
0x3fca187c              tiT    18/18         336/3240
0x3fca4dbc             wifi    23/23         336/6312
0x3fc9d4b4        esp_timer    22/22         224/3856

==================== THREAD 1 (TCB: 0x3fc9ff18, name: 'sys_evt') =====================
#0  0x00000000 in ?? ()
#1  0x4200dc68 in temperature_sensor_read_celsius (sensor=<optimized out>, temperature=temperature@entry=0x3fc9fe5c) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/components/temperature_sensor/temperature_sensor.c:150
#2  0x4200d4d4 in temp_event_handler (handler_arg=<optimized out>, base=<optimized out>, id=<optimized out>, event_data=<optimized out>) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/main/app_main.c:50
#3  0x420b1942 in handler_execute (loop=loop@entry=0x3fc9f13c, handler=<optimized out>, post=<error reading variable: Cannot access memory at address 0x0>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:136
#4  0x420b228e in esp_event_loop_run (event_loop=event_loop@entry=0x3fc9f13c, ticks_to_run=ticks_to_run@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:696
#5  0x420b2386 in esp_event_loop_run_task (args=0x3fc9f13c, args@entry=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:106
#6  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255
```

</details>

Buona caccia al bug!

<details>
<summary>Mostra soluzione</summary>

L’errore è causato dalla riga 128 in `app_main.c`

```c
free(sensor);
```

Elimina l’oggetto sensor e la lettura della temperatura sta usando un puntatore non valido.

</details>

> Passo successivo: [Lezione 4](../lecture-4/)

> Oppure [torna al menù di navigazione](../#agenda)