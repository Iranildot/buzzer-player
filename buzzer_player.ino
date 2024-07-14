#define part1_pin 3
#define part2_pin 5
#define part3_pin 6
#define part4_pin 9

/// TIME COUNTING
typedef struct {
  unsigned long current;
  unsigned long variation;
  unsigned long start;
  unsigned long end;
}time_counting;

typedef struct {
  bool started;
  unsigned long frequency;
  unsigned long duration;
  time_counting time_counting;
}part_info;

part_info part1_info;
part_info part2_info;
part_info part3_info;
part_info part4_info;

bool timer(time_counting *time, unsigned long stipulated_time);
void reset_timer(time_counting *time);


void setup() {
  Serial.begin(9600); // Iniciar comunicação serial a 9600 bps
  pinMode(part1_pin, OUTPUT);
  pinMode(part2_pin, OUTPUT);
  pinMode(part3_pin, OUTPUT);
  pinMode(part4_pin, OUTPUT);

  part1_info.started = false;
  part2_info.started = false;
  part3_info.started = false;
  part4_info.started = false;

}

void loop() {
    if (part1_info.started){
      if (timer(&part1_info.time_counting, part1_info.duration)){
        part1_info.started = false;
        noTone(part1_pin);
        Serial.print('0');
      }
    }
    if (part2_info.started){
      if (timer(&part2_info.time_counting, part2_info.duration)){
        part2_info.started = false;
        noTone(part2_pin);
        Serial.print('1');
      }
    }
    if (part3_info.started){
      if (timer(&part3_info.time_counting, part3_info.duration)){
        part3_info.started = false;
        noTone(part3_pin);
        Serial.print('2');
      }
    }
    if (part4_info.started){
      if (timer(&part4_info.time_counting, part4_info.duration)){
        part4_info.started = false;
        noTone(part4_pin);
        Serial.print('3');
      }
    }

  if (Serial.available()) {

    String part = Serial.readStringUntil(':'); // Ler comando da porta serial
  
    if (part.equals("0")) {
      part1_info.started = true;
      String frequency = Serial.readStringUntil(':');
      if (!frequency.equals("REST")) {
        part1_info.frequency = frequency.toInt();
        tone(part1_pin, part1_info.frequency);
      }
      part1_info.duration = Serial.readStringUntil('\r\n').toInt();
      reset_timer(&part1_info.time_counting);
    } else if (part.equals("1")) {
      part2_info.started = true;
      String frequency = Serial.readStringUntil(':');
      if (!frequency.equals("REST")) {
        part2_info.frequency = frequency.toInt();
        tone(part2_pin, part2_info.frequency);
      }
      part2_info.duration = Serial.readStringUntil('\r\n').toInt();
      reset_timer(&part2_info.time_counting);
    } else if (part.equals("2")) {
      part3_info.started = true;
      String frequency = Serial.readStringUntil(':');
      if (!frequency.equals("REST")) {
        part3_info.frequency = frequency.toInt();
        tone(part3_pin, part3_info.frequency);
      }
      part3_info.duration = Serial.readStringUntil('\r\n').toInt();
      reset_timer(&part3_info.time_counting);
    } else if (part.equals("3")) {
      part4_info.started = true;
      String frequency = Serial.readStringUntil(':');
      if (!frequency.equals("REST")) {
        part4_info.frequency = frequency.toInt();
        tone(part4_pin, part4_info.frequency);
      }
      part4_info.duration = Serial.readStringUntil('\r\n').toInt();
      reset_timer(&part4_info.time_counting);
    }
    Serial.print('5');
  }
}

// TIMER
bool timer(time_counting *time, unsigned long stipulated_time){

  time->end = millis();
  time->variation = time->end - time->start;
  
  // HANDLES WHEN MILLIS() EXCEEDS ITS MAX CAPACITY
  if (time->end < time->start)
    time->variation = 4294967295 + time->end - time->start;
  
  time->start = time->end; // RESET THE TIME COUNT
  
  // ADD VARIATION OF TIME TO CURRENT TIME
  time->current += time->variation;
  
  return time->current >= stipulated_time;
}

// TIMER RESETTER
void reset_timer(time_counting *time){
  time->current = 0;
  time->variation = 0;
  time->start = millis();
  time->end = millis();
}
