#!/usr/bin/env python
 
from time import sleep
import time
import os
import smbus
import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO

TREMOLO=127
DRUM=191
SAT=223
VIBRATO=239
STEP=247
REVERB=251
# port A
WAH=254
SHIFT=253

#P1   P2   P3   P4   P5   P6   P7   P8   P9    P10   P11   P12
#B1   B253 B251 B247 B239 B223 B191  B127 A254  A253  A251  A247

 
def send2Pd(message=''):
	try:
	        os.system("echo '"+message+"' | /usr/bin/pdsend 3010")
	except Exception, e1:
		print "Erreur : %s" % e1
	

def drum(status):
        if status==True: message='5 1;'
	else: message='5 0;'
        send2Pd(message)

def reverb(status):
        if status==True: message='0 1;'
        else: message='0 0;'
        send2Pd(message)

def straight(status):
        if status==True: message='2 1;'
        else: message='2 0;'
        send2Pd(message)

def sat(status):
        if status==True: message='3 1;'
        else: message='3 0;'
        send2Pd(message)

def wah(status):
        if status==True: message='4 1;'
        else: message='4 0;'
        send2Pd(message)

def step(status):
        if status==True: message='6 1;'
        else: message='6 0;'
        send2Pd(message)

def tremolo(status):
        if status==True: message='7 1;'
        else: message='7 0;'
        send2Pd(message)

def shift(status):
        if status==True: message='8 1;'
        else: message='8 0;'
        send2Pd(message)

def vibrato(status):
        if status==True: message='1 1;'
        else: message='1 0;'
        send2Pd(message)

def readAllInput():
    global wahState,shiftState,drumState,reverbState,vibratoState,stepState,satState,tremoloState
    global WAH,SHIFT,DRUM,REVERB,VIBRATO, STEP,SAT,TREMOLO
    global bus,ser
    try:
        dt=bus.read_i2c_block_data(0x20,0x12,2) # Read Port A
    except Exception, e5:
        print e5
        display(ser,"Erreur:",str(e5)+"\r\n")
        return False
    print "ok"
    pa = dt[0]
    pb = dt[1]
    if pa==255 and pb==255:
        return False
	# port A processing
    if (pa | WAH)==WAH: wahState=True
    else: wahState=False
    if (pa | SHIFT)==SHIFT:	shiftState=True
    else: shiftState=False
	# port B processing
    if (pb | TREMOLO)==TREMOLO: tremoloState=True
    else: tremoloState=False
    if (pb | DRUM)==DRUM: drumState=True
    else: drumState=False
    if (pb | REVERB)==REVERB: reverbState=True
    else: reverbState=False
    if (pb | VIBRATO)==VIBRATO: vibratoState=True
    else: vibratoState=False
    if (pb | STEP)==STEP: stepState=True
    else: stepState=False
    if (pb | SAT)==SAT: satState=True
    else: satState=False
    return True

def display(ser,txt1,txt2):
    # green foreground
    ser.write(chr(27)+chr(1)+chr(3)+chr(255))
    sleep(0.1)
    ser.write(txt1)
    sleep(0.1)
    # yellow foreground
    ser.write(chr(27)+chr(1)+chr(6)+chr(255))
    sleep(0.1)
    ser.write(txt2)
    sleep(0.1)

def display2(ser,txt):
    # white foreground
    ser.write(chr(27)+chr(1)+chr(7)+chr(255))
    sleep(0.1)
    ser.write(txt)
    sleep(0.1)

# 1 indicates /dev/i2c-1
bus=smbus.SMBus(2)
bus.write_byte_data(0x20,0x00,0xFF) # Port A with A0-A7 input
# enable the pull up resistor with a
bus.write_byte_data(0x20,0x0C,0xFF)
bus.write_byte_data(0x20,0x01,0xFF) # Port B with B0-B7 outputs
bus.write_byte_data(0x20,0x0D,0xFF)

UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600,stopbits=2,xonxoff=0,rtscts=0,dsrdtr=0)
ser.close()
ser.open()
# Fontsize 1
ser.write(chr(27)+chr(4)+chr(1)+chr(255))
ser.write(chr(27)+chr(0)+chr(255))
#backlight
ser.write(chr(27)+chr(14)+chr(20)+chr(255))
display2(ser,"Init en cours...")

