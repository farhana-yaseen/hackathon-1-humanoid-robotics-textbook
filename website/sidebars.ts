import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  modulesSidebar: [
    'intro', // This typically maps to docs/intro.mdx or similar
    {
      type: 'category',
      label: 'Introduction to PhyAI & Humanoid Robotics',
      items: ['introduction/overview'], // Assuming a subdirectory 'introduction'
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: ['module1/overview', 'module1/middleware', 'module1/rclpy', 'module1/urdf'],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: ['module2/overview', 'module2/physics', 'module2/environment-building', 'module2/rendering', 'module2/sensor-simulation'],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: ['module3/overview', 'module3/photorealistic-simulation', 'module3/isaac-ros', 'module3/nav2'],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: ['module4/overview', 'module4/llm-integration', 'module4/cognitive-planning'],
    },
    {
      type: 'category',
      label: 'Capstone Project: Autonomous Humanoid Robot',
      items: ['capstone/overview'],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: ['appendices/hardware-setup', 'appendices/simulation-guides'],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
