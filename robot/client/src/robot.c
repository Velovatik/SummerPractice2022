#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <gpio/gpio.h>
#include <stdbool.h>

#ifdef __arm__
#include <bsp/bsp.h>
#endif

#define GPIO_PIN_NUM 28U
#define DELAY_S 2

/**
 * exceptionPinArr is an array of GPIO pin numbers that should be excluded
 * from the example. This may be necessary if some of the pins are already
 * used for other functions, for example, if the pins are used for UART
 * connections during debugging.
 */
const int exceptionPinArr[] = {14, 15};
GpioHandle handle = NULL;
static bool IsExceptionPin(int pin)
{
    bool ret = false;

    for(int i = 0; i < sizeof(exceptionPinArr) / sizeof(int); i++)
    {
        if(exceptionPinArr[i] == pin)
        {
            ret = true;

            break;
        }
    }

    return ret;
}

void init(){
	GpioSetMode(handle, 6, GPIO_DIR_OUT); //Pins for turning the engines on
   	GpioSetMode(handle, 26, GPIO_DIR_OUT); //6 and 26

   	GpioSetMode(handle, 12, GPIO_DIR_OUT);
   	GpioSetMode(handle, 13, GPIO_DIR_OUT);
   	GpioSetMode(handle, 20, GPIO_DIR_OUT);
   	GpioSetMode(handle, 21, GPIO_DIR_OUT);

   	GpioOut(handle, 6, 1); //Turn pins P6 and P26 on
   	GpioOut(handle, 26, 1); //for switching both engines on
}

void stop(){
    GpioOut(handle, 12, 0); //Robot will stop
    GpioOut(handle, 13, 0);
    GpioOut(handle, 20, 0);
    GpioOut(handle, 21, 0);
}


void forward(int delay){
    GpioOut(handle, 12, 1); //Motors co-rotating in this case
    GpioOut(handle, 13, 0);
    GpioOut(handle, 20, 0);
    GpioOut(handle, 21, 1);
    sleep(delay);
    stop();
}

void backward(int delay){
    GpioOut(handle, 12, 0); //Robot will move back
    GpioOut(handle, 13, 1);
    GpioOut(handle, 20, 1);
    GpioOut(handle, 21, 0);
    sleep(delay);
    stop();
}

void left(int delay){
    GpioOut(handle, 12, 0); //Robot will turn left
    GpioOut(handle, 13, 0);
    GpioOut(handle, 20, 0);
    GpioOut(handle, 21, 1);
    sleep(delay);
    stop();
}

void right(int delay){
    GpioOut(handle, 12, 1); //Robot will turn right
    GpioOut(handle, 13, 0);
    GpioOut(handle, 20, 0);
    GpioOut(handle, 21, 0);
    sleep(delay);
    stop();
}

int main(int argc, const char *argv[])
{
    fprintf(stderr, "Start GPIO_output test\n");

#ifdef __arm__
    /**
     * Initialize board support package (BSP) driver and set configuration
     * for GPIO pins. It`s required for stdout by UART.
     */
    {
        BspError rc = BspInit(NULL);
        if (rc != BSP_EOK)
        {
            fprintf(stderr, "Failed to initialize BSP\n");
            return EXIT_FAILURE;
        }

        rc = BspSetConfig("gpio0", "raspberry_pi4b.default");
        if (rc != BSP_EOK)
        {
            fprintf(stderr, "Failed to set mux configuration for gpio0 module\n");
            return EXIT_FAILURE;
        }
    }
#endif

    if (GpioInit())
    {
        fprintf(stderr, "GpioInit failed\n");
        return EXIT_FAILURE;
    }

    /* initialize and setup gpio0 port */
    handle = NULL;
    GpioOpenPort("gpio0", &handle);

    init();
    forward(3);
    left(1);
    right(1);
    backward(3);

    return EXIT_SUCCESS;
}
