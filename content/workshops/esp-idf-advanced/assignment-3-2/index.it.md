---
title: "ESP-IDF Avanzato - Esercizio 3.2"
date: "2025-08-05"
series: ["WS00B"]
series_order: 11
showAuthor: false
summary: "Analizzare il core dump (guidato)"
---

## Core dump

Per questo esercizio, devi partire dal progetto [assignment_3_2_base](/workshop/esp-idf-advanced/assets/assignment_3_2_base).

## Obiettivi dell'esercizio

1. Abilitare il core dump in `menuconfig`
2. Compilare ed eseguire l'applicazione
3. Analizzare il core dump
4. Correggere i bug nel progetto
5. Ricompilare ed eseguire nuovamente l'applicazione

### Abilitare il core dump

* Apri `menuconfig`: `> ESP-IDF: SDK Configuration Editor (menuconfig)`
* Imposta `Core Dump` → `Data destination` → `Flash`
* `> ESP-IDF: Build, Flash and Start a Monitor on Your Device`

### Compilare ed eseguire l'applicazione

Ora attendi che si verifichi il crash.

* Quando si verifica, interrompi l'esecuzione (`CTRL + ]`)
* Crea un nuovo terminale `> ESP-IDF: Open ESP-IDF Terminal`
* esegui `idf.py coredump-info > coredump.txt`
* Apri il file `coredump.txt`

### Analizzare il core dump

Ora osserva attentamente il file core dump.

<details>
<summary>Clicca qui se non sei riuscito a generare coredump.txt</summary>

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
ra             0x4200d822	0x4200d822 <is_alarm_set+20>
sp             0x3fc9fe50	0x3fc9fe50
gp             0x3fc94600	0x3fc94600 <country_info_24ghz+200>
tp             0x3fc9ff10	0x3fc9ff10
t0             0x4005890e	1074104590
t1             0x90000000	-1879048192
t2             0xffffffff	-1
fp             0x0	0x0
s1             0x8b7f7a	9142138
a0             0x8b7f7a	9142138
a1             0x0	0
a2             0x8b7f7a0	146274208
a3             0x0	0
a4             0x4ddf	19935
a5             0x4c4b3f	4999999
a6             0x60023000	1610756096
a7             0xa	10
s2             0x0	0
s3             0x0	0
s4             0xffffffff	-1
s5             0x0	0
s6             0xffffffff	-1
s7             0x0	0
s8             0x0	0
s9             0x0	0
s10            0x0	0
s11            0x0	0
t3             0x0	0
t4             0xfe42	65090
t5             0x0	0
t6             0x0	0
pc             0x4200d840	0x4200d840 <is_alarm_set+50>

==================== CURRENT THREAD STACK =====================
#0  is_alarm_set (alarm=0x0) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/components/alarm/alarm.c:40
#1  0x4200d48c in alarm_event_handler (handler_arg=<optimized out>, base=<optimized out>, id=<optimized out>, event_data=<optimized out>) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/main/app_main.c:66
#2  0x420b1944 in handler_execute (loop=loop@entry=0x3fc9f13c, handler=<optimized out>, post=<error reading variable: Cannot access memory at address 0x4c4b3f>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:136
#3  0x420b2290 in esp_event_loop_run (event_loop=event_loop@entry=0x3fc9f13c, ticks_to_run=ticks_to_run@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:696
#4  0x420b2388 in esp_event_loop_run_task (args=0x3fc9f13c, args@entry=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:106
#5  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

======================== THREADS INFO =========================
  Id   Target Id          Frame
* 1    process 1070202648 is_alarm_set (alarm=0x0) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/components/alarm/alarm.c:40
  2    process 1070198548 0x403851d4 in esp_cpu_wait_for_intr () at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_hw_support/cpu.c:64
  3    process 1070209148 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  4    process 1070196668 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  5    process 1070253776 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  6    process 1070222780 0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
  7    process 1070191796 0x40387998 in vPortClearInterruptMaskFromISR (prev_int_level=1) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:515


       TCB             NAME PRIO C/B  STACK USED/FREE
---------- ---------------- -------- ----------------
0x3fc9ff18          sys_evt    20/20         352/2460
0x3fc9ef14             IDLE      0/0         208/1312
0x3fca187c              tiT    18/18         336/3240
0x3fc9e7bc             main      1/1         336/3752
0x3fcac6d0        mqtt_task      5/5         768/5372
0x3fca4dbc             wifi    23/23         336/6312
0x3fc9d4b4        esp_timer    22/22         224/3856

