'''This should be moved to your rpi
you need to install pigpio
you need to install python-osc

you will need to enable you gpio
with :   sudo pigpiod
and in the configurations

'''

import pigpio
from time import sleep


import pythonosc
from pythonosc import osc_message_builder
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import osc_server
import threading

ip = "" #ip address
fromSensing = 9998 #depending on which port

level = 127
state = 0
pinPan = [4,17]
pinTilt = [19,27]

def nothing(x):
    pass


#-----------------------------------
# handling OSC
#this handles only two categories out of wekinator!!!
def filter_handler(address, *args):
    if not len(args) == 3 or type(args[0]) is not int or type(args[1]) is not float or type(args[2]) is not float:
        print( "euh?")
        return
    hand = args[0]
    pAngle = args[1]
    angleTilt = args[2]

    #filter data

    #move it
    move(pinPan[hand], pAngle, delay=0)
    move(pinTilt[hand], angleTilt, delay=0)


#thread for the osc server
def start_server(ip, port):
    global server
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    threading.Thread()



#-----------------------------------

def  scaleBetween(unscaledNum, minAllowed, maxAllowed, min, max):
    if unscaledNum < min:
        unscaledNum = min
    if unscaledNum >= max:
        unscaledNum = max

    return ((maxAllowed - minAllowed) * (unscaledNum - min) / (max - min)) + minAllowed

def angletopwn(andle):
#range from 1000 to 1500???
    sleep(1)
    return 0

def move( id, angle, delay ):

    pwm = scaleBetween(angle, 500, 2500, 0.0, 1.0)
    print("move: ", id, angle, delay, int(pwm))
    pi.set_servo_pulsewidth(id, int(pwm))
    if delay >= 0:
        sleep(delay)

def stop(id):
    pi.set_servo_pulsewidth(pinPan,0)
    pi.set_servo_pulsewidth(pinTilt,0)

pi = pigpio.pi()

dispatcher = Dispatcher()
dispatcher.map("/hand", filter_handler)
server = osc_server.ThreadingOSCUDPServer((ip, fromSensing), dispatcher)
print("Starting Server")
print("Serving on {}".format(server.server_address))

start_server(ip,fromSensing)

while (True):
    sleep(5)

server.shutdown()
p.terminate()
