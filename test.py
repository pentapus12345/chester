import move
import time

move.setup()
# Move forward at full speed for 1 second
move.move(50, 1, 5)
time.sleep(1)

# Stop
move.motorStop()

# Reverse at half speed for 1 second
move.move(50, -1, 0)
time.sleep(1)

# Stop again
move.motorStop()

