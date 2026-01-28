#include <WiFi.h>
#include <FirebaseESP32.h>

// --- 1. UNIQUE IDENTITY (Differentiation) ---
#define DEVICE_ID "LIGHT_UNIT_01" 

// --- 2. NETWORK CREDENTIALS ---
#define WIFI_SSID "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// --- 3. FIREBASE CONFIGURATION ---
#define FIREBASE_HOST "light-40317-default-rtdb.asia-southeast1.firebasedatabase.app"
#define FIREBASE_AUTH "PASTE_YOUR_DATABASE_SECRET_HERE" 

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void setup() {
  Serial.begin(115200);
  WiFi.begin(Rendezvous, mochimochae);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  
  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  float gasValue = analogRead(34); 
  float tempValue = analogRead(35);
  String path = "/" + String(DEVICE_ID);

  // Sending data to unique folders to prevent overlap
  Firebase.setFloat(fbdo, path + "/gas_level", gasValue);
  Firebase.setFloat(fbdo, path + "/temp_level", tempValue);
  Firebase.setString(fbdo, path + "/status", "Online");

  delay(3000); 
}
