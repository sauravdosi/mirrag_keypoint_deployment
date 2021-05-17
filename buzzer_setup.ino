const int LED = 13;
String command;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    command = Serial.readStringUntil("\n");
    command.trim();
    Serial.println(command);

    if(command.equals("on")){
      digitalWrite(LED, HIGH);
      delay(3000);
      digitalWrite(LED, LOW);
    }

    else if(command.equals("off")){
      digitalWrite(LED, LOW);
    }
  }
}
