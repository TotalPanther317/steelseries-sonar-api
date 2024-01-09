#include "MIDIUSB.h"

int pot1 = 0;
int old1 = 0;
int pot2 = 0;
int old2 = 0;
int pot3 = 0;
int old3 = 0;
int pot4 = 0;
int old4 = 0;
int pot5 = 0;
int old5 = 0;
int pot6 = 0;
int old6 = 0;
int pot7 = 0;
int old7 = 0;
int pot8 = 0;
int old8 = 0;
int pot9 = 0;
int old9 = 0;
int pot10 = 0;
int old10 = 0;

int mapToMin = 0;
int mapToMax = 127;

void setup() {
  Serial.begin(115200);
}

// First parameter is the event type (0x0B = control change).
// Second parameter is the event type, combined with the channel.
// Third parameter is the control number number (0-119).
// Fourth parameter is the control value (0-127).

void controlChange(byte channel, byte control, byte value) {
  midiEventPacket_t event = {0x0B, 0xB0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}

void loop() {
  pot1 = map(analogRead(A0), 0, 1023, mapToMin, 127);
  if((old1 < pot1 - 1) || (old1 > pot1 + 1)){
    old1 = pot1;
    controlChange(0, 0, pot1);
    MidiUSB.flush();
    //delay(50);
  }
  
  pot2 = map(analogRead(A1), 0, 1023, mapToMin, mapToMax);
  if((old2 < pot2 - 1) || (old2 > pot2 + 1)){
    old2 = pot2;
    controlChange(0, 1, pot2);
    MidiUSB.flush();
    //delay(50);
  }
  
  pot3 = map(analogRead(A2), 0, 1023, mapToMin, mapToMax);
  if((old3 < pot3 - 1) || (old3 > pot3 + 1)){
    old3 = pot3;
    controlChange(0, 2, pot3);
    MidiUSB.flush();
    //delay(100);
  }
  
  pot4 = map(analogRead(A3), 0, 1023, mapToMin, mapToMax);
  if((old4 < pot4 - 1) || (old4 > pot4 + 1)){
    old4 = pot4;
    controlChange(0, 3, pot4);
    MidiUSB.flush();
    //delay(100);
  }

  pot5 = map(analogRead(A4), 0, 1023, mapToMin, mapToMax);
  if((old5 < pot5 - 1) || (old5 > pot5 + 1)){
    old5 = pot5;
    controlChange(0, 4, pot5);
    MidiUSB.flush();
    //delay(50);
  }
  
  pot6 = map(analogRead(A5), 0, 1023, mapToMin, mapToMax);
  if((old6 < pot6 - 1) || (old6 > pot6 + 1)){
    old6 = pot6;
    controlChange(0, 5, pot6);
    MidiUSB.flush();
    //delay(50);
  }
  
  pot7 = map(analogRead(A7), 0, 1023, mapToMin, mapToMax);
  if((old7 < pot7 - 1) || (old7 > pot7 + 1)){
    old7 = pot7;
    controlChange(0, 6, pot7);
    MidiUSB.flush();
    //delay(100);
  }
  
  pot8 = map(analogRead(A8), 0, 1023, mapToMin, mapToMax);
  if((old8 < pot8 - 1) || (old8 > pot8 + 1)){
    old8 = pot8;
    controlChange(0, 7, pot8);
    MidiUSB.flush();
    //delay(100);
  }

  pot9 = map(analogRead(A9), 0, 1023, mapToMin, mapToMax);
  if((old9 < pot9 - 1) || (old9 > pot9 + 1)){
    old9 = pot9;
    controlChange(0, 8, pot9);
    MidiUSB.flush();
    //delay(100);
  }

  pot10 = map(analogRead(A10), 0, 1023, mapToMin, mapToMax);
  if((old10 < pot10 - 1) || (old10 > pot10 + 1)){
    old10 = pot10;
    controlChange(0, 9, pot10);
    MidiUSB.flush();
    //delay(100);
  }
}
