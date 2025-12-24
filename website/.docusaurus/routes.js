import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/auth/signin',
    component: ComponentCreator('/auth/signin', 'df3'),
    exact: true
  },
  {
    path: '/auth/signup',
    component: ComponentCreator('/auth/signup', 'e56'),
    exact: true
  },
  {
    path: '/book',
    component: ComponentCreator('/book', '513'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '610'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '2b0'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '85f'),
            routes: [
              {
                path: '/docs/appendices/hardware-requirements',
                component: ComponentCreator('/docs/appendices/hardware-requirements', 'b37'),
                exact: true
              },
              {
                path: '/docs/appendices/hardware-setup',
                component: ComponentCreator('/docs/appendices/hardware-setup', '540'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/appendices/simulation-guides',
                component: ComponentCreator('/docs/appendices/simulation-guides', 'ca6'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/capstone/overview',
                component: ComponentCreator('/docs/capstone/overview', '3e7'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'eb9'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/introduction/chapter1',
                component: ComponentCreator('/docs/introduction/chapter1', '213'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/introduction/overview',
                component: ComponentCreator('/docs/introduction/overview', '607'),
                exact: true
              },
              {
                path: '/docs/module1/chapter1',
                component: ComponentCreator('/docs/module1/chapter1', '8d5'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/module1/middleware',
                component: ComponentCreator('/docs/module1/middleware', 'd14'),
                exact: true
              },
              {
                path: '/docs/module1/module1-personalized-example',
                component: ComponentCreator('/docs/module1/module1-personalized-example', '43a'),
                exact: true
              },
              {
                path: '/docs/module1/overview',
                component: ComponentCreator('/docs/module1/overview', '810'),
                exact: true
              },
              {
                path: '/docs/module1/rclpy',
                component: ComponentCreator('/docs/module1/rclpy', 'f19'),
                exact: true
              },
              {
                path: '/docs/module1/urdf',
                component: ComponentCreator('/docs/module1/urdf', 'ac8'),
                exact: true
              },
              {
                path: '/docs/module2/chapter1',
                component: ComponentCreator('/docs/module2/chapter1', 'c60'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/module2/environment-building',
                component: ComponentCreator('/docs/module2/environment-building', 'c62'),
                exact: true
              },
              {
                path: '/docs/module2/overview',
                component: ComponentCreator('/docs/module2/overview', '6c5'),
                exact: true
              },
              {
                path: '/docs/module2/physics',
                component: ComponentCreator('/docs/module2/physics', 'fb0'),
                exact: true
              },
              {
                path: '/docs/module2/rendering',
                component: ComponentCreator('/docs/module2/rendering', '218'),
                exact: true
              },
              {
                path: '/docs/module2/sensor-simulation',
                component: ComponentCreator('/docs/module2/sensor-simulation', 'fe4'),
                exact: true
              },
              {
                path: '/docs/module3/chapter1',
                component: ComponentCreator('/docs/module3/chapter1', '10d'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/module3/isaac-ros',
                component: ComponentCreator('/docs/module3/isaac-ros', '065'),
                exact: true
              },
              {
                path: '/docs/module3/nav2',
                component: ComponentCreator('/docs/module3/nav2', 'ebf'),
                exact: true
              },
              {
                path: '/docs/module3/overview',
                component: ComponentCreator('/docs/module3/overview', 'ffe'),
                exact: true
              },
              {
                path: '/docs/module3/photorealistic-simulation',
                component: ComponentCreator('/docs/module3/photorealistic-simulation', '3a0'),
                exact: true
              },
              {
                path: '/docs/module4/chapter1',
                component: ComponentCreator('/docs/module4/chapter1', '384'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/docs/module4/cognitive-planning',
                component: ComponentCreator('/docs/module4/cognitive-planning', 'ec8'),
                exact: true
              },
              {
                path: '/docs/module4/llm-integration',
                component: ComponentCreator('/docs/module4/llm-integration', 'b0e'),
                exact: true
              },
              {
                path: '/docs/module4/overview',
                component: ComponentCreator('/docs/module4/overview', '85d'),
                exact: true
              },
              {
                path: '/docs/module4/vla',
                component: ComponentCreator('/docs/module4/vla', '82b'),
                exact: true
              },
              {
                path: '/docs/textbook_outline',
                component: ComponentCreator('/docs/textbook_outline', 'f1f'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
te-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