==================== THREAD 1 (TCB: 0x3fc9ff18, name: 'sys_evt') =====================
#0  is_alarm_set (alarm=0x0) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/components/alarm/alarm.c:40
#1  0x4200d48c in alarm_event_handler (handler_arg=<optimized out>, base=<optimized out>, id=<optimized out>, event_data=<optimized out>) at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/main/app_main.c:66
#2  0x420b1944 in handler_execute (loop=loop@entry=0x3fc9f13c, handler=<optimized out>, post=<error reading variable: Cannot access memory at address 0x4c4b3f>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:136
#3  0x420b2290 in esp_event_loop_run (event_loop=event_loop@entry=0x3fc9f13c, ticks_to_run=ticks_to_run@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:696
#4  0x420b2388 in esp_event_loop_run_task (args=0x3fc9f13c, args@entry=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_event/esp_event.c:106
#5  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 2 (TCB: 0x3fc9ef14, name: 'IDLE') =====================
#0  0x403851d4 in esp_cpu_wait_for_intr () at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_hw_support/cpu.c:64
#1  0x42015ce8 in esp_vApplicationIdleHook () at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/freertos_hooks.c:58
#2  0x4038859c in prvIdleTask (pvParameters=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/tasks.c:4341
#3  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 3 (TCB: 0x3fca187c, name: 'tiT') =====================
#0  0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
#1  0x40387a5c in vPortYield () at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:638
#2  0x40387450 in xQueueReceive (xQueue=0x3fca099c, pvBuffer=pvBuffer@entry=0x3fca182c, xTicksToWait=<optimized out>, xTicksToWait@entry=6) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/queue.c:1659
#3  0x42086ae8 in sys_arch_mbox_fetch (mbox=mbox@entry=0x3fc9b7c0 <tcpip_mbox>, msg=msg@entry=0x3fca182c, timeout=60) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/port/freertos/sys_arch.c:313
#4  0x420710ea in tcpip_timeouts_mbox_fetch (mbox=mbox@entry=0x3fc9b7c0 <tcpip_mbox>, msg=msg@entry=0x3fca182c) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/lwip/src/api/tcpip.c:104
#5  0x420711dc in tcpip_thread (arg=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/lwip/src/api/tcpip.c:142
#6  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 4 (TCB: 0x3fc9e7bc, name: 'main') =====================
#0  0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
#1  0x40387a5c in vPortYield () at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:638
#2  0x40388d04 in vTaskDelay (xTicksToDelay=xTicksToDelay@entry=100) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/tasks.c:1588
#3  0x4200d7e8 in app_main () at /Users/francesco/Documents/articles/devrel-advanced-workshop-code/assignment_3_2/main/app_main.c:136
#4  0x420b420e in main_task (args=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/app_startup.c:208
#5  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 5 (TCB: 0x3fcac6d0, name: 'mqtt_task') =====================
#0  0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
#1  0x40387a5c in vPortYield () at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:638
#2  0x403875bc in xQueueSemaphoreTake (xQueue=0x3fcac8e0, xTicksToWait=<optimized out>, xTicksToWait@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/queue.c:1901
#3  0x42086910 in sys_arch_sem_wait (sem=sem@entry=0x3fcac8d0, timeout=timeout@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/port/freertos/sys_arch.c:165
#4  0x420713d4 in tcpip_send_msg_wait_sem (fn=<optimized out>, apimsg=apimsg@entry=0x3fcae33c, sem=0x3fcac8d0) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/lwip/src/api/tcpip.c:461
#5  0x42088840 in netconn_gethostbyname_addrtype (name=name@entry=0x3fcac8b8 <error: Cannot access memory at address 0x3fcac8b8>, addr=addr@entry=0x3fcae3a8, dns_addrtype=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/lwip/src/api/api_lib.c:1333
#6  0x4206de2a in lwip_getaddrinfo (nodename=nodename@entry=0x3fcac8b8 <error: Cannot access memory at address 0x3fcac8b8>, servname=servname@entry=0x0, hints=hints@entry=0x3fcae3fc, res=res@entry=0x3fcae41c) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/lwip/src/api/netdb.c:495
#7  0x42021468 in getaddrinfo (nodename=0x3fcac8b8 <error: Cannot access memory at address 0x3fcac8b8>, servname=0x0, hints=0x3fcae3fc, res=0x3fcae41c) at /Users/francesco/esp/v5.4.2/esp-idf/components/lwip/include/lwip/netdb.h:23
#8  esp_tls_hostname_to_fd (host=<optimized out>, hostlen=<optimized out>, port=1883, addr_family=<optimized out>, address=address@entry=0x3fcae464, fd=fd@entry=0x3fcae460) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp-tls/esp_tls.c:210
#9  0x420218c4 in tcp_connect (host=host@entry=0x3fca24cc <error: Cannot access memory at address 0x3fca24cc>, hostlen=<optimized out>, port=port@entry=1883, cfg=cfg@entry=0x3fcac83c, error_handle=error_handle@entry=0x3fcac824, sockfd=sockfd@entry=0x3fcac8a0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp-tls/esp_tls.c:359
#10 0x42021ebc in esp_tls_plain_tcp_connect (host=host@entry=0x3fca24cc <error: Cannot access memory at address 0x3fca24cc>, hostlen=<optimized out>, port=port@entry=1883, cfg=cfg@entry=0x3fcac83c, error_handle=error_handle@entry=0x3fcac824, sockfd=sockfd@entry=0x3fcac8a0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp-tls/esp_tls.c:533
#11 0x42023e06 in tcp_connect (t=<optimized out>, host=0x3fca24cc <error: Cannot access memory at address 0x3fca24cc>, port=1883, timeout_ms=10000) at /Users/francesco/esp/v5.4.2/esp-idf/components/tcp_transport/transport_ssl.c:148
#12 0x42023210 in esp_transport_connect (t=<optimized out>, host=<optimized out>, port=<optimized out>, timeout_ms=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/tcp_transport/transport.c:123
#13 0x4200f628 in esp_mqtt_task (pv=0x3fca1a28, pv@entry=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/mqtt/esp-mqtt/mqtt_client.c:1620
#14 0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 6 (TCB: 0x3fca4dbc, name: 'wifi') =====================
#0  0x4038345e in esp_crosscore_int_send_yield (core_id=core_id@entry=0) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_system/crosscore_int.c:121
#1  0x40387a5c in vPortYield () at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:638
#2  0x40387450 in xQueueReceive (xQueue=0x3fca2c9c, pvBuffer=0x3fca4d48, xTicksToWait=<optimized out>, xTicksToWait@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/queue.c:1659
#3  0x420b3d64 in queue_recv_wrapper (queue=<optimized out>, item=<optimized out>, block_time_tick=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_wifi/esp32c3/esp_adapter.c:238
#4  0x400407be in ppTask ()
#5  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255

