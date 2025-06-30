#!/usr/bin/env python3
import time
from gpiozero import PWMOutputDevice as PWM

# Map names to BCM pins exactly as in your RGBLED class
test_pins = {

    "Left Red":    13,
    "Left Green":   19,
    "Left Blue":   0,
    "Right Red":    1,
    "Right Green":  5,
    "Right Blue":   6,
}

# Create a PWM device for each pin
devices = {name: PWM(pin=p, initial_value=1.0, frequency=2000)
           for name, p in test_pins.items()}

try:
    for name, dev in devices.items():
        print(f"\n--- Testing {name} (BCM {test_pins[name]}) ---")
        # Blink it three times:
        for i in range(3):
            dev.value = 0.0   # full-on (for common-anode wiring)
            time.sleep(0.3)
            dev.value = 1.0   # off
            time.sleep(0.3)
        input("Did that blink the correct LED?  Press Enter to continue…")
finally:
    # turn everything off at the end
    for dev in devices.values():
        dev.value = 1.0
    print("\nAll done. Pins reset to off.")
