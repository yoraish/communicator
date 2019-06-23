#include <SPI.h>
#include <U8g2lib.h>
#define DELAY 300

//pins

int buttonPin = 15;
unsigned long press_start_time = millis();
unsigned long press_duration = 0;
bool value = LOW;
size_t state = 0;

// Set up the oled object
U8G2_SH1106_128X64_NONAME_F_4W_HW_SPI oled(U8G2_R0, 5, 17, 16);

void setup()
{
    Serial.begin(115200);
    Serial.println("button sketch");

    //start oled
    oled.begin(); // initialize the OLED

    //def pins
    pinMode(buttonPin, INPUT_PULLUP);
}

void loop()
{
    switch (state)
    {
    case 0:
        // wait for button press
        value = digitalRead(buttonPin);
        if (value == HIGH)
        {
            press_start_time = millis();
            state = 1;
        }
        break;
    case 1:
        // wait for press to be released
        value = digitalRead(buttonPin);
        if (value == LOW)
        {
            press_duration = millis() - press_start_time;
            state = 2;
        }
        break;
    case 2:
        oled.clearBuffer(); //clear the screen contents
        oled.setFont(u8g2_font_ncenB10_tr);
        char to_print[10];
        float press_duration_sec = press_duration/1000.0;
        dtostrf(press_duration_sec, 4, 3, to_print);
        oled.drawStr(0, 15, to_print);
        oled.sendBuffer(); // update the screen
        state = 0;
        break;
    // case 3:

    //     break;
            }
    }
