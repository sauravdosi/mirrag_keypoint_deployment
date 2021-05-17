const int LED = 13; // assign the correct pin for the input signal of the buzzer
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
      
      // Time in milliseconds for which the buzzer will be turned on once a trigger is received
      delay(3000);
      
      digitalWrite(LED, LOW);
    }

    else if(command.equals("off")){
      digitalWrite(LED, LOW);
    }
  }
}
