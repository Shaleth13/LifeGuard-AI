/*
 * LifeGuard AI - ESP32-S3 sensor acquisition starter.
 *
 * Libraries:
 *   SparkFun MAX3010x Pulse and Proximity Sensor Library
 *   Adafruit MPU6050
 *   Adafruit Unified Sensor
 *
 * Wire MAX30102 + MPU6050 to the ESP32-S3 I2C bus.
 *
 * The example reads MAX30102 IR values and MPU6050 acceleration.
 * A production build should add robust heart-rate/SpO2 filtering,
 * temperature hardware, TinyML/TFLite inference, power management,
 * calibration and medical-device validation.
 */

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not detected.");
    while (true) delay(1000);
  }

  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

  if (!mpu.begin()) {
    Serial.println("MPU6050 not detected.");
    while (true) delay(1000);
  }

  Serial.println("LifeGuard AI sensor node ready.");
}

void loop() {
  long irValue = particleSensor.getIR();

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float motion = sqrt(
    a.acceleration.x * a.acceleration.x +
    a.acceleration.y * a.acceleration.y +
    a.acceleration.z * a.acceleration.z
  );

  Serial.print("IR=");
  Serial.print(irValue);
  Serial.print(" | Motion=");
  Serial.println(motion);

  // TODO for the hardware build:
  // 1. Derive HR/SpO2 using the MAX30102 algorithm.
  // 2. Read body temperature from the chosen temperature sensor.
  // 3. Run the trained TinyML/TFLite model on-device.
  // 4. Trigger BLE/Wi-Fi caregiver synchronization when online.

  delay(500);
}
