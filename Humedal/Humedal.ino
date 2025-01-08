/*
  Sistema de monitoreo Arduino

  Este Sistema requiere la medicion de diferentes parametros como lo puede ser:
    
    - Temperatura
    - Humedad ambiente 
    - *Humedad de suelo
  
  Para esto se utilizo:
    
    - 4 sensores DHT22
    - 2 capacitive soil

  Se definieron los siguientes puertos

  -	Sensor DHT22(1): GPIO15 – Sensor ubicado en la barra derecha, parte superior.
  -	Sensor DHT22(2): GPIO2 – Sensor ubicado en la barra derecha, parte inferior.
  -	Sensor DHT22(3): GPIO4 – Sensor ubicado en la barra izquierda, parte inferior.
  -	Sensor DHT22(4): GPIO5 – Sensor ubicado en la barra izquierda, parte superior.

  - Sensor Capacitive Soil(1): GPIO34 -  barra derecha
  -	Sensor Capacitive Soil(2): GPIO35 -  barra izquierda



*/


#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHTPIN1 15
#define DHTPIN2 2
#define DHTPIN3 4
#define DHTPIN4 5


#define DHTTYPE DHT22

DHT dht1(DHTPIN1, DHTTYPE);  // Barra Superior Derecha
DHT dht2(DHTPIN2, DHTTYPE);  // Barra inferior Derecha
DHT dht3(DHTPIN3, DHTTYPE);  // Barra inferior Izquierda
DHT dht4(DHTPIN4, DHTTYPE);  // Barra Superior Izquierda

const char* ssid = "SDaniel";
const char* password = "12345678";
const char* serverName = "https://d3b4-200-14-226-170.ngrok-free.app/guardar_datos_sensor/";

const int soilSensor1Pin = 34;  // barra izquierda
const int soilSensor2Pin = 35;  // barra  derecha

const int id_sensor_1 = 3;  // Barra Superior Derecha
const int id_sensor_2 = 5;  // Barra inferior Derecha
const int id_sensor_3 = 6;  // Barra inferior Izquierda
const int id_sensor_4 = 4;  // Barra Superior Izquierda

/*
 if (!SPIFFS.begin(true)) {
    Serial.println("Error al montar SPIFFS");
    return;
}
*/
void setup() {
  Serial.begin(115200);

  dht1.begin();
  dht2.begin();
  dht3.begin();
  dht4.begin();

  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Conectado a la red Wi-Fi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
}
/*
  Se genera el envio de los datos leidos en formato JSON, 

  id_sensor: id
  valor: {0-100}
  tipo: {Humedad | humedad de suelo | Temperatura}

*/
void enviarDato(int id_sensor, float valor, String tipo) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"id_sensor\":" + String(id_sensor) + ",\"valor\":" + String(valor, 1) + ",\"tipo\":\"" + tipo + "\"}";

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Código de respuesta: " + String(httpResponseCode));
      Serial.println("Respuesta del servidor: " + response);
    } else {
      Serial.print("Error en la solicitud: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi no conectado");
  }
}

/*
  Se realiza un registro de un txt. 
  Este es el formato

  Fecha - Id_sensor - Tipo - Valor:00
  [02-01-2025 12:25; Id_sensor:3; Tipo: Temperatura; Valor:25];

  importante guardar el archivo aqui

  C:\Users\Sala409-04\Documents\IOT
  
*/

/*
void RegistrarDatos(int id_sensor, float valor, String tipo) {
  File file = SPIFFS.open("/datos.txt", FILE_APPEND);
  if (!file) {
    Serial.println("Error al abrir el archivo para escribir.");
    return;
  }

  String fecha = String(__DATE__) + " " + String(__TIME__);
  String logEntry = "[" + fecha + "; Id_sensor:" + String(id_sensor) + "; Tipo: " + tipo + "; Valor:" + String(valor, 1) + "]\n";
  file.print(logEntry);
  file.close();
}
*/

void loop() { 
 
  float temperatura1 = dht1.readTemperature(); 
  float humedad1 = dht1.readHumidity(); 
 
  float temperatura2 = dht2.readTemperature(); 
  float humedad2 = dht2.readHumidity(); 
 
  float temperatura3 = dht3.readTemperature(); 
  float humedad3 = dht3.readHumidity(); 
 
  float temperatura4 = dht4.readTemperature(); 
  float humedad4 = dht4.readHumidity(); 
 
  int soilMoisture1 = analogRead(soilSensor1Pin);   
  int soilMoisture2 = analogRead(soilSensor2Pin);   
 
  if (!isnan(temperatura1) && !isnan(humedad1)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor DHT1:"); 
    Serial.print("  Temperatura: "); 
    Serial.println(temperatura1); 
    Serial.print("  Humedad: "); 
    Serial.println(humedad1); 
    enviarDato(id_sensor_1, temperatura1, "Temperatura"); 
    enviarDato(id_sensor_1, humedad1, "Humedad"); 
    Serial.println("======================================="); 
  } 

  if (!isnan(temperatura2) && !isnan(humedad2)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor DHT2:"); 
    Serial.print("  Temperatura: "); 
    Serial.println(temperatura2); 
    Serial.print("  Humedad: "); 
    Serial.println(humedad2); 
    enviarDato(id_sensor_2, temperatura2, "Temperatura"); 
    enviarDato(id_sensor_2, humedad2, "Humedad"); 
    Serial.println("======================================="); 
  } 
 
  if (!isnan(temperatura3) && !isnan(humedad3)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor DHT3:"); 
    Serial.print("  Temperatura: "); 
    Serial.println(temperatura3); 
    Serial.print("  Humedad: "); 
    Serial.println(humedad3); 
    enviarDato(id_sensor_3, temperatura3, "Temperatura"); 
    enviarDato(id_sensor_3, humedad3, "Humedad"); 
    Serial.println("======================================="); 
  } 
 
  if (!isnan(temperatura4) && !isnan(humedad4)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor DHT4:"); 
    Serial.print("  Temperatura: "); 
    Serial.println(temperatura4); 
    Serial.print("  Humedad: "); 
    Serial.println(humedad4); 
    enviarDato(id_sensor_4, temperatura4, "Temperatura"); 
    enviarDato(id_sensor_4, humedad4, "Humedad"); 
    Serial.println("======================================="); 
  } 
 
  if (!isnan(soilMoisture1)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor de Humedad de Suelo 1:"); 
    Serial.print("  Humedad del Suelo: "); 
    Serial.println(soilMoisture1); 
    enviarDato(id_sensor_1, soilMoisture1, "Humedad_Suelo"); 
    Serial.println("======================================="); 
  } 
 
  if (!isnan(soilMoisture2)) { 
    Serial.println("======================================="); 
    Serial.println("Sensor de Humedad de Suelo 2:"); 
    Serial.print("  Humedad del Suelo: "); 
    Serial.println(soilMoisture2); 
    enviarDato(id_sensor_2, soilMoisture2, "Humedad_Suelo"); 
    Serial.println("======================================="); 
  } 
 
  delay(10000);

} 


 