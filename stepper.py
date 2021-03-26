import RPi.GPIO as GPIO # for stepper motor
import time
import requests # for webapi

import subprocess
# below imports or communication with ESP32
import serial
import sys
import socket




GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def move_one():
    for i in range(3):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.002)
    print("moving one")
    
ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
global connected
connected = False
while connected is False:
    try:
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        print(output)
        connected = True
        move_one()
    except subprocess.CalledProcessError:
        print("not connected")

UDP_IP = "172.20.10.4" # the IP that is printed in the serial moniter rom the ESP32
SHARED_UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet UDP
sock.connect((UDP_IP, SHARED_UDP_PORT))
    
def stepper_spin():
    global running
    # run for 30 seconds
    t_end = time.time() + 40
    while time.time() < t_end:  
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.002)
    GPIO.cleanup()
    running = "False"
    

if __name__ == "__main__":

    # get value of running and only start if this is true
    global running
    running = "False"
    while True:
        while running is "False":
            ready_to_run = requests.get('http://165.227.76.232:3000/prs2143/running')
            running = str(ready_to_run.json())
            print(running)
    
        sock.send('Hello ESP32'.encode())
        stepper_spin()
