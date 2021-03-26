#include <ESP32Servo.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>

//set up to connect to an existing network
const char* ssid = "Hotspot";
const char* password = "guest_pw";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;  //  port to listen on
char incomingPacket[255];  // buffer for incoming packets

Servo myservo;  // create servo object to control a servo

int posVal = 0;    // variable to store the servo position
int servoPin = 15; // Servo motor pin

long startTime;

void setup() {
  int status = WL_IDLE_STATUS;
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to wifi");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  // we recv one packet from the remote so we can know its IP and port
  bool readPacket = false;
  while (!readPacket) {
    int packetSize = Udp.parsePacket();
    if (packetSize)
     {
      // receive incoming UDP packets
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if (len > 0)
      {
        incomingPacket[len] = 0;
      }
      Serial.printf("UDP packet contents: %s\n", incomingPacket);
      readPacket = true;
    } 
  }
  
  myservo.setPeriodHertz(50);           // standard 50 hz servo
  myservo.attach(servoPin, 500, 2500);  // attaches the servo on servoPin to the servo object
  delay(200); 
  startTime = millis();  
}


void loop() {
  delay(5000);

  // servo runs for 20 seconds
  while (millis() < startTime + 20000) {
    Serial.printf("moving");
    
    for (posVal = 40; posVal >= 0; posVal -= 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(posVal);       // tell servo to go to position in variable 'pos'
      delay(15);                   // waits 15ms for the servo to reach the position
    }
  
    for (posVal = 0; posVal <= 40; posVal += 1) { // goes from 180 degrees to 0 degrees
      myservo.write(posVal);       // tell servo to go to position in variable 'pos'
      delay(15);                   // waits 15ms for the servo to reach the position
    }
  }
  bool readPacket = false;
  while (!readPacket) {
    int packetSize = Udp.parsePacket();
    if (packetSize)
     {
      // receive incoming UDP packets
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if (len > 0)
      {
        incomingPacket[len] = 0;
      }
      Serial.printf("UDP packet contents: %s\n", incomingPacket);
      readPacket = true;
      startTime = millis();
    } 
  }
}
