


#include <QTRSensors.h>

QTRSensors qtr;

const uint8_t SensorCount = 7;
uint16_t sensorValues[SensorCount];





int mod = 3;
int ib1 = 11;
int ib2 = 10;
int viteza_stanga = -50;
int ia1 = 9;
int ia2 = 6;
float cx = 0;
int viteza_curenta_stanga = 0;
int viteza_curenta_dreapta = 0;
int boost = 0;
int vs_pid = 0;
int vd_pid = 0;
int cf_bun = 0;
int cf_calculat = 0;
int j = 0;
int j1 = 0;
float KP = 0.2;
float KD = 2;
int M1 = 20;
int M2 = 20;
float a = 0.1;
int b = 5;
float cxp = 0; //precedent lui cx
float S0 = 0;
float S1 = 0;
float S2 = 0;
float S3 = 0;
int index_viteza = 0;
float S4 = 0;
float S5 = 0;
float S6 = 0;






int cf_corecte[40] = {};






void setup()
{
  // configure the sensors

  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){ 12 ,8, 7,13, 5, 4, 3}, SensorCount);
  
  pinMode(ia1, OUTPUT);
  pinMode(ib1, OUTPUT);
  pinMode(ia2, OUTPUT);
  pinMode(ib2, OUTPUT);
  qtr.setEmitterPin(2);

  delay(500);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode

  // analogRead() takes about 0.1 ms on an AVR.
  // 0.1 ms per sensor * 4 samples per sensor read (default) * 6 sensors
  // * 10 reads per calibrate() call = ~24 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  qtr.emittersOn();
  for (int i = 0; i < 250; i++)
  {
    qtr.calibrate();
    delay(5);
  }
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration

  // print the calibration minimum values measured when emitters were on
  Serial.begin(115200);
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.minimum[i]);
    Serial.print(' ');
  }
  Serial.println();

  // print the calibration maximum values measured when emitters were on
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.maximum[i]);
    Serial.print(' ');
  }
  Serial.println();
  Serial.println();
  delay(50);
  
  /*
  for (int i=0;i<255;i++){
      dreapta(i);
      stanga(i);
      delay(100);  
  }
  
  for (int i=0;i>-255;i--){
      dreapta(i);
      stanga(i);
      delay(100);  
  }
  
  */
  dreapta(0);
  stanga(0);
  
}



void dreapta(int viteza)
{
   if(viteza > 0)
   {
     digitalWrite(ia1, HIGH);
     analogWrite(ib1, 255-viteza);  
   }
   if(viteza < 0)
   {
     digitalWrite(ia1, LOW);
     analogWrite(ib1, viteza);  
   } 
   //Serial.print("viteza_d = ");
   //Serial.println(viteza);
}

void stanga(int viteza)
{
  
   if(viteza > 0)
   {
     digitalWrite(ia2, HIGH);
     analogWrite(ib2, 255-viteza);  
   }
   if(viteza < 0)
   {
     digitalWrite(ia2, LOW);
     analogWrite(ib2, (viteza));  
   }
   //Serial.print("viteza_d = ");
   //Serial.println(viteza); 
}



int lastError = 0;
 
