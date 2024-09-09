def adc_read_pin_value(pin: int) -> int:
    '''
    Read the raw value from the ADC channel.

    :param pin: The pin to read (e.g. :const:`GPIO_PIN_PC1`).
    :returns: The raw value between 0 and 4095.
    
    .. versionadded:: 1.3.0

    .. hint::

        Don't forget to initialize the pin first.
    '''
    pass

def adc_read_pin_voltage(pin: int) -> float:
    '''
    Read the voltage from the ADC channel.

    :param pin: The pin to read (e.g. :const:`GPIO_PIN_PC1`).
    :returns: The voltage between 0 - 2.048 V with a precision of ~0.1%.
    
    .. versionadded:: 1.3.0

    .. hint::

        Don't forget to initialize the pin first.
    '''
    pass
def canvas_update() -> None:
    '''
    Updates the display buffer with your drawings from the canvas.

    .. versionadded:: 1.0.0

    .. note::

        Your drawings will only appear on the display after this function call.
    '''
    pass

def canvas_clear() -> None:
    '''
    Clear the whole canvas. This does not affect the current display buffer.
    You need to call :func:`canvas_update` to reveal your changes.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_width() -> int:
    '''
    Get the canvas width in pixels.

    .. versionadded:: 1.0.0

    :returns: The canvas width.
    '''
    pass

def canvas_height() -> int:
    '''
    Get the canvas height in pixels.

    .. versionadded:: 1.0.0

    :returns: The canvas height.
    '''
    pass

COLOR_BLACK: int
'''
Constant value for the color `black`.

.. versionadded:: 1.0.0
'''

COLOR_WHITE: int
'''
Constant value for the color `white`.

.. versionadded:: 1.0.0
'''

def canvas_set_color(color: int) -> None:
    '''
    Set the color to use when drawing or writing on the canvas.

    .. versionadded:: 1.0.0

    :param color: The color to use.
    '''
    pass

ALIGN_BEGIN: int
'''
Align element at `begin` (horizontal or vertical, depends on the context).

.. versionadded:: 1.0.0
'''

ALIGN_END: int
'''
Align element at `end` (horizontal or vertical, depends on the context).

.. versionadded:: 1.0.0
'''

ALIGN_CENTER: int
'''
Align element at `center` (horizontal or vertical, depends on the context).

.. versionadded:: 1.0.0
'''

def canvas_set_text_align(x: int, y: int) -> None:
    '''
    Define how the text should be aligned in relation to the ``x`` and ``y`` coordinates 
    when writing on the canvas, using the :func:`canvas_set_text` function.

    :param x: The horizontal alignment.
    :param y: The vertical alignment.

    .. versionadded:: 1.0.0
    '''
    pass

FONT_PRIMARY: int
'''
Constant value for the primary font.

.. versionadded:: 1.0.0
'''

FONT_SECONDARY: int
'''
Constant value for the secondary font.

.. versionadded:: 1.0.0
'''

def canvas_set_font(font: int) -> None:
    '''
    Change the font to use when writing on the canvas using the :func:`canvas_set_text` function.

    :param font: The font to use.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_set_text(x: int, y: int, text: str) -> None:
    '''
    Write text on the canvas at the position of ``x`` and ``y`` by using the currently active color, font and alignment settings.
    
    :param x: The horizontal position.
    :param y: The vertical position.
    :param text: The text to write.

    .. versionadded:: 1.0.0
    
    .. code-block::

        import flipperzero as f0

        f0.canvas_set_color(f0.COLOR_BLACK)
        f0.canvas_set_text_align(f0.ALIGN_CENTER, f0.ALIGN_BEGIN)
        f0.canvas_set_text(64, 32, 'Hello World!')
        f0.canvas_update()

    .. seealso::

        * :func:`canvas_set_color` to change the canvas color.
        * :func:`canvas_set_text_align` to change the alignment settings.
        * :func:`canvas_set_font` to change the current font.
    '''
    pass

