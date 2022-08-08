#include <Arduino.h>
#include "WiFi.h" 
#include "driver/adc.h"
#include <esp_wifi.h>
#include <esp_bt.h>

#define WAIT_LOT(a) for(j = 0; j < 14; j++) {  __asm__ __volatile__ ("nop"); }
#define STEP_SIZE 3
#define N_FRAMES 24

int i = 0;
int j = 0;
String incoming = "";
char inChar;

int frame = 0;
int frame_ = 0;
int positive_positive[4] = {GPIO_OUT_W1TC_REG, GPIO_OUT_W1TS_REG, GPIO_OUT_W1TC_REG, GPIO_OUT_W1TS_REG};
int positive_negative[4] = {GPIO_OUT_W1TC_REG, GPIO_OUT_W1TS_REG, GPIO_OUT_W1TS_REG, GPIO_OUT_W1TC_REG};
int negative_negative[4] = {GPIO_OUT_W1TS_REG, GPIO_OUT_W1TC_REG, GPIO_OUT_W1TS_REG, GPIO_OUT_W1TC_REG};
int negative_positive[4] = {GPIO_OUT_W1TS_REG, GPIO_OUT_W1TC_REG, GPIO_OUT_W1TC_REG, GPIO_OUT_W1TS_REG};

int* positions[24][24] =
{
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,negative_negative},
  {negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative,positive_negative},
  {positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,positive_positive,negative_positive,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,negative_negative,positive_negative}
};

TaskHandle_t Task1;
TaskHandle_t Task2;

void SignalGenerator( void * pvParameters ){
  loop:
    frame_ = frame;
    for(i = 0; i <= 23; i++){
      REG_WRITE(positions[frame_][i][0], BIT18); REG_WRITE(positions[frame_][i][1],BIT19); REG_WRITE(positions[frame_][i][2], BIT21); REG_WRITE(positions[frame_][i][3], BIT22);
      WAIT_LOT();
    }
  goto loop;
}

void CommandReader( void * pvParameters ){
  for(;;){
    if(Serial.available()>0){
      inChar = (char) Serial.read();
      incoming += inChar;
      if(incoming == "+"){
        if ( frame >= N_FRAMES-STEP_SIZE ) { 
              frame = 0;
            }
        else {
              frame+=STEP_SIZE; 
            }  
      }
      else if(incoming == "-"){
        if( frame < STEP_SIZE ) { 
              frame = N_FRAMES-1;
           }
        else{
              frame-=STEP_SIZE; 
           } 
      }
      else if(incoming == "r"){
        frame == 0;  
      }

      incoming = "";
    }
    delay(10);
  }
}

void setup() {
  // disable everything that we do not need 
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  btStop();
  esp_wifi_stop();
  esp_bt_controller_disable();

  Serial.begin(115200);
  delay(1000);

  frame = 0;

  REG_WRITE(GPIO_ENABLE_REG, BIT18 + BIT19 + BIT21 + BIT22); //Definindo Pinos de Saida (GPIO 18, 19, 21, 22)

  disableCore0WDT();
  // disableCore1WDT();

  xTaskCreatePinnedToCore(
                    SignalGenerator,   /* Task function. */
                    "SignalGenerator",     /* name of task. */
                    8192,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task1,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */                  
  delay(500); 

  xTaskCreatePinnedToCore(
                    CommandReader,   /* Task function. */
                    "CommandReader",     /* name of task. */
                    10000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task2,      /* Task handle to keep track of created task */
                    1);          /* pin task to core 1 */
  delay(500); 
}

void loop() {
  
}