void loop()
{
   //if (1==1) return;
  
   int position = qtr.readLineBlack(sensorValues);
   int error = position - 3300;
   cf_calculat = KP*error+KD*(error-lastError);
   lastError = error;
  
   cf_calculat /= 7;
   /*
   Serial.print(" S0 = ");Serial.print(sensorValues[0]);
   Serial.print(" S1 = ");Serial.print(sensorValues[1]);
   Serial.print(" S2 = ");Serial.print(sensorValues[2]);
   Serial.print(" S3 = ");Serial.print(sensorValues[3]);
   Serial.print(" S4 = ");Serial.print(sensorValues[4]);
   Serial.print(" S5 = ");Serial.print(sensorValues[5]);
   Serial.print(" S6 = ");Serial.print(sensorValues[6]);Serial.println();
   */
   /*
   if(sensorValues[0] >= 900 && sensorValues[1] >= 900 && mod != 2 && sensorValues[2] >= 900)
   {
      mod = 2; // dreapta   
   }
   else if(sensorValues[4] >= 900 && sensorValues[5] >= 900 && mod != 1 && sensorValues[6] >= 900)
   {
      mod = 1; //stanga
   }
   else if ((sensorValues[2] >= 800 || sensorValues[3] >= 800) && sensorValues[0]<=200 && sensorValues[6]<=200)
   {
      mod = 3; //PID
   }
   */
  
  
  
    if (sensorValues[5] >= 150 && sensorValues[6] >= 150 /*sensorValues[5] >= 900  && sensorValues[6] >= 600 && sensorValues[4] >= 400*/ && mod != 2 ) mod=1;
    else if (sensorValues[0] >= 400 /*  && sensorValues[1] >= 600 && sensorValues[2] >= 300 */ && mod != 1) mod=2;
    else if ((sensorValues[3] >= 500 || sensorValues[4] >= 700 || sensorValues[2] >= 500) && sensorValues[0]<=350 && sensorValues[6]<=350) mod=3;   
   
   if(mod == 1)
   {  
     boost = 0;
     j = 0;
     /*
      if (viteza_curenta_stanga<100){
          viteza_curenta_stanga += 5;
      }else{
          viteza_curenta_stanga = 100;
      }
      if (viteza_curenta_dreapta>-100){
          viteza_curenta_dreapta -= 25;
      }else{
          viteza_curenta_dreapta = -100;
      }    
      */
      stanga(120);
      dreapta(0-120);
      //Serial.print(" MOD   1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! = ");
   }
   else if(mod == 2)
   {
      
      boost = 0;
      j = 0;
       /*
      if (viteza_curenta_stanga>-100) {
          viteza_curenta_stanga -= 25;
      }else{
          viteza_curenta_stanga = -100;
      }   
       
      if (viteza_curenta_dreapta<120){
          viteza_curenta_dreapta += 8;
      }else{
          viteza_curenta_dreapta = 120;
      }*/
      stanga(0-120);
      dreapta(120);
      //Serial.println(" MOD 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! = ");
    
   }
   else if(mod == 3)
   {
      
      viteza_curenta_stanga = 125 + cf_calculat + boost;
      viteza_curenta_dreapta = 125 - cf_calculat + boost;
      if( viteza_curenta_stanga > 255) viteza_curenta_stanga = 254;
      if(viteza_curenta_dreapta  > 255) viteza_curenta_dreapta = 254;
      
      //j1 = 0;
      dreapta(viteza_curenta_dreapta);
      stanga(viteza_curenta_stanga);
      if(j > 30) boost += 2;
      if(boost >= 90) boost = 90;
      
      //Serial.println(" MOD 3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! = ");
      j++;
      
   }
   
   
   /*
   Serial.print(" S0 = ");
   Serial.print(sensorValues[0]);
   Serial.print("  S1 = ");
   Serial.print(sensorValues[1]);
   Serial.print("  S2 = ");
   Serial.print(sensorValues[2]);
   Serial.print("  S3 = ");
   Serial.print(sensorValues[3]);
   Serial.print("  S4 = ");
   Serial.print(sensorValues[4]);
   Serial.print("  S5 = ");
   Serial.print(sensorValues[5]);
   Serial.print("  S6 = ");
   Serial.print(sensorValues[6]);
   
   Serial.print(" cx = ");
   Serial.print(cx);
   
   Serial.print(" i = ");
   Serial.print(index_viteza);
   
   Serial.print(" cf_calculat = ");
   Serial.print(cf_calculat);
   
   Serial.print(" cx = ");
   Serial.print(cx);
   Serial.print(" cxp = ");
   Serial.print(cxp);
   Serial.print(" position = ");
   Serial.print(position);
   Serial.print(" mod = ");
   Serial.print(mod);
    
   Serial.println();
   */
    cxp = cx;
 //   delay(500);
 /*
   Serial.print(" cf_calculat = ");
   Serial.print(cf_calculat);
   Serial.print(" vs = ");
   Serial.print(viteza_curenta_stanga);
   Serial.print(" vd = ");
   Serial.print(viteza_curenta_dreapta);
   Serial.print(" position = ");
   Serial.print(position);
   */

}