def canvas_draw_dot(x: int, y: int) -> None:
    '''
    Draw a dot on the canvas by using the currently active color settings.

    :param x: The horizontal position.
    :param y: The vertical position.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_draw_box(x: int, y: int, w: int, h: int, r: int) -> None:
    '''
    Draw a box on the canvas. The fill color is defined by the currently active color settings.
    Set the corner radius to zero to draw a rectangle without rounded corners.

    :param x: The horizontal position.
    :param y: The vertical position.
    :param w: The width of the box.
    :param h: The height of the box.
    :param r: The corner radius to use.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_draw_frame(x: int, y: int, w: int, h: int, r: int) -> None:
    '''
    Draw a frame on the canvas. The border color is defined by the currently active color settings.
    Set the corner radius to zero to draw a rectangle without rounded corners.

    :param x: The horizontal position.
    :param y: The vertical position.
    :param w: The width of the box.
    :param h: The height of the box.
    :param r: The corner radius to use.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_draw_line(x0: int, y0: int, x1: int, y1: int) -> None:
    '''
    Draw a line on the canvas. The color is defined by the currently active color settings.

    :param x0: The horizontal start position.
    :param y0: The vertical start position.
    :param x1: The horizontal end position.
    :param y1: The vertical end sposition.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_draw_circle(x: int, y: int, r: int) -> None:
    '''
    Draw a circle on the canvas. The border color is defined by the currently active color settings.

    :param x: The horizontal position.
    :param y: The vertical position.
    :param r: The radius to use.

    .. versionadded:: 1.0.0
    '''
    pass

def canvas_draw_disc(x: int, y: int, r: int) -> None:
    '''
    Draw a disc on the canvas. The fill color is defined by the currently active color settings.

    :param x: The horizontal position.
    :param y: The vertical position.
    :param r: The radius to use.

    .. versionadded:: 1.0.0
    '''
    pass
def dialog_message_set_header(text: str, x: int, y: int, h: int, v: int) -> None:
    '''
    Set a header text on the dialog box.

    :param text: The text to set.
    :param x: The x coordinates to use.
    :param y: The y coordinates to use.
    :param h: The horizontal alignment.
    :param v: The vertical alignment.

    .. versionadded:: 1.0.0
    '''
    pass

def dialog_message_set_text(text: str, x: int, y: int, h: int, v: int) -> None:
    '''
    Set a text on the dialog box.

    :param text: The text to set.
    :param x: The x coordinates to use.
    :param y: The y coordinates to use.
    :param h: The horizontal alignment.
    :param v: The vertical alignment.

    .. versionadded:: 1.0.0
    '''
    pass

def dialog_message_set_button(text: str, button: int) -> None:
    '''
    Set the text of a dialog box button.

    :param text: The text to set.
    :param button: The button to use (e.g. :const:`INPUT_BUTTON_UP`).

    .. versionadded:: 1.0.0
    '''
    pass

def dialog_message_show() -> int:
    '''
    Display the dialog box with the configured settings.
    This function is blocking.

    :returns: The button code, used to close the dialog (e.g. :const:`INPUT_BUTTON_OK`)

    .. versionadded:: 1.0.0

    .. code-block::

        import flipperzero as f0

        f0.dialog_message_set_header('Important',64, 12)
        f0.dialog_message_set_text('It this awesome?', 64, 24)
        f0.dialog_message_set_button('Yes', f0.INPUT_BUTTON_LEFT)
        f0.dialog_message_set_button('No', f0.INPUT_BUTTON_RIGHT)

        while f0.dialog_message_show() is not f0.INPUT_BUTTON_LEFT:
            pass
    '''
    pass
from typing import Callable

GPIO_PIN_PC0: int
'''
Constant identifier for GPIO pin PC0.

* This pin can be used as ADC input.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PC1: int
'''
Constant identifier for GPIO pin PC1.

* This pin can be used as ADC input.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PC3: int
'''
Constant identifier for GPIO pin PC3.

* This pin can be used as ADC input.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PB2: int
'''
Constant identifier for GPIO pin PB2.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PB3: int
'''
Constant identifier for GPIO pin PB3.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PA4: int
'''
Constant identifier for GPIO pin PA4.

* This pin can be used as ADC input.
* This pin can be used as PWM output.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PA6: int
'''
Constant identifier for GPIO pin PA6.

* This pin can be used as ADC input.
    
.. versionadded:: 1.2.0
'''

