const int trigPin = 13;
const int echoPin = 14;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW); delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;

  // Jika ada objek lebih dekat dari 50cm
  if (distance > 0 && distance < 50) {
    Serial.println("ADA_ORANG"); // Kirim sinyal ke laptop
    delay(5000); // Jeda 5 detik supaya tidak spam foto
  }
  delay(100);
}