# Carousel for Covid Times

# Description
This project mimics a carousel motion by spinning and moving animals up and down. It also runs  Arduino script from the ESP32 with a wireless connection, as well as a python script on raspberry pi. All code can be viewed in this Github repo.

# Dependencies
This project requires the Arduino IDE to run. You can download it here: https://www.arduino.cc/en/software
Make sure to select the correct download based on your machine (I used a MacBook Pro).

# Physical Setup

This project uses two motors: a stepper motor and a servo motor. The stepper motor is connected to and controlled by a Raspberry Pi 4. This motor begins spinning when the pi received the signal from the web API. Once this happens, the pi sends a signal over wifi to the ESP32 (powered by a 9V battery), telling it to begin. The ESP32 waits 5 seconds before starting the servo to toggle the cranes up and down. 

To connect the stepper motor to the Raspberry Pi, first, connect the stepper motor to the stepper motor driver. Then, plug an F-F wire from In1 on the stepper motor driver to GPIO 7 on the pi. Connect the following pins using 3 more F-F wires: In2 on the driver to GPIO11 on the pi; In3 on the driver to GPIO13 on the pi; In4 on the driver to GPIO15 on the pi. Then, plug the 12V (power) port on the driver into 5V on the Pi (GPIO 4) and the 5- port to GND (GPIO 6). 

To set up the servo motor, Connected the servo motor to the ESP32 by plugging the two end pins into the ground and 5V power. A third wire is used to connect the middle pin to ESP32 pin 15.

The Arduino sketch was uploaded from my laptop to the ESP32. Once uploaded, I unplugged the ESP32 from my laptop and powered it with a 9V battery.

The ESP32 is connected to wifi via station mode. To run the project, I connected both the ESP32 and the raspberry pu to a mobile hotspot set up on an iPhone. Change the "GUEST" wifi and corresponding "guest_pw" to the wifi network and password that you will connect to. Both the ESP32 and pi must be connected to the same network to send messages.