GPIO_PIN_PA7: int
'''
Constant identifier for GPIO pin PA7.

* This pin can be used as ADC input.
* This pin can be used as PWM output.
* This pin can be used to transmit an infrared signal with an IR LED.

    
.. versionadded:: 1.2.0
'''

GPIO_MODE_INPUT: int
'''
Constant configuration value for the GPIO input mode.
    
.. versionadded:: 1.2.0
'''

GPIO_MODE_OUTPUT_PUSH_PULL: int
'''
Constant configuration value for the GPIO output as push-pull mode.
    
.. versionadded:: 1.2.0
'''

GPIO_MODE_OUTPUT_OPEN_DRAIN: int
'''
Constant configuration value for the GPIO output as open-drain mode.
    
.. versionadded:: 1.2.0
'''

GPIO_MODE_ANALOG: int
'''
Constant configuration value for the GPIO analog mode.
    
.. versionadded:: 1.2.0
'''

GPIO_MODE_INTERRUPT_RISE: int
'''
Constant configuration value for the GPIO interrupt on rising edges mode.
    
.. versionadded:: 1.2.0
'''

GPIO_MODE_INTERRUPT_FALL: int
'''
Constant configuration value for the GPIO interrupt on falling edges mode.
    
.. versionadded:: 1.2.0
'''

GPIO_PULL_NO: int
'''
Constant configuration value for the GPIO internal pull resistor disabled.
    
.. versionadded:: 1.2.0
'''

GPIO_PULL_UP: int
'''
Constant configuration value for the GPIO internal pull-up resistor enabled.
    
.. versionadded:: 1.2.0
'''

GPIO_PULL_DOWN: int
'''
Constant configuration value for the GPIO internal pull-down resistor enabled.
    
.. versionadded:: 1.2.0
'''

GPIO_SPEED_LOW: int
'''
Constant configuration value for the GPIO in low speed.
    
.. versionadded:: 1.2.0
'''

GPIO_SPEED_MEDIUM: int
'''
Constant configuration value for the GPIO in medium speed.
    
.. versionadded:: 1.2.0
'''

GPIO_SPEED_HIGH: int
'''
Constant configuration value for the GPIO in high speed.
    
.. versionadded:: 1.2.0
'''

GPIO_SPEED_VERY_HIGH: int
'''
Constant configuration value for the GPIO in very high speed.
    
.. versionadded:: 1.2.0
'''

def gpio_init_pin(pin: int, mode: int, pull: int = None, speed: int = None) -> bool:
    '''
    Initialize a GPIO pin.

    :param pin: The pin to initialize (e.g. :const:`GPIO_PIN_PA4`).
    :param mode: The mode to use (e.g. :const:`GPIO_MODE_INPUT`).
    :param pull: The pull resistor to use. Default is :const:`GPIO_PULL_NO`.
    :param speed: The speed to use. Default is :const:`GPIO_SPEED_LOW`.
    :returns: :const:`True` on success, :const:`False` otherwise.
    
    .. versionadded:: 1.2.0
    .. versionchanged:: 1.3.0
       The return value changed from ``None`` to ``bool``.

    .. hint::

        The interrupt modes :const:`GPIO_MODE_INTERRUPT_RISE` and :const:`GPIO_MODE_INTERRUPT_FALL` can be combined using bitwise OR.
        This allows you to handle rising `and` falling edges.
    '''
    pass

def gpio_deinit_pin(pin: int) -> None:
    '''
    Deinitialize a GPIO pin.

    :param pin: The pin to deinitialize (e.g. :const:`GPIO_PIN_PA4`).
    
    .. versionadded:: 1.3.0

    .. note::

        It's not strictly necessary to deinitialize your GPIO pins upon script termination, this is already covered by the interpreter.
    '''
    pass

def gpio_set_pin(pin: int, state: bool) -> None:
    '''
    Set the state of an output pin.

    :param pin: The pin to set (e.g. :const:`GPIO_PIN_PA4`).
    :param state: The state to set.
    
    .. versionadded:: 1.2.0

    .. hint::

        Don't forget to initialize the pin first.
    '''
    pass

