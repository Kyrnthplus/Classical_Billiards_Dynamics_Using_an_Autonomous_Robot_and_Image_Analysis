#include <Servo.h>
#include <VL53L0X.h>
#include <Wire.h>

const int ServoDPin = 11; // Right servo pin
const int ServoEPin = 10; // Left servo pin

Servo ServoD; // Right servo object
Servo ServoE; // Left servo object
#define SHUT_A 6
#define SHUT_B 7
#define SHUT_C 8
#define SensorA_address 42
#define SensorB_address 43
#define SensorC_address 44

VL53L0X sensor_right, sensor_left, sensor_front; // (A=Right, B=Left, C=Front)

const int distMin = 0;
const int distMax = 5000;
bool detected = false;

#define SA 00 // 20
#define SB 00 // 50
#define SC 00 // 15

#define WAIT_MS 25      // Time the robot stops to calculate distances
#define READ_DELAY_MS 2 // Time between distance readings

#define MAX                                                                    \
  500 // Maximum distance we want to ping for (in centimeters). Maximum sensor
      // distance is rated at 400-500cm.
#define DISTANCE_THRESHOLD_MM 200 // Minimum distance for avoidance

#define ROT 1800
#define ROT0 50

#define STOP 1500

#define EF 1590 // 1650
#define DF 1276 // 1306

#define ET 1269 // 1272
#define DT 1593 // 1682

float Pi = 3.14159265359;
//----------------ENCODER-------------//
int lastStateE = HIGH;
int lastStateD = HIGH;
int EFF = 1503;
int DFF = 1387;

int r = 6;
int RTT = 100;

#define vcc 5
#define gnd 4
#define pino_D0 2
#define pino_D1 3

unsigned long countE;
unsigned long countD;
float Time;
float X2 = Time;
float Rr = 12.7;
float Rp = 6.8;
float totalHoles = 90;
int rotation_pulses = 0;
int loop_counter = 1;

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  ServoD.attach(ServoDPin); // Initialize right servo
  ServoE.attach(ServoEPin); // Initialize left servo

  // Set shutdown pins as outputs to control sensor reset states
  pinMode(SHUT_A, OUTPUT);
  pinMode(SHUT_B, OUTPUT);
  pinMode(SHUT_C, OUTPUT);

  Serial.begin(115200);
  Wire.begin();

  pinMode(SHUT_A, INPUT);
  delay(10);
  sensor_right.setAddress(SensorA_address);
  pinMode(SHUT_B, INPUT);
  delay(10);
  sensor_left.setAddress(SensorB_address);
  pinMode(SHUT_C, INPUT);
  delay(10);
  sensor_front.setAddress(SensorC_address);

  sensor_right.init();
  sensor_left.init();
  sensor_front.init();

  sensor_right.setTimeout(500);
  sensor_left.setTimeout(500);
  sensor_front.setTimeout(500);

  sensor_right.startContinuous();
  sensor_left.startContinuous();
  sensor_front.startContinuous();

  // ENCODER
  pinMode(vcc, OUTPUT);
  pinMode(gnd, OUTPUT);
  pinMode(pino_D0, INPUT);
  pinMode(pino_D1, INPUT);

  digitalWrite(vcc, HIGH);
  digitalWrite(gnd, LOW);

  attachInterrupt(1, counterE_ISR, CHANGE);
  attachInterrupt(0, counterD_ISR, CHANGE);

  delay(1000);
}

void loop() { controlMotors(); }

