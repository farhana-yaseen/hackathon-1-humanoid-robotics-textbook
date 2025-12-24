// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  modulesSidebar: [
    'intro', // This typically maps to docs/intro.mdx or similar
    {
      type: 'category',
      label: 'Introduction to PhyAI & Humanoid Robotics',
      items: ['introduction/chapter1'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: ['module1/chapter1'],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: ['module2/chapter1'],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: ['module3/chapter1'],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: ['module4/chapter1'],
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
};

module.exports = sidebars;