def gpio_get_pin(pin: int) -> bool:
    '''
    Read the state of an input pin.

    :param pin: The pin to read (e.g. :const:`GPIO_PIN_PA4`).
    :returns: :const:`True` if the pin is high, :const:`False` on a low signal.
    
    .. versionadded:: 1.2.0

    .. hint::

        Don't forget to initialize the pin first.
    '''
    pass

def on_gpio() -> Callable[[int], None]:
    '''
    Decorate a function to be used as GPIO interrupt handler. The decorated function will be invoked upon a GPIO interrupt.

    .. versionadded:: 1.0.0

    .. code-block::

        import flipperzero as f0

        f0.gpio_init_pin(f0.GPIO_PIN_PC0, f0.GPIO_MODE_INTERRUPT_RISE, f0.GPIO_PULL_UP)

        @f0.on_gpio
        def interrupt_handler(pin):
            if pin == f0.GPIO_PIN_PC0:
                ...
    
    .. warning::

        You can only decorate one function per application.
    '''
    pass
from typing import List

def infrared_receive(timeout: int = 1000000) -> List[int]:
    '''
    Receive an infrared signal. This is a blocking method.
    The method blocks until a timeout occurs or the internal
    signal buffer (capacity is 1024 timings) is filled.

    :param timeout: The timeout to use in microseconds.
    :returns: A list of timings in microseconds, starting with high.
    
    .. versionadded:: 1.3.0
    '''
    pass

def infrared_transmit(signal: List[int], repeat: int = 1, use_external_pin: bool = False, frequency: int = 38000, duty: float = 0.33) -> bool:
    '''
    Transmit an infrared signal. This is a blocking method.
    The method blocks until the whole signal is sent.
    The signal list has the same format as the return value 
    of :func:`infrared_receive`. Hence you can directly re-send
    a received signal without any further processing.

    :param signal: The signal to use.
    :param repeat: How many times the signal should be sent.
    :param use_external_pin: :const:`True` to use an external IR LED on GPIO pin :const:`flipperzero.GPIO_PIN_PA7`.
    :param frequency: The frequency to use for the PWM signal.
    :param duty: The duty cycle to use for the PWM signal.
    :returns: :const:`True` on success, :const:`False` otherwise.
    
    .. versionadded:: 1.3.0
    '''
    pass

def infrared_is_busy() -> bool:
    '''
    Check if the infrared subsystem is busy.

    :returns: :const:`True` if occupied, :const:`False` otherwise.
    
    .. versionadded:: 1.3.0
    '''
    pass
from typing import Callable

INPUT_BUTTON_UP: int
'''
Constant value for the `up` button.

.. versionadded:: 1.0.0
'''

INPUT_BUTTON_DOWN: int
'''
Constant value for the `down` button.

.. versionadded:: 1.0.0
'''

INPUT_BUTTON_RIGHT: int
'''
Constant value for the `right` button.

.. versionadded:: 1.0.0
'''

INPUT_BUTTON_LEFT: int
'''
Constant value for the `left` button.

.. versionadded:: 1.0.0
'''

INPUT_BUTTON_OK: int
'''
Constant value for the `ok` button.

.. versionadded:: 1.0.0
'''

INPUT_BUTTON_BACK: int
'''
Constant value for the `back` button.

.. versionadded:: 1.0.0
'''

INPUT_TYPE_PRESS: int
'''
Constant value for the `press` event of a button.

.. versionadded:: 1.0.0
'''

INPUT_TYPE_RELEASE: int
'''
Constant value for the `release` event of a button.

.. versionadded:: 1.0.0
'''

INPUT_TYPE_SHORT: int
'''
Constant value for the `short` press event of a button.

.. versionadded:: 1.0.0
'''

INPUT_TYPE_LONG: int
'''
Constant value for the `long` press event of a button.

.. versionadded:: 1.0.0
'''

INPUT_TYPE_REPEAT: int
'''
Constant value for the `repeat` press event of a button.

.. versionadded:: 1.0.0
'''

