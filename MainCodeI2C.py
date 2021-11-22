# Import LCD library
import os
import serial
# Import sleep library
from time import sleep
import RPi.GPIO as GPIO


os.system("cd /home/pi/.local/bin")
from RPLCD import i2c


def SerialCommRead():
    global ser
    if ser.in_waiting>0:
        Val=ser.readline().decode("ascii").rstrip()
        return Val
    
    
        
# constants to initialise the LCD
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

ser=serial.Serial('/dev/ttyUSB0',9600)
ser.flush()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Write a string on first line and move to next line
Mes='Welcome'
while True:
    Val=SerialCommRead()
    ser.flush()
    if str(Val)!='None':
        LocL=Val.find("T")
        LocT=Val.find("H")
        lcd.cursor_pos = (1, 0)
        lcd.write_string('T:'+str(Val[2:LocT-2])+"C H:"+str(Val[LocT+2:-1])+ "%")
        lcd.crlf()
        
    if GPIO.input(10)==GPIO.LOW:
        print("Input Mode Starts")
        Mes=input("Enter Your Message: ")
        while len(Mes)>16:
            print("Please Input Again")
            Mes=input("Enter Your Message: ")
        
    
    lcd.cursor_pos = (0, 0)
    lcd.write_string("                ")
    lcd.cursor_pos = (0, 0)
    lcd.crlf()
    lcd.write_string(Mes)
    lcd.crlf()
    sleep(2)    
    
    
    