import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug', '52e'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/config',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/config', '550'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/content',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/content', 'd4b'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/globalData',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/globalData', 'd41'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/metadata',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/metadata', '13e'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/registry',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/registry', '53c'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/__docusaurus/debug/routes',
    component: ComponentCreator('/humanoid-robotics-textbook/__docusaurus/debug/routes', '667'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog',
    component: ComponentCreator('/humanoid-robotics-textbook/blog', 'f2e'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/archive',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/archive', '91a'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/authors',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/authors', '224'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/authors/all-sebastien-lorber-articles', '0d7'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/authors/yangshun',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/authors/yangshun', 'e47'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/first-blog-post',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/first-blog-post', '673'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/long-blog-post',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/long-blog-post', '732'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/mdx-blog-post',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/mdx-blog-post', 'b9e'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/tags',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/tags', '29c'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/tags/docusaurus',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/tags/docusaurus', '90e'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/tags/facebook',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/tags/facebook', '91c'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/tags/hello',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/tags/hello', 'a2a'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/tags/hola',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/tags/hola', 'f70'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/blog/welcome',
    component: ComponentCreator('/humanoid-robotics-textbook/blog/welcome', '7af'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/markdown-page',
    component: ComponentCreator('/humanoid-robotics-textbook/markdown-page', 'e6c'),
    exact: true
  },
  {
    path: '/humanoid-robotics-textbook/docs',
    component: ComponentCreator('/humanoid-robotics-textbook/docs', '558'),
    routes: [
      {
        path: '/humanoid-robotics-textbook/docs',
        component: ComponentCreator('/humanoid-robotics-textbook/docs', 'b21'),
        routes: [
          {
            path: '/humanoid-robotics-textbook/docs',
            component: ComponentCreator('/humanoid-robotics-textbook/docs', 'd9c'),
            routes: [
              {
                path: '/humanoid-robotics-textbook/docs/appendices/hardware-requirements',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/appendices/hardware-requirements', '529'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/appendices/hardware-setup',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/appendices/hardware-setup', 'ea6'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/appendices/simulation-guides',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/appendices/simulation-guides', '85c'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/capstone/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/capstone/overview', '195'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/intro',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/intro', 'df1'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/introduction/chapter1',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/introduction/chapter1', '14e'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/introduction/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/introduction/overview', 'c4e'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/chapter1',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/chapter1', '6cf'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/middleware',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/middleware', '2ba'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/module1-personalized-example',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/module1-personalized-example', '0f0'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/overview', '6ec'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/rclpy',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/rclpy', '0d4'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module1/urdf',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module1/urdf', 'fdd'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/chapter1',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/chapter1', '870'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/environment-building',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/environment-building', '66c'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/overview', '482'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/physics',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/physics', '857'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/rendering',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/rendering', '6c7'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module2/sensor-simulation',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module2/sensor-simulation', '0e8'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module3/chapter1',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module3/chapter1', 'e8f'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/module3/isaac-ros',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module3/isaac-ros', '697'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module3/nav2',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module3/nav2', '213'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module3/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module3/overview', '327'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module3/photorealistic-simulation',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module3/photorealistic-simulation', '4b7'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module4/chapter1',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module4/chapter1', '16f'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/humanoid-robotics-textbook/docs/module4/cognitive-planning',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module4/cognitive-planning', '1f9'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module4/llm-integration',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module4/llm-integration', 'a3b'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module4/overview',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module4/overview', '3df'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/module4/vla',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/module4/vla', 'fec'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/textbook_outline',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/textbook_outline', '357'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/congratulations', '6f3'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/create-a-blog-post', '1a5'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/create-a-document', '291'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/create-a-page', '492'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/deploy-your-site', '50a'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-basics/markdown-features', '1b9'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-extras/manage-docs-versions', '811'),
                exact: true
              },
              {
                path: '/humanoid-robotics-textbook/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/humanoid-robotics-textbook/docs/tutorial-extras/translate-your-site', '33d'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/humanoid-robotics-textbook/',
    component: ComponentCreator('/humanoid-robotics-textbook/', '436'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
