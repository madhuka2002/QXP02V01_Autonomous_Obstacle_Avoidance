from controller import Robot


# ============================================================
# QXP02V01 — Autonomous Obstacle Avoidance Robot
# Quantheonix Robotics Research Project
# ============================================================

robot = Robot()
timeStep = int(robot.getBasicTimeStep())


# ============================================================
# Configuration
# ============================================================

maxSpeed = 6.28

forwardSpeed = 3.0
slowSpeed = 1.8
turnSpeed = 2.7
reverseSpeed = 2.0

frontThreshold = 80.0
clearThreshold = 45.0
steeringDifference = 15.0

stopDuration = 0.20
minimumTurnDuration = 0.30
maximumTurnDuration = 1.50
reverseDuration = 0.80
recoveryTurnDuration = 1.30

stuckTimeWindow = 3.0
maximumRepeatedObstacles = 3

statisticsInterval = 5.0


# ============================================================
# Robot States
# ============================================================

FORWARD = 0
STOP = 1
ANALYZE = 2
TURN_LEFT = 3
TURN_RIGHT = 4
BACKWARD = 5
RECOVERY_TURN = 6


stateNames = {
    FORWARD: "FORWARD",
    STOP: "STOP",
    ANALYZE: "ANALYZE",
    TURN_LEFT: "TURN_LEFT",
    TURN_RIGHT: "TURN_RIGHT",
    BACKWARD: "BACKWARD",
    RECOVERY_TURN: "RECOVERY_TURN"
}


# ============================================================
# Motor Initialization
# ============================================================

leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

if leftMotor is None:
    raise RuntimeError('Device "left wheel motor" was not found.')

if rightMotor is None:
    raise RuntimeError('Device "right wheel motor" was not found.')

leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


# ============================================================
# Distance Sensor Initialization
# ============================================================

sensors = []

for sensorIndex in range(8):
    sensorName = f"ps{sensorIndex}"
    sensor = robot.getDevice(sensorName)

    if sensor is None:
        raise RuntimeError(f'Distance sensor "{sensorName}" was not found.')

    sensor.enable(timeStep)
    sensors.append(sensor)


# ============================================================
# Controller Variables
# ============================================================

currentState = FORWARD
previousState = None
stateStartTime = robot.getTime()

lastTurnDirection = TURN_RIGHT
recoveryTurnDirection = TURN_LEFT

lastObstacleTime = -100.0
repeatedObstacleCount = 0

obstacleCount = 0
leftTurnCount = 0
rightTurnCount = 0
recoveryCount = 0

lastStatisticsTime = robot.getTime()


# ============================================================
# Helper Functions
# ============================================================

def clampSpeed(speed):
    """Keep motor speed inside the e-puck motor limits."""
    return max(-maxSpeed, min(maxSpeed, speed))


def setMotorSpeeds(leftSpeed, rightSpeed):
    """Apply velocity values to both wheel motors."""
    leftMotor.setVelocity(clampSpeed(leftSpeed))
    rightMotor.setVelocity(clampSpeed(rightSpeed))


def changeState(newState):
    """Change the FSM state and reset the state timer."""
    global currentState
    global stateStartTime

    currentState = newState
    stateStartTime = robot.getTime()


def getStateElapsedTime():
    """Return the time spent in the current state."""
    return robot.getTime() - stateStartTime


def printStateChange():
    """Print state only when it changes."""
    global previousState

    if currentState != previousState:
        print(f"\nState: {stateNames[currentState]}")
        previousState = currentState


def printStatistics():
    """Display navigation statistics periodically."""
    runtime = robot.getTime()

    print("\n")
    print("=" * 46)
    print("QXP02V01 NAVIGATION STATISTICS")
    print("=" * 46)
    print(f"Runtime             : {runtime:7.1f} seconds")
    print(f"Obstacles detected  : {obstacleCount}")
    print(f"Left turns          : {leftTurnCount}")
    print(f"Right turns         : {rightTurnCount}")
    print(f"Recovery actions    : {recoveryCount}")
    print(f"Current state       : {stateNames[currentState]}")
    print("=" * 46)


# ============================================================
# Startup Message
# ============================================================

print("=" * 52)
print("QXP02V01 — AUTONOMOUS OBSTACLE AVOIDANCE ROBOT")
print("Quantheonix controller started successfully.")
print("=" * 52)
print("Eight proximity sensors initialized.")
print("Robot is ready.\n")


# ============================================================
# Main Control Loop
# ============================================================