void controlMotors() {
  int DistA = sensor_right.readRangeContinuousMillimeters() + SA;
  int DistB = sensor_left.readRangeContinuousMillimeters() + SB;
  int DistC = sensor_front.readRangeContinuousMillimeters() + SC;

  if (DistA > DISTANCE_THRESHOLD_MM and DistB > DISTANCE_THRESHOLD_MM and
      DistC > (DISTANCE_THRESHOLD_MM)) {
    moveStraight();
  } else {
    ServoD.writeMicroseconds(STOP);
    ServoE.writeMicroseconds(STOP);
    delay(WAIT_MS);

    float DistA = 0;
    float DistB = 0;
    float DistC = 0;
    const int numReadings = 1;

    for (int i = 0; i < numReadings; i++) {
      DistA += sensor_right.readRangeContinuousMillimeters() + SA;
      DistB += sensor_left.readRangeContinuousMillimeters() + SB;
      DistC += sensor_front.readRangeContinuousMillimeters() + SC;
      delay(READ_DELAY_MS);
    }

    DistA /= numReadings;
    DistB /= numReadings;
    DistC /= numReadings;

    if (DistC <= DistB and DistC < DistA) {
      ServoD.writeMicroseconds(DF);
      ServoE.writeMicroseconds(ET);
      float A = DistA;
      float B = DistB;
      float C = sqrt(pow(A, 2) + pow(B, 2));
      float D = A * B / C;
      float N = pow(A, 2) / C;
      float M = pow(B, 2) / C;
      float H = acos((pow(A, 2) + pow(D, 2) - pow(N, 2)) / (2 * A * D));
      float J = acos((pow(B, 2) + pow(D, 2) - pow(M, 2)) / (2 * B * D));
      float Alfa = H - Pi / 4;
      float Beta = J - Pi / 4;
      float V_Alfa = Pi - 2 * Alfa;
      float V_Beta = Pi - 2 * Beta;

      if (DistA <= DistB) {
        float Time = (V_Beta) / (Pi);
        ServoD.writeMicroseconds(DF);
        ServoE.writeMicroseconds(ET);
        Serial.println(Time);
        X2 = Time;
        rotateLeft();
      } else {
        float Time = (V_Alfa) / (Pi);
        ServoD.writeMicroseconds(DT);
        ServoE.writeMicroseconds(EF);
        Serial.println(Time);
        X2 = Time;
        rotateRight();
      }
    } else {
      if (DistA <= DistB) {
        ServoD.writeMicroseconds(DF);
        ServoE.writeMicroseconds(ET);
        float A = DistA;
        float B = DistB;
        float C = DistC;
        float D = sqrt(pow(A, 2) + pow(C, 2) - A * C * sqrt(2));
        float Alfa = acos((-pow(A, 2) + pow(D, 2) + pow(C, 2)) / (2 * C * D));
        float Time = (2 * Alfa) / (Pi);
        ServoD.writeMicroseconds(DF);
        ServoE.writeMicroseconds(ET);
        Serial.println(Time);
        X2 = Time;
        rotateLeft();
      }
      if (DistB < DistA) {
        ServoD.writeMicroseconds(DT);
        ServoE.writeMicroseconds(EF);
        float A = DistA;
        float B = DistB;
        float C = DistC;
        float E = sqrt(pow(B, 2) + pow(C, 2) - B * C * sqrt(2));
        float Beta = acos((-pow(B, 2) + pow(E, 2) + pow(C, 2)) / (2 * C * E));
        float Time = (Beta * 2) / (Pi);
        ServoD.writeMicroseconds(DT);
        ServoE.writeMicroseconds(EF);
        Serial.println(Time);
        X2 = Time;
        rotateRight();
      }
    }
  }
}

void moveStraight() {
  Serial.println("[INFO] Moving");
  attachInterrupt(1, counterE_ISR, CHANGE);
  attachInterrupt(0, counterD_ISR, CHANGE);
  ServoD.writeMicroseconds(DFF);
  ServoE.writeMicroseconds(EFF);
  delay(RTT);

  detachInterrupt(0);
  detachInterrupt(1);

  if (countE == 0 and countD == 0) {
    ServoD.writeMicroseconds(1500);
    ServoE.writeMicroseconds(1500);
    delay(5000);
  } else {
    if (countE < r) {
      EFF = EFF + 1;
    } else {
      EFF = EFF - 1;
    }

    if (countD < r) {
      DFF = DFF - 1;
    } else {
      DFF = DFF + 1;
    }
  }
  countE = 0;
  countD = 0;
}

void counterE_ISR() { countE++; }
void counterD_ISR() { countD++; }

void rotateRight() {
  Serial.println("[INFO] Rotating Right");
  rotation_pulses =
      (loop_counter == 0) ? (X2 * 0.5 + 0.5) * totalHoles : X2 * totalHoles;
  attachInterrupt(1, counterE_ISR, CHANGE);
  attachInterrupt(0, counterD_ISR, CHANGE);
  while (countE < rotation_pulses && countD < rotation_pulses) {
    ServoD.writeMicroseconds(DT);
    ServoE.writeMicroseconds(EF);
  }
  delay(5);
  detachInterrupt(1);
  detachInterrupt(0);
  countD = 0;
  countE = 0;
  loop_counter = 1;
}

void rotateLeft() {
  Serial.println("[INFO] Rotating Left");
  rotation_pulses =
      (loop_counter == 0) ? (X2 * 0.5 + 0.5) * totalHoles : X2 * totalHoles;
  attachInterrupt(1, counterE_ISR, CHANGE);
  attachInterrupt(0, counterD_ISR, CHANGE);
  while (countE < rotation_pulses && countD < rotation_pulses) {
    ServoE.writeMicroseconds(ET);
    ServoD.writeMicroseconds(DF);
  }
  delay(5);
  detachInterrupt(1);
  detachInterrupt(0);
  countD = 0;
  countE = 0;
  loop_counter = 1;
}
