int bit_array[25];        
unsigned long time_now;   
 
int CLOCK_PIN = 4;
int DATA_PIN = 5;
 
void setup() {
  Serial.begin(9600);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(DATA_PIN, INPUT);
}
 
void loop() {
  while (digitalRead(CLOCK_PIN) == LOW) {}  
  time_now = micros();
  while (digitalRead(CLOCK_PIN) == HIGH) {} 
  if ((micros() - time_now) > 500) {        
    decode(); 
  }
}
 
void decode() {
  int sign = 1;
  int i = 0;
  float value = 0.0;
  float result = 0.0;
 
  bit_array[0] = digitalRead(DATA_PIN);       
  while (digitalRead(CLOCK_PIN) == HIGH) {};
 
  for (i = 1; i <= 24; i++) {
    while (digitalRead(CLOCK_PIN) == LOW) { } 
    bit_array[i] = digitalRead(DATA_PIN);  
    while (digitalRead(CLOCK_PIN) == HIGH) {} 
  }
 
  for (i = 1; i <= 20; i++) {                 
      value = value + (pow(2, i-1) * bit_array[i]);
  }
 
  if (bit_array[21] == 1) sign = -1;          

  if (bit_array[24] == 1) {                   
     result = (value*sign) / 2000.00;
     Serial.print(result, 3);                   
     Serial.println(" in");
  } else {
     result = (value*sign) / 100.00;  
     Serial.print(result, 2);                   
     Serial.println(" mm");  
  }
  // Am scos delay(1000) pentru a permite o afișare fluidă, în timp real, în interfața Python.
}