# QXP02V01 Project Summary

## Project Title

Autonomous Obstacle Avoidance Robot

## Project ID

QXP02V01

## Platform

Webots

## Programming Language

Python

## Robot Model

e-puck

## Project Overview

QXP02V01 is an autonomous mobile robotics project developed under the Quantheonix project series.

The project uses an e-puck robot in Webots to demonstrate reactive obstacle avoidance, differential-drive movement, proximity sensor processing, finite state machine control, and recovery behaviour.

The robot navigates without manual input. It moves forward, detects obstacles, analyzes available space, selects a safer turning direction, reverses when repeatedly blocked, and continues exploration.

## Main Functionalities

- Autonomous movement
- Infrared proximity sensing
- Obstacle detection
- Smooth steering
- Direction selection
- Finite state machine control
- Reverse recovery
- Trapped-condition handling
- Runtime statistics
- Multi-environment testing

## Controller States

- FORWARD
- STOP
- ANALYZE
- TURN_LEFT
- TURN_RIGHT
- BACKWARD
- RECOVERY_TURN

## Final Outcome

The project successfully demonstrates a complete reactive obstacle avoidance system in simulation.

The robot can operate independently in multiple environments and recover from many common trapped situations.

## Skills Developed

- Webots simulation
- Python robotics programming
- Differential-drive control
- Sensor integration
- Finite state machines
- Reactive navigation
- Recovery logic
- Controller tuning
- Robotics testing
- Technical documentation

## Project Status

Completed
