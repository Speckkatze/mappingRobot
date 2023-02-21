# mappingRobot
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

  If you want to see the current progress of the map, host index.html on the pi in your local network. This is not required for it to work (you can just
  download the mapOfRoom.png file once the robot is finished), but its usefull nonetheless. I used NGINX for it, but you can use anything, really.
