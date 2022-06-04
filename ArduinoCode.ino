#include <Servo.h>

Servo servoLR, servoUD;

#define dir1PinL  2    //Motor direction
#define dir2PinL  4    //Motor direction
#define speedPinL 6    // Needs to be a PWM pin to be able to control motor speed

#define dir1PinR  7    //Motor direction
#define dir2PinR  8   //Motor direction
#define speedPinR 5    // Needs to be a PWM pin to be able to control motor speed
int parseDataX(String data){
    data.remove(data.indexOf(":"));
    data.remove(0, data.indexOf("X")+1);
    return data.toInt();
}

int parseDataY(String data){
    data.remove(0,data.indexOf(":") + 1);
    data.remove(data.indexOf("Y"), 1);
    return data.toInt();
}

void go_Advance(int t=0)  //Forward
{
  digitalWrite(dir1PinL, HIGH);
  digitalWrite(dir2PinL,LOW);
  digitalWrite(dir1PinR,HIGH);
  digitalWrite(dir2PinR,LOW);
  analogWrite(speedPinL,255);
  analogWrite(speedPinR,255);
  delay(t);
}
void go_Left(int t=0)  //Turn left
{
  digitalWrite(dir1PinL, HIGH);
  digitalWrite(dir2PinL,LOW);
  digitalWrite(dir1PinR,LOW);
  digitalWrite(dir2PinR,HIGH);
  analogWrite(speedPinL,200);
  analogWrite(speedPinR,200);
  delay(t);
}
void go_Right(int t=0)  //Turn right
{
  digitalWrite(dir1PinL, LOW);
  digitalWrite(dir2PinL,HIGH);
  digitalWrite(dir1PinR,HIGH);
  digitalWrite(dir2PinR,LOW);
  analogWrite(speedPinL,200);
  analogWrite(speedPinR,200);
  delay(t);
}
void go_Back(int t=0)  //Reverse
{
  digitalWrite(dir1PinL, LOW);
  digitalWrite(dir2PinL,HIGH);
  digitalWrite(dir1PinR,LOW);
  digitalWrite(dir2PinR,HIGH);
  analogWrite(speedPinL,255);
  analogWrite(speedPinR,255);
  delay(t);
}
void stop_Stop()    //Stop
{
  digitalWrite(dir1PinL, LOW);
  digitalWrite(dir2PinL,LOW);
  digitalWrite(dir1PinR,LOW);
  digitalWrite(dir2PinR,LOW);
}
void setup() {
  servoLR.attach(10);
  servoUD.attach(11);
  servoLR.write(90);
  servoUD.write(90);
  Serial.begin(250000);
  Serial.setTimeout(10);
}
void loop() {
    //james
}
void serialEvent() {
    String data = Serial.readString();
    servoLR.write(parseDataX(data));
    servoUD.write(parseDataY(data));
    if(data.indexOf("W")!=-1){
      go_Advance(30);
    }else if(data.indexOf("S")!=-1){
      go_Back(30);
    }
    if(data.indexOf("A")!=-1){
      go_Left(30);
    }else if(data.indexOf("D")!=-1){
      go_Right(30);
    }
    stop_Stop();
}
