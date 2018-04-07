#include<SPI.h>
#include<RF24.h>
int index = 0;
bool gotDataToSend = false;
bool change = false;
bool readIn = false;
bool sendToFrontLoader = false;
bool sendToDumpTruck = false;
bool sendToExcavator = false;
bool gotPreamble = false;
bool gotLocation = false;
String preamble = "";
String location = "";
String frontLoader = "<fl>";
String dumpTruck = "<dt>";
String excavator = "<ex>";

//ce, csn pins
RF24 radio(9,10);

void setup(void)
{
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  digitalWrite(13, change);
}

void loop(void) 
{
  readInData();
  SetChannel();
  sendLocation();
}

void readInData()
{
  while(Serial.available() == 0);

  while(gotLocation == false)
  {
    byte test = Serial.read();
    delay(50);

    if(test == (byte)'<')
    {
      readIn = true;
    }

    if(readIn)
    {
      location.concat(String(char(test)));
    }

    if(test == (byte)'>')
    {
      readIn = false;
      index++;
    }

    if(location.equals(frontLoader))
    {
      sendToFrontLoader = true;
      gotPreamble = true;
      digitalWrite(13,HIGH);

    }

    if(location.equals(dumpTruck))
    {
      sendToDumpTruck = true;
      gotPreamble = true;
    }

    if(location.equals(excavator))
    {
      sendToExcavator = true;
      gotPreamble = true;
    }

    if(gotPreamble && index == 2)
    {
      gotLocation = true;
      gotDataToSend = true;
    }
  }

  gotLocation = false;
  index = 0;
}


void SetChannel()
{
  if(sendToFrontLoader)
  {
    radio.setChannel(0x76);
    sendToFrontLoader = false;
  }
  
  if(sendToDumpTruck)
  {
    radio.setChannel(0x66);
    sendToDumpTruck = false;
  }
  
  if(sendToExcavator)
  {
    radio.setChannel(0x56);
    sendToExcavator = false;
  }
}

void sendLocation()
{
  if(gotDataToSend)
  {
    int messageLength = location.length() + 1;
    const char message[messageLength];
    location.toCharArray(message,messageLength);
    radio.write(&message, sizeof(message));
    Serial.print(location);
    delay(100);
    Serial.flush();
    location = "";
    
    gotDataToSend = false;
  }
  return;
}

