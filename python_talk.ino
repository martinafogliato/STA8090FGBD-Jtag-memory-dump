#define DELAY 10000

char val;
int i,j;


void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);

}

void loop() {
   while (Serial.available()>0){
    val = Serial.read();

    if (val == 'g'){
      digitalWrite(2, HIGH);
      delay(2000);
      digitalWrite(2, LOW);
      delay(500);
      Serial.flush();
      Serial.write('k');
      delay(500);
      Serial.flush();
      
    }
   } 
}