==================== THREAD 7 (TCB: 0x3fc9d4b4, name: 'esp_timer') =====================
#0  0x40387998 in vPortClearInterruptMaskFromISR (prev_int_level=1) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:515
#1  0x40387a28 in vPortExitCritical () at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:624
#2  0x40389774 in ulTaskGenericNotifyTake (uxIndexToWait=uxIndexToWait@entry=0, xClearCountOnExit=xClearCountOnExit@entry=1, xTicksToWait=xTicksToWait@entry=4294967295) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/tasks.c:5759
#3  0x42017e9a in timer_task (arg=<error reading variable: value has been optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/esp_timer/src/esp_timer.c:459
#4  0x403877cc in vPortTaskWrapper (pxCode=<optimized out>, pvParameters=<optimized out>) at /Users/francesco/esp/v5.4.2/esp-idf/components/freertos/FreeRTOS-Kernel/portable/riscv/port.c:255


======================= ALL MEMORY REGIONS ========================
Name   Address   Size   Attrs
.rtc.text 0x50000000 0x0 RW
.rtc.force_fast 0x50000000 0x1c RW A
.rtc_noinit 0x5000001c 0x0 RW
.rtc.force_slow 0x5000001c 0x0 RW
.iram0.text 0x40380000 0x13d0a R XA
.dram0.data 0x3fc93e00 0x2ed8 RW A
.flash.text 0x42000020 0xb4fd8 R XA
.flash.appdesc 0x3c0c0020 0x100 R  A
.flash.rodata 0x3c0c0120 0x1ff3c RW A
.eh_frame_hdr 0x3c0e005c 0x0 RW
.eh_frame 0x3c0e005c 0x0 RW
.flash.tdata 0x3c0e005c 0x0 RW
.iram0.data 0x40393e00 0x0 RW
.iram0.bss 0x40393e00 0x0 RW
.dram0.heap_start 0x3fc9b8e0 0x0 RW
.coredump.tasks.data 0x3fc9ff18 0x150 RW
.coredump.tasks.data 0x3fc9fdb0 0x160 RW
.coredump.tasks.data 0x3fc9ef14 0x150 RW
.coredump.tasks.data 0x3fc9ee30 0xd0 RW
.coredump.tasks.data 0x3fca187c 0x150 RW
.coredump.tasks.data 0x3fca1720 0x150 RW
.coredump.tasks.data 0x3fc9e7bc 0x150 RW
.coredump.tasks.data 0x3fc9e660 0x150 RW
.coredump.tasks.data 0x3fcac6d0 0x150 RW
.coredump.tasks.data 0x3fcae240 0x300 RW
.coredump.tasks.data 0x3fca4dbc 0x150 RW
.coredump.tasks.data 0x3fca4c60 0x150 RW
.coredump.tasks.data 0x3fc9d4b4 0x150 RW
.coredump.tasks.data 0x3fc9d3c0 0xe0 RW