while robot.step(timeStep) != -1:

    currentTime = robot.getTime()

    # --------------------------------------------------------
    # Read all eight sensors
    # --------------------------------------------------------

    sensorValues = [sensor.getValue() for sensor in sensors]

    frontRight = sensorValues[0]
    rightFront = sensorValues[1]
    rightRear = sensorValues[2]

    backRight = sensorValues[3]
    backLeft = sensorValues[4]

    leftRear = sensorValues[5]
    leftFront = sensorValues[6]
    frontLeft = sensorValues[7]

    # --------------------------------------------------------
    # Process sensor groups
    # --------------------------------------------------------

    frontValue = max(frontLeft, frontRight)

    leftValue = max(
        frontLeft,
        leftFront,
        leftRear
    )

    rightValue = max(
        frontRight,
        rightFront,
        rightRear
    )

    backValue = max(backLeft, backRight)

    frontClear = frontValue < clearThreshold

    printStateChange()

    # --------------------------------------------------------
    # State: FORWARD
    # --------------------------------------------------------

    if currentState == FORWARD:

        leftSpeed = forwardSpeed
        rightSpeed = forwardSpeed

        sensorDifference = frontLeft - frontRight

        # Obstacle is closer on the left.
        # Turn slightly toward the right.
        if sensorDifference > steeringDifference:
            leftSpeed = forwardSpeed
            rightSpeed = slowSpeed

        # Obstacle is closer on the right.
        # Turn slightly toward the left.
        elif sensorDifference < -steeringDifference:
            leftSpeed = slowSpeed
            rightSpeed = forwardSpeed

        setMotorSpeeds(leftSpeed, rightSpeed)

        if frontValue > frontThreshold:

            obstacleCount += 1

            print(
                f"\nObstacle #{obstacleCount} detected | "
                f"Front-left: {frontLeft:.0f} | "
                f"Front-right: {frontRight:.0f}"
            )

            # Detect repeated obstacle encounters.
            if currentTime - lastObstacleTime < stuckTimeWindow:
                repeatedObstacleCount += 1
            else:
                repeatedObstacleCount = 1

            lastObstacleTime = currentTime

            setMotorSpeeds(0.0, 0.0)

            # Repeated detection means the robot may be trapped.
            if repeatedObstacleCount >= maximumRepeatedObstacles:
                print("Possible corner or trapped condition detected.")
                changeState(BACKWARD)
            else:
                changeState(STOP)

    # --------------------------------------------------------
    # State: STOP
    # --------------------------------------------------------

    elif currentState == STOP:

        setMotorSpeeds(0.0, 0.0)

        if getStateElapsedTime() >= stopDuration:
            changeState(ANALYZE)

    # --------------------------------------------------------
    # State: ANALYZE
    # --------------------------------------------------------

    elif currentState == ANALYZE:

        setMotorSpeeds(0.0, 0.0)

        print(
            f"Analyzing path | "
            f"Left: {leftValue:.0f} | "
            f"Right: {rightValue:.0f}"
        )

        # Lower proximity reading means more free space.
        if leftValue < rightValue:
            leftTurnCount += 1
            lastTurnDirection = TURN_LEFT

            print("Decision: turn left.")
            changeState(TURN_LEFT)

        elif rightValue < leftValue:
            rightTurnCount += 1
            lastTurnDirection = TURN_RIGHT

            print("Decision: turn right.")
            changeState(TURN_RIGHT)

        else:
            # Alternate when both directions look equal.
            if lastTurnDirection == TURN_LEFT:
                rightTurnCount += 1
                lastTurnDirection = TURN_RIGHT

                print("Paths are equal. Alternating to the right.")
                changeState(TURN_RIGHT)

            else:
                leftTurnCount += 1
                lastTurnDirection = TURN_LEFT

                print("Paths are equal. Alternating to the left.")
                changeState(TURN_LEFT)

    # --------------------------------------------------------
    # State: TURN LEFT
    # --------------------------------------------------------

    elif currentState == TURN_LEFT:

        setMotorSpeeds(-turnSpeed, turnSpeed)

        elapsedTime = getStateElapsedTime()

        if (
            elapsedTime >= minimumTurnDuration
            and frontClear
        ):
            setMotorSpeeds(0.0, 0.0)
            changeState(FORWARD)

        elif elapsedTime >= maximumTurnDuration:
            setMotorSpeeds(0.0, 0.0)
            changeState(FORWARD)

    # --------------------------------------------------------
    # State: TURN RIGHT
    # --------------------------------------------------------

    elif currentState == TURN_RIGHT:

        setMotorSpeeds(turnSpeed, -turnSpeed)

        elapsedTime = getStateElapsedTime()

        if (
            elapsedTime >= minimumTurnDuration
            and frontClear
        ):
            setMotorSpeeds(0.0, 0.0)
            changeState(FORWARD)

        elif elapsedTime >= maximumTurnDuration:
            setMotorSpeeds(0.0, 0.0)
            changeState(FORWARD)

    # --------------------------------------------------------
    # State: BACKWARD
    # --------------------------------------------------------

    elif currentState == BACKWARD:

        setMotorSpeeds(-reverseSpeed, -reverseSpeed)

        # Stop reversing early if something is behind the robot.
        if backValue > frontThreshold:
            print("Rear obstacle detected. Ending reverse early.")
            setMotorSpeeds(0.0, 0.0)

            recoveryCount += 1

            if lastTurnDirection == TURN_LEFT:
                recoveryTurnDirection = TURN_RIGHT
            else:
                recoveryTurnDirection = TURN_LEFT

            changeState(RECOVERY_TURN)

        elif getStateElapsedTime() >= reverseDuration:
            setMotorSpeeds(0.0, 0.0)

            recoveryCount += 1

            if lastTurnDirection == TURN_LEFT:
                recoveryTurnDirection = TURN_RIGHT
            else:
                recoveryTurnDirection = TURN_LEFT

            changeState(RECOVERY_TURN)

    # --------------------------------------------------------
    # State: RECOVERY TURN
    # --------------------------------------------------------

    elif currentState == RECOVERY_TURN:

        if recoveryTurnDirection == TURN_LEFT:
            setMotorSpeeds(-turnSpeed, turnSpeed)
        else:
            setMotorSpeeds(turnSpeed, -turnSpeed)

        if getStateElapsedTime() >= recoveryTurnDuration:
            setMotorSpeeds(0.0, 0.0)

            repeatedObstacleCount = 0

            print("Recovery completed.")
            changeState(FORWARD)

    # --------------------------------------------------------
    # Periodic statistics
    # --------------------------------------------------------

    if currentTime - lastStatisticsTime >= statisticsInterval:
        printStatistics()
        lastStatisticsTime = currentTime


# ============================================================
# Simulation End
# ============================================================

setMotorSpeeds(0.0, 0.0)
printStatistics()
print("QXP02V01 controller stopped.")