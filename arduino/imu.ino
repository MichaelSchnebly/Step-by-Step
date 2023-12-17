#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire);  //check I2C device address (by default address is 0x29 or 0x28)
imu::Vector<3> accel, gyro, orient;

double a_constant = 9.80665; //gravitational constant
double a_range = 5; //device range (e.g. 16 means +/- 16g)
double a_max = a_constant*a_range;
// double a_max_mag = sqrt(3*a_max*a_max);

double g_max = 2000; //device range (e.g. 2000 means +/- 2000 °/s)
// double g_max_mag = sqrt(3*g_max*g_max);


class Data {
public:
  // uint8_t channel;
  float ax, ay, az, gx, gy, gz, ox, oy, oz;
  //a: accelerometer
  //g: gyrometer
  //o: orientation
};
Data data;


#define BNO055_ADDRESS 0x28
#define ACC_CONFIG_REGISTER 0x08
#define ACC_CONFIG_VALUE 0x13 //0b00010011: Normal Mode, 125Hz, +/-16G
#define PAGE_ID_REGISTER 0x07
#define PAGE_ID_VALUE_0 0x00
#define PAGE_ID_VALUE_1 0x01

#define BNO055_SAMPLERATE_DELAY_MS (10) //(8)
// #define LAEF_CHANNEL (2)
#define DEBUG false


void bno_setup() {
  Serial.print("Initial Mode: ");
  Serial.println(bno.getMode());

  // Set the correct register page.
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(PAGE_ID_REGISTER);  // PAGE_ID register.
  Wire.write(PAGE_ID_VALUE_1);  // Set to page 1.
  Wire.endTransmission();

  // Set the ACC_CONFIG register value.
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(ACC_CONFIG_REGISTER);
  Wire.write(ACC_CONFIG_VALUE);
  Wire.endTransmission();
  
  // Return to original register page.
  Wire.beginTransmission(BNO055_ADDRESS);
  Wire.write(PAGE_ID_REGISTER);  // PAGE_ID register.
  Wire.write(PAGE_ID_VALUE_0);   // Set to page 0.
  Wire.endTransmission();

  // bno.setMode(OPERATION_MODE_ACCONLY);
  bno.setMode(OPERATION_MODE_NDOF);
  Serial.print("Operation Mode: ");
  Serial.println(bno.getMode());
}


void setup() {
  Serial.begin(1000000);
  // data.channel = LAEF_CHANNEL;
  
  //SETUP SENSOR
  //-----------------------------------------------------------------------------
  // if(!bno.begin(OPERATION_MODE_CONFIG))
  if(!bno.begin(OPERATION_MODE_NDOF))
  {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  // bno_setup();
  //-----------------------------------------------------------------------------

  delay(1000);
}


void loop() {
  unsigned long currentMillis = millis();

  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2

  accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  data.ax = accel.x()/a_max;
  data.ay = accel.y()/a_max;
  data.az = accel.z()/a_max;
  // data.a = accel.magnitude()/a_max_mag;

  gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  data.gx = gyro.x()/g_max;
  data.gy = gyro.y()/g_max;
  data.gz = gyro.z()/g_max;
  // data.g = gyro.magnitude()/g_max_mag;

  orient = bno.getVector(Adafruit_BNO055::VECTOR_GRAVITY);
  data.ox = orient.x()/a_constant;
  data.oy = orient.y()/a_constant;
  data.oz = orient.z()/a_constant;

  Serial.write((uint8_t *)&data, sizeof(data));

  // Only print if DEBUG is true
  if (DEBUG) {
    /* Display the floating point data */
    // Serial.print("CHANNEL: ");
    // print(data.channel);
    Serial.print("    AX: ");
    print(data.ax);
    Serial.print("    AY: ");
    print(data.ay);
    Serial.print("    AZ: ");
    print(data.az);
    // Serial.print("    A: ");
    // print(data.a);
    Serial.print("    GX: ");
    print(data.gx);
    Serial.print("    GY: ");
    print(data.gy);
    Serial.print("    GZ: ");
    print(data.gz);
    // Serial.print("    G: ");
    // print(data.g);
    Serial.print("    OX: ");
    print(data.ox);
    Serial.print("    OY: ");
    print(data.oy);
    Serial.print("    OZ: ");
    print(data.oz);
    Serial.println("\t\t");
  }

  while(millis() < currentMillis + BNO055_SAMPLERATE_DELAY_MS){}
}


void print(double num) {
  if(num >= 0) {
    Serial.print(" ");
  }
  if(abs(num) <= 10) {
    Serial.print(" ");
  }
  if(abs(num) <= 100) {
    Serial.print(" ");
  }
  if(abs(num) <= 1000) {
    Serial.print(" ");
  }
  Serial.print(num, 2);
}