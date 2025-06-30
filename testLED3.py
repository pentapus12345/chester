import time
from gpiozero import PWMOutputDevice as PWM

test_pins = {
    "Left-Red":    22,
    "Left-Green":   23,
    "Left-Blue":   24,
    "Right-Red":    1,
    "Right-Green":  5,
    "Right-Blue":   6,
}

devices = {name: PWM(pin, initial_value=1.0, frequency=2000)
           for name, pin in test_pins.items()}

try:
    for name, dev in devices.items():
        print(f"\n--- Testing {name} (BCM {test_pins[name]}) ---")
        for _ in range(3):
            dev.value = 0.0   # on (for common-anode)
            time.sleep(0.2)
            dev.value = 1.0   # off
            time.sleep(0.2)
        input("Was that the correct LED? Press Enter to continue…")
finally:
    for dev in devices.values():
        dev.value = 1.0
    print("Done.")