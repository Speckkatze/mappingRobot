# mappingRobot

IF YOU ARE ACTUALLY LOOKING FOR A ROBOT TO MAP YOUR ROOM, THIS IS NOT WHAT YOU ARE LOOKING FOR. THIS IS JUST A SCHOOL PROJECT AND PROOF OF CONCEPT, AND WHILE IT DOES WORK, IT DOES NOT WORK WELL ENOUGH TO ACTUALLY CREATE A MAP OF YOUR ROOM THATS USEFUL FOR ANYTHING. JUST USE A MEASURING TAPE.


Robot which drives arrount and creates a (somewhat) accurate map of your space. 


WHAT YOU NEED:
  
  - 1x Raspberry Pi 4b + microSD card
  - 1x Waveshare Stepper Motor HAT  (https://www.waveshare.com/wiki/Stepper_Motor_HAT)
  - 2x NEMA 17 Stepper Motor 1.5a 12v (shouldnt be bigger than 42x42x39mm, otherwise you wont be able to fit them)
  - 1x 5a12v DC PSU
  - 4x Arduino 6x6mm push button    (7 if you want some on the breadboard for debugging, recommended)
  - 3x ballpen spring 20mm
  - 4x 10koh resistor
  - 4x 100oh resistor
  - 8x m3 12mm screw
  - cables to connect pins with buttons
  - zipties
  - Breadboard (not strictly needed but makes it easier by requiring less soldering)
  - glue
  
  All STL files here:
  
  PLA recommended, chassis needs to be slightly flexible to fit motors
  
  
HOW TO USE:
  
  Once you built the robot, connect with the raspberry pi with ssh, download mapBotMain.py, run file from terminal. New .png file will get generated in the
  same directory once the robot stops (off button)
  
  Website is not needed, but is a nice addition too see current progress of map. Simply host index.html on the pi and access its ip in the local network. It
  should reload the page every five seconds.
