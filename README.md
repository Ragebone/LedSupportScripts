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




## LED Scripts for Dummies - A Step by Step Guide to use Colorchord with LEDs.
Lets begin with Colorchord. You should be able to use CNLohrs Version but We'd recommend to get our fork available at github.com/ragebone/colorchord
In the config, you can about configure it as you like except youll need a DisplayNetwork with either of the 3 default Outdrivers Prominent, Linear or Voronoi. For DisplayNetwork youll need the config values adress, port and leds. The leds value has to match the amount of leds you want to control with the AVR. The port has to match the socketport in the config.json and the adress has to match with the system youre running the scripts on. If youre using it all on the same PC, set it to 127.0.0.1.

Next to the config.json: set the leds to the amount youre using, the serial port, if you have more serial devices than one, and adjust the socketport to the value set in colochord config. Enable debug output if wanted. That should do it for now.

Adjust the AVR script to your needs.
The TOTALMAINSIZE has to be the sum of all main stripes, the TOTALCOMPLEMENTSIZE the sum of all complement stripes.
If you have 1 stripe conntected to 1 pin, set the TOTALMAINSIZE and MAINSTRIPE1SIZE to the amount and the MAINSTRIPE1PIN to the pin number and ignore the COMPLEMENT values.
Init a platformio project with your board, install the FastLED lib (126) and flash it to the AVR.

If done, run the Pipe.py and see your leds working with colorchord. If somethings not working add an issue here.

Enjoy!