def on_input() -> Callable[[int, int], None]:
    '''
    Decorate a function to be used as input handler. The decorated function will be invoked upon interaction with one of the buttons on the Flipper.

    .. versionadded:: 1.0.0

    .. code-block::

        import flipperzero as f0

        @f0.on_input
        def input_handler(button, type):
            if button == f0.INPUT_BUTTON_BACK:
                if type == f0.INPUT_TYPE_LONG:
                    ...
    
    .. warning::

        You can only decorate one function per application.
    '''
    pass
from typing import Callable

LIGHT_RED: int
'''
Constant value for the red LED light.

.. versionadded:: 1.0.0
'''

LIGHT_GREEN: int
'''
Constant value for the green LED light.

.. versionadded:: 1.0.0
'''

LIGHT_BLUE: int
'''
Constant value for the blue LED light.

.. versionadded:: 1.0.0
'''

LIGHT_BACKLIGHT: int
'''
Constant value for the display backlight.

.. versionadded:: 1.0.0
'''

def light_set(light: int, brightness: int) -> None:
    '''
    Control the RGB LED on your Flipper. You can also set the brightness of multiple channels at once using bitwise operations.
    The ``brightness`` parameter accepts values from 0 (light off) to 255 (very bright).

    :param light: The RGB channels to set.
    :param brightness: The brightness to use.

    .. versionadded:: 1.0.0

    .. code-block::
    
        import flipperzero as f0
        
        f0.light_set(f0.LIGHT_RED | f0.LIGHT_GREEN, 250)

    .. tip::

        You can use  up to seven colors using `additive mixing <https://en.wikipedia.org/wiki/Additive_color>`_.
    '''
    pass

def light_blink_start(light: int, brightness: int, on_time: int, period: int) -> None:
    '''
    Let the RGB LED blink. You can define the total duration of a blink period and the duration, the LED is active during a blink period.
    Hence, ``on_time`` must be smaller than ``period``. This is a non-blocking operation. The LED will continue to blink until you call :func:`light_blink_stop`.

    :param light: The RGB channels to set.
    :param brightness: The brightness to use.
    :param on_time: The LED's active duration in milliseconds.
    :param period: Total duration of a blink period in milliseconds.

    .. versionadded:: 1.0.0

    .. code-block::
    
        import flipperzero as f0
        
        f0.light_blink_start(f0.LIGHT_RED, 150, 100, 200)
    '''
    pass

def light_blink_set_color(light: int) -> None:
    '''
    Change the RGB LED's color while blinking. This is a non-blocking operation.
    Be aware, that you must start the blinking procedure first by using the :func:`light_blink_start` function.
    Call the :func:`light_blink_stop` function to stop the blinking LED.

    :param light: The RGB channels to set.

    .. versionadded:: 1.0.0
    '''
    pass

def light_blink_stop() -> None:
    '''
    Stop the blinking LED.

    .. versionadded:: 1.0.0
    '''
    pass
def pwm_start(pin: int, frequency: int, duty: int) -> bool:
    '''
    Start or change the PWM signal on the corresponding GPIO pin.

    :param pin: The pin to read (e.g. :const:`GPIO_PIN_PA7`).
    :param frequency: The frequency to set in Hz.
    :param duty: The duty cycle per period in percent.
    :returns: :const:`True` on success, :const:`False` otherwise.
    
    .. versionadded:: 1.3.0

    .. warning::

        You don't have to initialize the pin first.
    '''
    pass

def pwm_stop(pin: int) -> None:
    '''
    Stop the PWM signal on the corresponding GPIO pin.

    :param pin: The pin to use (e.g. :const:`GPIO_PIN_PA7`).
    
    .. versionadded:: 1.3.0
    '''
    pass

def pwm_is_running(pin: int) -> bool:
    '''
    Check if the corresponding GPIO pin has a PWM signal output.

    :param pin: The pin to check (e.g. :const:`GPIO_PIN_PA7`).
    :returns: :const:`True` on success, :const:`False` otherwise.
    
    .. versionadded:: 1.3.0
    '''
    pass
'''
Python script for notes generation

# coding: utf-8
# Python script for notes generation

from typing import List

note_names: List = ['C', 'CS', 'D', 'DS', 'E', 'F', 'FS', 'G', 'GS', 'A', 'AS', 'B']

for octave in range(9):
    for name in note_names:
        print("SPEAKER_NOTE_%s%s: float" % (name, octave))
        print('\'\'\'')
        print('The musical note %s\\ :sub:`0` as frequency in `Hz`.\n' % (name if len(name) == 1 else (name[0]+'#')))
        print('.. versionadded:: 1.2.0')
        print('\'\'\'\n')
'''

