void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0,INPUT);
}

void loop() {

  //int data = analogRead(2);
  // put your main code here, to run repeatedly:
  //if (analogRead(0) < 300) Serial.println("Heavy R");
  //else if (analogRead(0) < 500) Serial.println("Moderate R");
  //else Serial.println("No R");
  
  //Serial.println(data);
  
  int rain = analogRead(A0);

  if(rain<1000) {
    Serial.println("Rain");
  }
  else {
    Serial.println("No Rain");
  }
  delay(1000);
}