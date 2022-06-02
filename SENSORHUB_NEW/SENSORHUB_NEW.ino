#include <DHT.h>
#include <DHT_U.h>
int IRpin = 5;
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
static const int RXPin = 8, TXPin = 9;
static const uint32_t GPSBaud = 38400;
TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);
DHT dht(2, DHT11);
String msg="";
void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
  dht.begin();
}

void loop()

{
  
  // This sketch displays information every time a new sentence is correctly encoded.
  while (ss.available() > 0)
    if (gps.encode(ss.read())){
    msg="";
    delay(2000);
      displayInfo();
    }
  }

void displayInfo()
{
  if (gps.location.isValid())
  {
    String glat=String(gps.location.lat());
    String glng=String(gps.location.lng());
    msg=msg+ " "+ glat+" "+glng;
  }
  else
  {
    msg=msg+ " "+"No GPS";
  }

  if (gps.date.isValid())
  {
     msg=" "+msg+ String(gps.date.month())+"/"+String(gps.date.day())+"/"+String(gps.date.year())+" ";
  }
  else
  {
     msg=msg+ " "+"No data";
  }

  if (gps.time.isValid())
  {
    msg=msg+ String(gps.time.hour())+":"+String(gps.time.minute())+":"+String(gps.time.second())+"."+String(gps.time.centisecond());
  }
  else
  {
     msg=msg+ " "+"No time";
  }

  
  float temp=dht.readTemperature();
  msg=msg+" "+"Temp="+" "+String(temp);

String message="";
 float volts = analogRead(IRpin)*0.0048828125;
 float distance = 65*pow(volts, -1.10);
 message = message+String(distance)+" ";
 String locationdata=String(gps.location.lat());  
 message = message+String(locationdata)+" ";
 msg=msg+ " "+message;
  delay(2000);

  Serial.println(msg);
  
}