SPEAKER_NOTE_C0: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS0: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D0: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS0: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E0: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F0: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS0: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G0: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS0: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A0: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS0: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B0: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C1: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS1: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D1: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS1: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E1: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F1: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS1: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G1: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS1: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A1: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS1: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B1: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C2: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS2: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D2: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS2: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E2: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F2: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS2: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G2: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS2: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A2: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS2: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B2: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C3: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS3: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D3: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS3: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E3: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F3: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS3: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G3: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS3: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A3: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS3: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B3: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C4: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS4: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D4: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS4: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E4: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F4: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS4: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G4: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS4: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A4: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS4: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B4: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C5: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS5: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D5: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS5: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E5: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F5: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS5: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G5: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS5: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A5: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS5: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B5: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C6: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS6: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D6: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS6: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E6: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F6: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS6: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G6: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS6: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A6: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS6: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B6: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C7: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS7: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D7: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS7: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E7: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F7: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS7: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G7: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS7: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A7: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS7: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B7: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_C8: float
'''
The musical note C\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_CS8: float
'''
The musical note C#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_D8: float
'''
The musical note D\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_DS8: float
'''
The musical note D#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_E8: float
'''
The musical note E\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_F8: float
'''
The musical note F\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_FS8: float
'''
The musical note F#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_G8: float
'''
The musical note G\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_GS8: float
'''
The musical note G#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_A8: float
'''
The musical note A\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_AS8: float
'''
The musical note A#\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_NOTE_B8: float
'''
The musical note B\ :sub:`0` as frequency in `Hz`.

.. versionadded:: 1.2.0
'''

SPEAKER_VOLUME_MIN: float
'''
The minimal volume value.

.. versionadded:: 1.2.0
'''

SPEAKER_VOLUME_MAX: float
'''
The maximum volume value.

.. versionadded:: 1.2.0
'''

def speaker_start(frequency: float, volume: float) -> bool:
    '''
    Output a steady tone of a defined frequency and volume on the Flipper's speaker.
    This is a non-blocking operation. The tone will continue until you call :func:`speaker_stop`.
    The ``volume`` parameter accepts values from :py:const:`SPEAKER_VOLUME_MIN` (silent) up to :py:const:`SPEAKER_VOLUME_MAX` (very loud).

    :param frequency: The frequency to play in `Hz <https://en.wikipedia.org/wiki/Hertz>`_.
    :param volume: The volume to use.
    :returns: :const:`True` if the speaker was acquired.

    .. versionadded:: 1.0.0

    .. code-block::
        
        import flipperzero as f0
        
        f0.speaker_start(50.0, 0.8)
    '''
    pass

def speaker_set_volume(volume: float) -> bool:
    '''
    Set the speaker's volume while playing a tone. This is a non-blocking operation.
    The tone will continue until you call :func:`speaker_stop`.
    The ``volume`` parameter accepts values from 0.0 (silent) up to 1.0 (very loud).
    
    :param volume: The volume to use.
    :returns: :const:`True` if the speaker was acquired.

    .. versionadded:: 1.0.0

    This function can be used to play `nice` sounds:

    .. code-block::

        import time
        import flipperzero as f0
        
        volume = 0.8

        f0.speaker_start(100.0, volume)

        for _ in range(0, 150):
            volume *= 0.9945679

            f0.speaker_set_volume(volume)

            time.sleep_ms(1)
        
        f0.speaker_stop()
    '''
    pass

def speaker_stop() -> bool:
    '''
    Stop the speaker output.

    :returns: :const:`True` if the speaker was successfully released.

    .. versionadded:: 1.0.0
    '''
    pass
def vibro_set(state: bool) -> bool:
    '''
    Turn vibration on or off. This is a non-blocking operation. The vibration motor will continue to run until you stop it.

    :param state: :const:`True` to turn on vibration.
    :returns: :const:`True` if vibration is on.

    .. versionadded:: 1.0.0
    '''
    pass
