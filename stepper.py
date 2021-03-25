import RPi.GPIO as GPIO # for stepper motor
import time
import requests # for webapi

# below imports or communication with ESP32
import serial
import sys
import socket

UDP_IP = "172.20.10.4" # the IP that is printed in the serial moniter rom the ESP32
SHARED_UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet UDP
sock.connect((UDP_IP, SHARED_UDP_PORT))

def get_running():
    running = requests.get('http://165.227.76.232:3000/prs2143/running')
    return running

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

def stepper_spin():
    # run for 30 seconds
    t_end = time.time() + 30
    while time.time() < t_end:  
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.002)
    GPIO.cleanup()

if __name__ == "__main__":
    print("starting")
    # get value of running and only start i this is true
    running = False
    while not running:
        running = get_running()
        print(running.json())
    
    sock.send('Hello ESP32'.encode())
    while running:
        stepper_spin()