===================== ESP32 CORE DUMP END =====================
===============================================================
Done!

```

</details>

#### Identificare il task che ha causato il crash

Il core dump inizia con:

```
Crashed task handle: 0x3fc9ff18, name: 'sys_evt'
Crashed task is not in the interrupt context
```

Da questo possiamo concludere:

1. Il crash è avvenuto nel task FreeRTOS chiamato **`sys_evt`**.
2. Il crash non è avvenuto durante un interrupt, quindi è un crash in un task normale.

#### Osservare il program counter (PC) e lo stack trace

Il dump dei registri mostra:

```
pc             0x4200d840	0x4200d840 <is_alarm_set+50>
ra             0x4200d822	0x4200d822 <is_alarm_set+20>
sp             0x3fc9fe50
```

Questo significa che:

1. Il program counter (PC) si trova all'indirizzo `0x4200d840`, all'interno della funzione `is_alarm_set`, precisamente all'offset +50 byte.
2. L'indirizzo di ritorno (`ra`) è anch’esso dentro `is_alarm_set`, quindi il crash è avvenuto **all’interno di quella funzione**.

#### Esaminare lo stack trace

Stack trace (in ordine inverso di chiamata):

```
#0  is_alarm_set (alarm=0x0) at alarm.c:40
#1  alarm_event_handler at app_main.c:66
#2  handler_execute (esp_event.c:136)
#3  esp_event_loop_run (esp_event.c:696)
#4  esp_event_loop_run_task (esp_event.c:106)
#5  vPortTaskWrapper (port.c:255)
```

1. Il crash è originato dalla chiamata a `is_alarm_set` da parte di `alarm_event_handler`.
2. Questo handler è chiamato dall'event loop (`esp_event_loop_run`).

#### Concentrarsi sugli argomenti della funzione

Osserva gli argomenti di `is_alarm_set`:

```
#0  is_alarm_set (alarm=0x0) at alarm.c:40
```

* L'argomento `alarm` è `0x0` (puntatore NULL) (!)

#### Diagnosticare il motivo del crash

Il crash è avvenuto dentro `is_alarm_set` con un puntatore NULL come argomento. Di solito, questo significa:

* `is_alarm_set` dereferenzia `alarm` senza verificare se fosse NULL.
* Poiché `alarm` è NULL, accedere ai suoi campi ha causato un accesso a memoria non valido, provocando il crash.

#### Controllare il sorgente

La riga del crash è `alarm.c:40`. Se guardiamo quella linea:

```c
return alarm->last_state;
```

* Dereferenziare `alarm` senza controllo NULL provoca un fault se `alarm == NULL`.

Qualche riga sopra troviamo:

```c
alarm = NULL;
```

che è probabilmente il nostro bug.

### Ricompilare ed eseguire l'applicazione

Rimuovi la riga e il blocco `else` inutile, ottenendo la funzione `is_alarm_set` come segue:

```c
bool is_alarm_set(alarm_t *alarm)
{
    int64_t now_us = esp_timer_get_time();
    int64_t elapsed_us = now_us - alarm->last_check_time_us;

    if (elapsed_us >= CONFIG_ALARM_REFRESH_INTERVAL_MS * 1000) {
        uint32_t rand_val = esp_random() % 100;
        alarm->last_state = rand_val < CONFIG_ALARM_THRESHOLD_PERCENT;
        alarm->last_check_time_us = now_us;
    }
    return alarm->last_state;
}
```

Ricompila ed esegui l'applicazione:

* `> ESP-IDF: Build, Flash and Start a Monitor`

Un altro crash! Se hai ancora tempo, prova a risolverlo passando a [Esercizio 3.3](../assignment-3-3/). 

## Conclusione

In questo esercizio, abbiamo imparato come creare un core dump e come analizzarlo per capire il motivo di un crash.
L’analisi del core dump è uno strumento molto potente per il debug delle applicazioni.

### Prossimi passi

> Se hai ancora tempo: [Esercizio 3.3](../assignment-3-3/)

> Altrimenti: [Lezione 4](../lecture-4/)

> Oppure [torna al menù di navigazione](../#agenda)