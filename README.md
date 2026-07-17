# QXP02V01 – Autonomous Obstacle Avoidance Robot

![Project](https://img.shields.io/badge/Quantheonix-QXP02V01-blue)
![Platform](https://img.shields.io/badge/Platform-Webots-green)
![Language](https://img.shields.io/badge/Language-Python-yellow)
![Robot](https://img.shields.io/badge/Robot-e--puck-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

# Overview

QXP02V01 is the second robotics research project developed under the **Quantheonix Robotics Research Program**.

The project focuses on autonomous navigation using a differential drive robot inside the Webots simulation environment. The robot continuously explores an unknown environment while detecting obstacles, selecting safer paths, avoiding collisions, recovering from trapped situations, and continuing its navigation without any human intervention.

This project introduces the fundamental concepts of autonomous mobile robotics including sensor processing, finite state machines, reactive navigation, differential drive control, and recovery behaviors.

---

# Project Information

| Item | Value |
|------|-------|
| Project ID | QXP02V01 |
| Project Name | Autonomous Obstacle Avoidance Robot |
| Version | V01 |
| Category | Mobile Robotics |
| Simulation Platform | Webots |
| Robot | e-puck |
| Programming Language | Python |
| Navigation Method | Reactive Navigation |
| Control Architecture | Finite State Machine (FSM) |
| Status | Completed |

---

# Objectives

The primary objectives of this project are:

- Build a fully autonomous mobile robot
- Detect nearby obstacles using infrared proximity sensors
- Navigate without manual control
- Perform smooth steering while moving
- Select safer paths automatically
- Recover from trapped situations
- Demonstrate finite state machine control
- Collect navigation statistics
- Prepare a foundation for advanced robotics projects

---

# Features

- Autonomous forward navigation
- Eight infrared proximity sensors
- Differential drive locomotion
- Front obstacle detection
- Left and right path analysis
- Smooth steering corrections
- Intelligent turning decisions
- Reverse recovery mode
- Corner escape behavior
- Stuck detection
- Runtime statistics
- Modular Python controller
- Expandable architecture

---

# Technologies Used

- Webots
- Python
- e-puck Robot
- Differential Drive
- Infrared Distance Sensors
- Finite State Machine
- Reactive Navigation

---

# Robot Architecture

```
                +-----------------------+
                | Distance Sensors      |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Sensor Processing     |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Decision Engine (FSM) |
                +-----------+-----------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
      Navigation Module          Recovery Module
             |                             |
             +--------------+--------------+
                            |
                            v
                 Differential Drive Motors
                            |
                            v
                         e-puck Robot
```

---

# Robot Sensors

The robot uses eight infrared proximity sensors.

| Sensor | Position |
|----------|----------------|
| ps0 | Front Right |
| ps1 | Right Front |
| ps2 | Right Rear |
| ps3 | Back Right |
| ps4 | Back Left |
| ps5 | Left Rear |
| ps6 | Left Front |
| ps7 | Front Left |

Sensor Rule

```
Higher Value  → Obstacle is closer

Lower Value   → Free Space
```

---

# Navigation Algorithm

The robot continuously performs the following sequence.

```
Move Forward

↓

Read Sensors

↓

Obstacle?

↓

No
↓

Continue Moving

↓

Yes

↓

Stop

↓

Analyze Left & Right

↓

Choose Safer Direction

↓

Turn

↓

Continue Moving

↓

Repeat Forever
```

---

# Finite State Machine

The robot controller consists of seven states.

| State | Description |
|----------|-----------------------------|
| FORWARD | Move forward |
| STOP | Stop robot |
| ANALYZE | Compare left/right sensors |
| TURN_LEFT | Rotate left |
| TURN_RIGHT | Rotate right |
| BACKWARD | Reverse robot |
| RECOVERY_TURN | Escape from trapped area |

State Flow

```
               FORWARD
                   |
           Obstacle Detected
                   |
                   v
                STOP
                   |
                   v
              ANALYZE
             /        \
            /          \
     TURN_LEFT      TURN_RIGHT
            \          /
             \        /
               FORWARD


If Robot Gets Trapped

FORWARD

↓

BACKWARD

↓

RECOVERY TURN

↓

FORWARD
```

---

# Controller Configuration

The robot behavior is controlled by configurable parameters.

```python
forwardSpeed = 3.0
slowSpeed = 1.8
turnSpeed = 2.7
reverseSpeed = 2.0

frontThreshold = 80
clearThreshold = 45

minimumTurnDuration = 0.30
maximumTurnDuration = 1.50

reverseDuration = 0.80
recoveryTurnDuration = 1.30
```

These values can be modified depending on the simulation environment.

---

# Project Structure

```
QXP02V01_Autonomous_Obstacle_Avoidance
│
├── controllers
│   └── obstacle_avoidance_controller
│       └── obstacle_avoidance_controller.py
│
├── worlds
│   ├── ObstacleAvoidance.wbt
│   ├── ObstacleAvoidance_Easy.wbt
│   ├── ObstacleAvoidance_Medium.wbt
│   └── ObstacleAvoidance_Hard.wbt
│
├── documentation
│
├── screenshots
│
├── videos
│
├── README.md
│
└── CHANGELOG.md
```

---

# Installation

## Requirements

- Webots
- Python (compatible with your Webots version)

---

## Running the Project

1. Open Webots

2. Open

```
worlds/ObstacleAvoidance.wbt
```

3. Select the e-puck robot

4. Set controller

```
obstacle_avoidance_controller
```

5. Save

6. Press Reset

7. Press Run

The robot should immediately begin exploring.

---

# Robot Behaviour

The robot performs the following actions automatically.

- Drive forward
- Detect nearby obstacles
- Steer around objects
- Stop before collisions
- Compare left and right paths
- Select safer direction
- Turn
- Continue moving
- Reverse when trapped
- Perform recovery turn
- Continue exploration

---

# Navigation Statistics

During execution the controller records:

- Runtime
- Obstacles detected
- Left turns
- Right turns
- Recovery actions
- Current robot state

Example

```
=====================================
QXP02V01 Navigation Statistics
=====================================

Runtime : 120 sec

Obstacles : 18

Left Turns : 9

Right Turns : 9

Recoveries : 2

Current State : FORWARD

=====================================
```

---

# Testing

The project should be tested using multiple environments.

## Easy

Large open space with few obstacles.

Purpose

- Verify movement
- Verify sensors

---

## Medium

Moderate obstacle density.

Purpose

- Test steering
- Test decision making

---

## Hard

Dense obstacle environment.

Purpose

- Test recovery
- Test corner escape

---

## Maze

Complex corridors.

Purpose

- Long duration testing
- Stability evaluation

---

# Functional Checklist

- ✔ Robot moves autonomously
- ✔ Reads all eight sensors
- ✔ Detects front obstacles
- ✔ Smooth steering
- ✔ Stops safely
- ✔ Chooses better direction
- ✔ Turns left/right
- ✔ Reverse recovery
- ✔ Corner escape
- ✔ Stuck detection
- ✔ Navigation statistics
- ✔ Stable autonomous operation

---

# Learning Outcomes

This project teaches

- Mobile Robotics
- Differential Drive Control
- Sensor Integration
- Python Robotics Programming
- Webots Simulation
- Finite State Machines
- Autonomous Navigation
- Obstacle Avoidance
- Recovery Algorithms
- Robot Decision Making

---

# Future Improvements

Future versions may include

- Wheel Encoder Integration
- Camera Vision
- SLAM
- Occupancy Grid Mapping
- A* Path Planning
- Dijkstra Navigation
- GPS Localization
- Compass Integration
- LiDAR
- Reinforcement Learning
- Deep Learning
- Multi-Robot Coordination

---

 - QXP02V01
 - Status: COMPLETED
 - Release: V01

---

# Author

**Quantheonix Robotics Research**

Research Focus

- Robotics
- Artificial Intelligence
- Computer Vision
- Embedded Systems
- Autonomous Systems
- Human Robot Interaction

---

# License

This project is developed for educational, research, and portfolio purposes.

Copyright © Quantheonix Robotics Research.