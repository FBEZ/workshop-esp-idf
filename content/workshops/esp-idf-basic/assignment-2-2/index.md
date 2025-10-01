---
title: "ESP-IDF Basics - Assign. 2.2"
date: "2025-08-05"
series: ["WS00A"]
series_order: 6
showAuthor: false
summary: "Add additional routes to the HTTP server to drive the led remotely"
---

The second assignment is to add the following routes to the HTTP server that we created in the previous assignment:


- `GET /led/on` &rarr; turns the LED on and returns JSON {"led": "on"}
- `GET /led/off`&rarr; turns the LED off and returns JSON {"led": "off"}
- `POST /led/blink` &rarr; accepts JSON `{ "times": int, "interval_ms": int }` to blink the LED the specified number of times at the given interval, and returns JSON `{"blink": "done"}`


## Solution Outline

To control the LED, you can use the code from exercise 1.2, included here for convenience.

* Include the GPIO header

  ```c
  #include "driver/gpio.h"
  ```
* Specify the pin to use

  ```c
   #define OUTPUT_LED GPIO_NUM_7
  ```
* Create the LED configuration function (to be called from `app_main`)

  ```c
   static void configure_led(void)
   {
       ESP_LOGI(TAG, "LED Configured!\n");
       gpio_reset_pin(OUTPUT_LED);
       /* Set the GPIO as push/pull output */
       gpio_set_direction(OUTPUT_LED, GPIO_MODE_OUTPUT);
   }
  ```


## Assignment Code

<details>
<summary>Show assignment code</summary>

```c
#include <stdio.h>
#define ESP_WIFI_SSID "TEST_WORKSHOP"
#define ESP_WIFI_PASS "test_esp"
#define ESP_WIFI_CHANNEL 1
#define MAX_STA_CONN 2
#include "esp_wifi.h"
#include "string.h"
#include "esp_log.h"
#include "esp_http_server.h"
#include "driver/gpio.h"

#define OUTPUT_LED GPIO_NUM_7

static const char* TAG = "main";

static void configure_led(void)
{
  ESP_LOGI(TAG, "LED Configured!\n");
  gpio_reset_pin(OUTPUT_LED);
  /* Set the GPIO as push/pull output */
  gpio_set_direction(OUTPUT_LED, GPIO_MODE_OUTPUT);
}

static esp_err_t hello_get_handler(httpd_req_t *req)
{
    const char* resp_str = "<h1>Hello World</h1>";
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

/* Handler definitions */

static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                  int32_t event_id, void* event_data){
    printf("Event number: %ld!\n", event_id);
}


static esp_err_t led_on_handler(httpd_req_t *req)
{
    led_control(1);

    const char* resp_str = "{\"led\": \"on\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t led_off_handler(httpd_req_t *req)
{
    led_control(0);

    const char* resp_str = "{\"led\": \"off\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

/* URI definitions */

static const httpd_uri_t hello_world_uri= {
    .uri       = "/",               
    .method    = HTTP_GET,          
    .handler   = hello_get_handler, 
    .user_ctx  = NULL               
};

static const httpd_uri_t led_on_uri = {
    .uri       = "/led/on",
    .method    = HTTP_GET,
    .handler   = led_on_handler,
    .user_ctx  = NULL
};

static const httpd_uri_t led_off_uri = {
    .uri       = "/led/off",
    .method    = HTTP_GET,
    .handler   = led_off_handler,
    .user_ctx  = NULL
};

void wifi_init_softap(){
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_ap();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT(); // always start from here

    esp_wifi_init(&cfg);

    esp_event_handler_instance_register(WIFI_EVENT,
                                        ESP_EVENT_ANY_ID,
                                        &wifi_event_handler,
                                        NULL,
                                        NULL);

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = ESP_WIFI_SSID,
            .ssid_len = strlen(ESP_WIFI_SSID),
            .channel = ESP_WIFI_CHANNEL,
            .password = ESP_WIFI_PASS,
            .max_connection = MAX_STA_CONN,
            .authmode = WIFI_AUTH_WPA2_PSK,
            .pmf_cfg = {
                .required = true,
            },
        },
    };

    esp_wifi_set_mode(WIFI_MODE_AP);
    esp_wifi_set_config(WIFI_IF_AP, &wifi_config);
    esp_wifi_start();

    ESP_LOGI(TAG, "wifi_init_softap completed. SSID:%s password:%s channel:%d",
             ESP_WIFI_SSID, ESP_WIFI_PASS, ESP_WIFI_CHANNEL);
}

httpd_handle_t start_webserver() {
    httpd_handle_t server = NULL;
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    if (httpd_start(&server, &config) == ESP_OK) {
        ESP_LOGI(TAG, "Server started successfully, registering URI handlers...");
        return server;
    }

    ESP_LOGE(TAG, "Unable to start the server");
    return NULL;
}


void app_main(void)
{
    wifi_init_softap();
    configure_led();
    httpd_handle_t server = start_webserver();

    /* Register URI/Handler */
    httpd_register_uri_handler(server,&hello_world_uri);
    httpd_register_uri_handler(server, &led_on_uri);
    httpd_register_uri_handler(server, &led_off_uri);
}

```
<details>
### Conclusion

Now we have a clear picture of how to connect REST API requests to physical device control. You will work on a more complex application in the last assignment 3.3.

### Next step

If you still have time, you can try this optional assignment.

> Next (optional) assignment &rarr; [Assignment 2.3](../assignment-2-3/)

Otherwise, you can move to the third lecture.

> Next lecture &rarr; [Lecture 3](../lecture-3/)

> Or [go back to navigation menu](../#workshop)