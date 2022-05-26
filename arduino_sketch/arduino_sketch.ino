void setup() {
  Serial.begin(9600);

}

void loop() {
  int a;
  String str="";
  String data="";
  if(Serial.available()){
      data=Serial.readString();
      if (data=="open"){
        a=analogRead(0);
        delay(1000);
        str=String(a)+"---------------------------*--------------------*--------------------";
        Serial.println(str);
      }
    }
    
  }