drumOn=False
reverbOn=False
satOn=False
stepOn=False
wahOn=False
shiftOn=False
vibratoOn=False
straightOn=True
tremoloOn=False
drum(False)
sat(False)
vibrato(False)
wah(False)
shift(False)
step(False)
reverb(False)
straight(True)
tremolo(False)
readAllInput()
try:
#	screen.addstr(1,1,'DRUM:',curses.color_pair(1))
#	screen.addstr(2,1,'SAT:',curses.color_pair(1))
#	screen.addstr(3,1,'REVERB:',curses.color_pair(1))
#	screen.addstr(4,1,'VIBRATO:',curses.color_pair(1))
#	screen.addstr(5,1,'STEP:',curses.color_pair(1))
#	screen.addstr(6,1,'WAH-WAH:',curses.color_pair(1))
#	screen.addstr(7,1,'SHIFT:',curses.color_pair(1))
#	screen.addstr(8,1,'TREMOLO:',curses.color_pair(1))
#	screen.refresh()
    ser.write(chr(27)+chr(0)+chr(255))
    while True:
        changes=readAllInput()
        if changes==False:
            sleep(0.3)
            continue		
        if drumOn==False and drumState==True:
            #print "Drum On"
            display(ser,"Drum","ON")
            drumOn=True
            drum(True)
        elif drumOn==True and drumState==True:
		    #print "Drum Off"
            display(ser,"Drum","OFF")
            drumOn=False
            drum(False)
        if satOn==False and satState==True:
            #print "Sat On"
            display(ser,"Sat","ON")
            satOn=True
            sat(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif satOn==True and satState==True:
            #print "Sat Off"
            display(ser,"Sat","OFF")
            satOn=False
            sat(False)
            if straightOn==False:
                straightOn=True
                straight(True)
        if reverbOn==False and reverbState==True:
            #print "Reverb On"
            display(ser,"Reverb","ON")
            reverbOn=True
            reverb(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif reverbOn==True and reverbState==True:
            #print "Reverb Off"
            display(ser,"Reverb","OFF")
            reverbOn=False
            reverb(False)
            if straightOn==False: 
                straightOn=True
                straight(True)
        if vibratoOn==False and vibratoState==True:
            #print "Vibrato On"
            display(ser,"Vibrato","ON")
            vibratoOn=True
            vibrato(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif vibratoOn==True and vibratoState==True:
            #print "Vibrato off"
            display(ser,"Vibrato","OFF")
            vibratoOn=False
            vibrato(False)
            if straightOn==False:
                straightOn=True
                straight(True)
        if stepOn==False and stepState==True:
            #print "Step On"
            display(ser,"Step","ON")
            stepOn=True
            step(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif stepOn==True and stepState==True:
            #print "Step Off"
            display(ser,"Step","OFF")
            stepOn=False
            step(False)
            if straightOn==False:
                straightOn=True
                straight(True)
        if wahOn==False and wahState==True:
            #print "Wah On"
            display(ser,"WahWah","ON")
            wahOn=True
            wah(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif wahOn==True and wahState==True:
            #print "Wah Off"
            display(ser,"WahWah","OFF")
            wahOn=False
            wah(False)
            if straightOn==False:
                straightOn=True
                straight(True)
        if shiftOn==False and shiftState==True:
            #print "Shift On"
            display(ser,"Shift","ON")
            shiftOn=True
            shift(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif shiftOn==True and shiftState==True:
            #print "shift Off"
            display(ser,"Shift","OFF")
            shiftOn=False
            shift(False)
            if straightOn==False:
                straightOn=True
                straight(True)
        if tremoloOn==False and tremoloState==True:
            #print "Tremolo On"
            display(ser,"Tremolo","ON")
            tremoloOn=True
            tremolo(True)
            if straightOn==True:
                straightOn=False
                straight(False)
        elif tremoloOn==True and tremoloState==True:
            #print "Tremolo Off"
            display(ser,"Tremolo","OFF")
            tremoloOn=False
            tremolo(False)
            if straightOn==False:
                straightOn=True
                straight(True)
		sleep(0.3)
finally:
        # shut down cleanly
        ser.close()
        print "fin du programme"


