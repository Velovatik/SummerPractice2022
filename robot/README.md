### GPIO Output Example
This example allows you to check the functionality of the GPIO pins output.
Description of the example execution:
1. At the beginning of execution, in the console will be displayed a message : "Start GPIO_output test"
2. The BSP driver will be initialized, and GPIO pins will be configured with help by it.
3. Port "gpio0" will be opened
4. The initial state of all GPIO pins must correspond to logical zero (there is no voltage on the pin).
5. Further, all GPIO pins, except those specified in the exceptionPinArr array, will be configured to output.
6. Each pin, starting from GPIO0 (except specified in the exceptionPinArr array), will be sequentially transferred to the state of a logical "1" (voltage appears on the pin). Then state of this pin is changed to logical zero "0", and next pin switched to "1". Delay between pin switching is determined by the DELAY_S macro definition (the time is specified in seconds).
7. Enabling / disabling pins is performed from GPIO0 to GPIO27 and back to GPIO0.
8. If the example completes successfully, the following message will be displayed in the console: "Test finished."
If any errors occur during the execution of the example, a message about the error will be displayed in the console, the execution of the example will be stoped.
Code notation:
GPIO_PIN_NUM - number of GPIO pins on the board
DELAY_S - delay between changes in the state of adjacent pins in seconds
exceptionPinArr is an array of GPIO pin numbers that should be excluded from the example. This may be necessary if some of the pins are already used for other functions, for example, if the pins are used for UART connections during debugging.
For details please refer to the [documentation](https://click.kaspersky.com/?hl=en-us&customization=kcebeta&link=online_help&pid=kos&version=1.0).

### Prerequisites
Before you begin, ensure that you have met the following requirements:
- You have installed the latest version of [KasperskyOS Community Edition](https://os.kaspersky.com/development/download/)
- You have Debian GNU/Linux "Buster" 10.7 x64

### Usage
To build the example and run the resulting image please refer to the documentation.

© 2021 AO Kaspersky Lab
