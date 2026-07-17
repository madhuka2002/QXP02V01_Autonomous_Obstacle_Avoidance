from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# --------------------------------------------------
# Configuration
# --------------------------------------------------

FORWARD_SPEED = 3.0
TURN_SPEED = 2.5

FRONT_THRESHOLD = 80
SIDE_THRESHOLD = 60

STOP_DURATION = 5
TURN_DURATION = 45

# --------------------------------------------------
# Motors
# --------------------------------------------------

leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

if leftMotor is None:
    raise RuntimeError('Device "left wheel motor" was not found.')

if rightMotor is None:
    raise RuntimeError('Device "right wheel motor" was not found.')

# Enable velocity control
leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# --------------------------------------------------
# Distance Sensors
# --------------------------------------------------

sensors = []

for i in range(8):
    sensor = robot.getDevice(f"ps{i}")

    if sensor is None:
        raise RuntimeError(f'Distance sensor "ps{i}" was not found.')

    sensor.enable(timestep)
    sensors.append(sensor)

print("Sensors initialized.")

# --------------------------------------------------
# Robot States
# --------------------------------------------------

FORWARD = 0
STOP = 1
ANALYZE = 2
TURN_LEFT = 3
TURN_RIGHT = 4

state = FORWARD
previousState = None
stateCounter = 0

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def set_motor_speeds(left_speed, right_speed):
    leftMotor.setVelocity(left_speed)
    rightMotor.setVelocity(right_speed)


def state_name(current_state):
    names = {
        FORWARD: "FORWARD",
        STOP: "STOP",
        ANALYZE: "ANALYZE",
        TURN_LEFT: "TURN_LEFT",
        TURN_RIGHT: "TURN_RIGHT"
    }

    return names.get(current_state, "UNKNOWN")


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

while robot.step(timestep) != -1:

    # Read sensor values
    values = [sensor.getValue() for sensor in sensors]

    frontLeft = values[7]
    frontRight = values[0]

    leftFront = values[6]
    leftRear = values[5]

    rightFront = values[1]
    rightRear = values[2]

    # Combine sensor readings
    frontValue = max(frontLeft, frontRight)

    leftValue = max(frontLeft, leftFront, leftRear)
    rightValue = max(frontRight, rightFront, rightRear)

    # Print state only when it changes
    if state != previousState:
        print(f"\nState changed to: {state_name(state)}")
        previousState = state

    # Optional sensor debugging
    print(
        f"\r"
        f"FL: {frontLeft:5.0f} | "
        f"FR: {frontRight:5.0f} | "
        f"LF: {leftFront:5.0f} | "
        f"RF: {rightFront:5.0f}",
        end=""
    )

    # --------------------------------------------------
    # FORWARD
    # --------------------------------------------------

    if state == FORWARD:

        # Slight steering corrections
        left_speed = FORWARD_SPEED
        right_speed = FORWARD_SPEED
    
        # Obstacle closer on the left
        if frontLeft > frontRight + 15:
            left_speed = FORWARD_SPEED
            right_speed = FORWARD_SPEED * 0.65
    
        # Obstacle closer on the right
        elif frontRight > frontLeft + 15:
            left_speed = FORWARD_SPEED * 0.65
            right_speed = FORWARD_SPEED
    
        set_motor_speeds(left_speed, right_speed)
    
        if frontValue > FRONT_THRESHOLD:
            print("\nObstacle detected.")
    
            set_motor_speeds(0.0, 0.0)
    
            state = STOP
            stateCounter = 0

    # --------------------------------------------------
    # STOP
    # --------------------------------------------------

    elif state == STOP:

        set_motor_speeds(0.0, 0.0)

        stateCounter += 1

        if stateCounter >= STOP_DURATION:
            state = ANALYZE
            stateCounter = 0

    # --------------------------------------------------
    # ANALYZE
    # --------------------------------------------------

    elif state == ANALYZE:

        set_motor_speeds(0.0, 0.0)

        print(
            f"\nAnalyzing space: "
            f"Left={leftValue:.0f}, "
            f"Right={rightValue:.0f}"
        )

        # Lower sensor value means more free space
        if leftValue < rightValue:
            print("More space on the left.")
            state = TURN_LEFT

        elif rightValue < leftValue:
            print("More space on the right.")
            state = TURN_RIGHT

        else:
            print("Both sides are similar. Turning left by default.")
            state = TURN_LEFT

        stateCounter = 0

    # --------------------------------------------------
    # TURN LEFT
    # --------------------------------------------------
    
    elif state == TURN_LEFT:
    
        set_motor_speeds(-TURN_SPEED, TURN_SPEED)
    
        stateCounter += 1
    
        # Finish turning when the front is clear
        # but require a minimum turning time first.
        if stateCounter >= 12 and frontValue < FRONT_THRESHOLD * 0.6:
            set_motor_speeds(0.0, 0.0)
    
            state = FORWARD
            stateCounter = 0
    
        # Safety fallback
        elif stateCounter >= TURN_DURATION:
            set_motor_speeds(0.0, 0.0)
    
            state = FORWARD
            stateCounter = 0
    
    
    # --------------------------------------------------
    # TURN RIGHT
    # --------------------------------------------------
    
    elif state == TURN_RIGHT:
    
        set_motor_speeds(TURN_SPEED, -TURN_SPEED)
    
        stateCounter += 1
    
        # Finish turning when the front is clear
        # but require a minimum turning time first.
        if stateCounter >= 12 and frontValue < FRONT_THRESHOLD * 0.6:
            set_motor_speeds(0.0, 0.0)
    
            state = FORWARD
            stateCounter = 0
    
        # Safety fallback
        elif stateCounter >= TURN_DURATION:
            set_motor_speeds(0.0, 0.0)
    
            state = FORWARD
            stateCounter = 0