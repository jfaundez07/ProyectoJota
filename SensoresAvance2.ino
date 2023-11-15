//-----Conexion Wifi y envio de datos-----
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "movistar2,4GHZ_270135";             
const char* password = "QP5bcHfAvNrkntNf6akb";  

const char* ssid1 = "TEST2";             
const char* password1 = "Testing_2K23";  
//---------------------------------------

//------------Temp y huemdad:------------
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>

Adafruit_BME680 bme;

#define SEALEVELPRESSURE_HPA (1010.0)
//---------------------------------------

//---------Material Particulado:---------
#include "RAK12039_PMSA003I.h"

RAK_PMSA003I PMSA003I;
#define SET_PIN   WB_IO6
//---------------------------------------

void setup() {

  // Conectarse a la red WiFi
  WiFi.begin(ssid1, password1);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a la red WiFi...");
  }

  Serial.begin(115200);
  
  //------------Temp y huemdad:------------
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  //---------------------------------------

  //---------Material Particulado:---------
  pinMode(WB_IO2, OUTPUT);
  digitalWrite(WB_IO2, HIGH); 

  pinMode(SET_PIN, OUTPUT);
  digitalWrite(SET_PIN, HIGH);
  //---------------------------------------

  time_t serial_timeout = millis();
  while (!Serial) {
    if ((millis() - serial_timeout) < 5000) {
      delay(100);
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    } else {
      break;
    }
  }

  bme680_init();
  Wire.begin();
  delay(3000);

  //---------Material Particulado:---------
  if(!PMSA003I.begin()) 
  {
    Serial.println("PMSA003I begin fail,please check connection!");
    delay(100);
    while(1);
  }

}

void loop() {

  if (!bme.performReading()) {
    Serial.println("Failed to perform reading :(");
  }

  lectura_Sensores();

  Serial.println("#-----------------------------------------#");
  delay(5000);

}

void lectura_Sensores(){

  PMSA_Data_t data;

  if (PMSA003I.readDate(&data)) {

    Serial.println("PMSA003I read date success.");

    Serial.println("Atmospheric environment:");
    
    float lectura_PM25 = data.pm25_env;
    Serial.print("PM2.5: "); 
    Serial.print(lectura_PM25);
    Serial.println(" [µg/𝑚3]"); 
    
    float lectura_PM10 = data.pm100_env;
    Serial.print("PM10:  "); 
    Serial.print(lectura_PM10);
    Serial.println(" [µg/𝑚3]");

    float lectura_Temperatura = bme.temperature;
    Serial.print("Temperatura: ");
    Serial.print(lectura_Temperatura);
    Serial.println(" *C");

    float lectura_Humedad = bme.humidity;
    Serial.print("Humedad:     ");
    Serial.print(lectura_Humedad);
    Serial.println(" %");

    Serial.println();

    StaticJsonDocument<200> jsonData;

    jsonData["Temperatura"] = lectura_Temperatura; //graoos celsius
    jsonData["Humedad"] = lectura_Humedad; //porcentaje
    jsonData["PM25"] = lectura_PM25; //[ug/m3]
    jsonData["PM10"] = lectura_PM10; //[ug/m3]

    String jsonString;
    serializeJson(jsonData, jsonString);

    if (send_data(jsonString)) {
      Serial.println("Datos enviados con éxito.");
    } else {
      Serial.println("Error al enviar datos.");
    }

  } else {
    Serial.println("PMSA003I read failed!");
  }

}

void bme680_init() { //Funcion para el sensor T y H

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    return;
  }

  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
 
}

bool send_data(String data) {


  if (WiFi.status() == WL_CONNECTED) {

    WiFiClient client;
    HTTPClient http;

    if (http.begin(client, "http://44.219.124.55:8081/POST")) {  //Aqui va la IP
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST(data);

      if (httpResponseCode > 0) {
        http.end();
        return true;
      } else {
        return false;
      }
    }

    return false;
  }

  return false;
}


