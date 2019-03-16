# LED Support Scripts
____________________
These are some scripts written in ___Python3___ for Colorchord2 and AVRs programmable with platformio (like Arduinos).
Libraries needed for platformio: FastLED, to install: platformio lib (-g if wanted globally) install 126

#### config.json
---
sets some variables for all other scripts
###### config
1. leds*: the amount of leds adressed by the AVR
2. socketport*: the UDP Socket Port to listen on for colorchord
3. port: Serial port to the AVR, e.g "COM5" in Windows, e.g. "/dev/ttyACM0" on Linux  
Uses the first available Serial port if not set.
4. counterSize: The amount of bytes used in the Run Length Encoding for the counter. Default: 2.  
If you have less than 256 leds, you can decrease it to 1, if you have more than 65536 leds, you have to increase it to 3.  
___Has to match the AVR script___
5. maxBrightness: rescale the sent data from 0 to 255 to a lower range.
###### debug
1. printComplement*: print the complement color to set int manually in other solutions like Aura or iCUE.
2. printInDataRate*: print the incoming Datarate.
3. printOutDataRate*: print the sending Datarate.
4. printInData*: print the bytestream received.
5. printOutData: print the bytestream sent.

_\* not used by all scripts_

#### Pipe
---
reads data from socketport, compresses the Data with a Run Length Encoding and sends the compressed Data to the serial port.

#### setRGB
---
asks for user input to create a static color distribution.
Ignores config: socketport, printInDataRate, printOutDataRate, printInData

#### Utility
---
Collection of functions used by all scripts. Prints the available serial ports if run.






