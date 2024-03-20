import time
import max30100
import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()


mx30 = max30100.MAX30100()
mx30.enable_spo2()
BLYNK_AUTH_TOKEN = 'MFeXvZ4CbTzo9WEEvQ2ah-06HlpjOk1X'
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
hb=0
spo2=0;
percentage=0
# Create BlynkTimer Instance
timer = BlynkTimer()
GAIN = 1
# function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    print(".......................................................")
    print("................... By SME Dehradun ...................")
    time.sleep(2);

# Functon for collect data from sensor & send it to Server
def myData():
    blynk.virtual_write(0,hb)
    blynk.virtual_write(1,spo2)
    blynk.virtual_write(2,percentage)
    #print("Values sent to New Blynk Server!")

timer.set_interval(2, myData)

while 1:
    try:
        blynk.run()
        timer.run()
        mx30.read_sensor()

        mx30.ir, mx30.red

        hb = int(mx30.ir / 100)
        spo2 = int(mx30.red/100)-10
    
        if mx30.ir != mx30.buffer_ir :
            print("Pulse:",hb);
        if mx30.red != mx30.buffer_red:
            print("SPO2:",spo2)
        value = adc.read_adc_difference(0, gain=GAIN)
        #val2=adc.read_adc_difference(1, gain=GAIN)
        volt=value*0.000125
        max=3.7
        per=(volt/max)*100
        percentage=int(per)
        print(percentage)
        time.sleep(0.5)


    except:
        print("No Beat Found")

    time.sleep(1)

