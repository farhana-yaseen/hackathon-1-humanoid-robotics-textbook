# Humanoid Robotics Textbook Outline

## Introduction: Physical AI & Humanoid Robotics
- Focus and Theme: AI Systems in the Physical World. Embodied Intelligence.
- Goal: Bridge the gap between the digital brain and the physical body.
- Quarter Overview: Introduction to Physical AI, designing, simulating, and deploying humanoid robots.
- Why Physical AI Matters: Humanoid robots in human-centered spaces.
- Learning Outcomes:
    - Understand Physical AI and embodied intelligence
    - Master ROS 2 for robotic control
    - Simulate robots in Gazebo and Unity
    - Develop with NVIDIA Isaac robotics platform
    - Design humanoid robots for natural interactions
    - Integrate GPT models for conversational robotics

## Module 1: The Robotic Nervous System (ROS 2)
- Focus: Middleware for robot control.
- Topics:
    - ROS 2 Nodes, Topics, and Services
    - Bridging Python Agents to ROS controllers using `rclpy`
    - Understanding URDF (Unified Robot Description Format) for humanoids
- Weeks 3–5: ROS 2 Fundamentals
    - ROS 2 architecture and API
    - Nodes, topics, services, actions
    - Building ROS 2 packages with Python
    - Launch files & parameters

## Module 2: The Digital Twin (Gazebo & Unity)
- Focus: Physics simulation and environment building.
- Topics:
    - Simulating physics, gravity, collisions in Gazebo
    - High-fidelity human–robot interaction in Unity
    - Simulating sensors: LiDAR, Depth Cameras, IMUs
- Weeks 6–7: Robot Simulation with Gazebo
    - Gazebo setup
    - URDF/SDF
    - Physics + sensor simulation
    - Unity visualization

## Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Focus: Advanced perception and training.
- Topics:
    - Isaac Sim for photorealistic simulation + synthetic data
    - Isaac ROS for hardware-accelerated VSLAM & navigation
    - Nav2 for bipedal humanoid motion planning
- Weeks 8–10: NVIDIA Isaac Platform
    - Isaac SDK & Isaac Sim
    - AI-powered perception and manipulation
    - Reinforcement learning
    - Sim-to-Real transfer

## Module 4: Vision–Language–Action (VLA)
- Focus: The convergence of LLMs and Robotics.
- Topics:
    - Voice-to-Action with Whisper
    - Cognitive Planning using LLMs
- Week 13: Conversational Robotics
    - Integrating GPT models
    - Speech recognition & NLU
    - Multi-modal interaction
- Capstone Project: A robot receives a voice command → plans a path → navigates obstacles → identifies an object → manipulates it.

## Appendices
### Hardware Requirements
- **The “Digital Twin” Workstation (Required per Student)**
    - GPU: RTX 4070 Ti (min), 3090/4090 ideal (24GB VRAM)
    - CPU: Intel i7 13th Gen+ / Ryzen 9
    - RAM: 64GB recommended (32GB minimum)
    - OS: Ubuntu 22.04 LTS
- **The “Physical AI” Edge Kit**
    - Brain: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)
    - Eyes: Intel RealSense D435i / D455
    - Inner Ear: USB IMU (BNO055)
    - Voice: USB Mic Array (ReSpeaker)
- **The Robot Lab (Three Options)**
    - Option A — Proxy Robots (Recommended Budget Option): Unitree Go2 Edu
    - Option B — Mini Humanoids: Unitree G1 (~$16k), Robotis OP3, Hiwonder TonyPi Pro
    - Option C — Premium Lab (Humanoid Deployment): Unitree G1 Humanoid
- **Summary of Architecture**
    - Sim Rig: RTX 4080 PC + Ubuntu (Runs Isaac, Gazebo, Unity, VLA)
    - Edge Brain: Jetson Orin Nano (AI inference stack)
    - Sensors: RealSense + LiDAR (Real-world perception input)
    - Actuator: Unitree Go2 or G1 (Executes movement commands)
- **Cloud Option: “Ether Lab” (High OpEx)**
    - Cloud Workstations: AWS g5/g6e GPU instances
    - Required Local Hardware: Jetson Kit, Unitree Go2 robot
- **Economy Jetson Student Kit (~$700)**
    - Brain: Jetson Orin Nano (8GB)
    - Eyes: RealSense D435i
    - Ears: ReSpeaker USB Mic Array
    - Misc: SD Card + wires
- **The Latency Trap (Important Note)**
    - Solution: Train in cloud → download weights → deploy on Jetson locally.

### Assessments
- ROS 2 package development
- Gazebo simulation
- Isaac-based perception pipeline
- Capstone: Simulated humanoid with conversational AI


import Chatbot from '@site/src/components/Chatbot';


<Chatbot />

You can select any section above and ask questions about it.
