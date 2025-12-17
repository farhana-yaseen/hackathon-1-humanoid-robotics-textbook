import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ur/auth/signin',
    component: ComponentCreator('/ur/auth/signin', '8a9'),
    exact: true
  },
  {
    path: '/ur/auth/signup',
    component: ComponentCreator('/ur/auth/signup', '007'),
    exact: true
  },
  {
    path: '/ur/blog',
    component: ComponentCreator('/ur/blog', '5a6'),
    exact: true
  },
  {
    path: '/ur/blog/archive',
    component: ComponentCreator('/ur/blog/archive', '1c5'),
    exact: true
  },
  {
    path: '/ur/blog/authors',
    component: ComponentCreator('/ur/blog/authors', '186'),
    exact: true
  },
  {
    path: '/ur/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/ur/blog/authors/all-sebastien-lorber-articles', '536'),
    exact: true
  },
  {
    path: '/ur/blog/authors/yangshun',
    component: ComponentCreator('/ur/blog/authors/yangshun', '09b'),
    exact: true
  },
  {
    path: '/ur/blog/first-blog-post',
    component: ComponentCreator('/ur/blog/first-blog-post', 'fdc'),
    exact: true
  },
  {
    path: '/ur/blog/long-blog-post',
    component: ComponentCreator('/ur/blog/long-blog-post', '941'),
    exact: true
  },
  {
    path: '/ur/blog/mdx-blog-post',
    component: ComponentCreator('/ur/blog/mdx-blog-post', 'db8'),
    exact: true
  },
  {
    path: '/ur/blog/tags',
    component: ComponentCreator('/ur/blog/tags', '14b'),
    exact: true
  },
  {
    path: '/ur/blog/tags/docusaurus',
    component: ComponentCreator('/ur/blog/tags/docusaurus', '591'),
    exact: true
  },
  {
    path: '/ur/blog/tags/facebook',
    component: ComponentCreator('/ur/blog/tags/facebook', 'bc0'),
    exact: true
  },
  {
    path: '/ur/blog/tags/hello',
    component: ComponentCreator('/ur/blog/tags/hello', '6e2'),
    exact: true
  },
  {
    path: '/ur/blog/tags/hola',
    component: ComponentCreator('/ur/blog/tags/hola', '2c4'),
    exact: true
  },
  {
    path: '/ur/blog/welcome',
    component: ComponentCreator('/ur/blog/welcome', 'c57'),
    exact: true
  },
  {
    path: '/ur/book',
    component: ComponentCreator('/ur/book', 'fad'),
    exact: true
  },
  {
    path: '/ur/markdown-page',
    component: ComponentCreator('/ur/markdown-page', 'c0a'),
    exact: true
  },
  {
    path: '/ur/docs',
    component: ComponentCreator('/ur/docs', '345'),
    routes: [
      {
        path: '/ur/docs',
        component: ComponentCreator('/ur/docs', 'f69'),
        routes: [
          {
            path: '/ur/docs',
            component: ComponentCreator('/ur/docs', '27d'),
            routes: [
              {
                path: '/ur/docs/appendices/hardware-requirements',
                component: ComponentCreator('/ur/docs/appendices/hardware-requirements', 'adf'),
                exact: true
              },
              {
                path: '/ur/docs/appendices/hardware-setup',
                component: ComponentCreator('/ur/docs/appendices/hardware-setup', '4f6'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/appendices/simulation-guides',
                component: ComponentCreator('/ur/docs/appendices/simulation-guides', '442'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/capstone/overview',
                component: ComponentCreator('/ur/docs/capstone/overview', 'e22'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/intro',
                component: ComponentCreator('/ur/docs/intro', 'b05'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/introduction/chapter1',
                component: ComponentCreator('/ur/docs/introduction/chapter1', '16a'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/introduction/overview',
                component: ComponentCreator('/ur/docs/introduction/overview', '448'),
                exact: true
              },
              {
                path: '/ur/docs/module1/chapter1',
                component: ComponentCreator('/ur/docs/module1/chapter1', '9b0'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/module1/middleware',
                component: ComponentCreator('/ur/docs/module1/middleware', 'ff5'),
                exact: true
              },
              {
                path: '/ur/docs/module1/module1-personalized-example',
                component: ComponentCreator('/ur/docs/module1/module1-personalized-example', '5a8'),
                exact: true
              },
              {
                path: '/ur/docs/module1/overview',
                component: ComponentCreator('/ur/docs/module1/overview', '2f8'),
                exact: true
              },
              {
                path: '/ur/docs/module1/rclpy',
                component: ComponentCreator('/ur/docs/module1/rclpy', 'd87'),
                exact: true
              },
              {
                path: '/ur/docs/module1/urdf',
                component: ComponentCreator('/ur/docs/module1/urdf', '298'),
                exact: true
              },
              {
                path: '/ur/docs/module2/chapter1',
                component: ComponentCreator('/ur/docs/module2/chapter1', '884'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/module2/environment-building',
                component: ComponentCreator('/ur/docs/module2/environment-building', '412'),
                exact: true
              },
              {
                path: '/ur/docs/module2/overview',
                component: ComponentCreator('/ur/docs/module2/overview', '208'),
                exact: true
              },
              {
                path: '/ur/docs/module2/physics',
                component: ComponentCreator('/ur/docs/module2/physics', 'ee3'),
                exact: true
              },
              {
                path: '/ur/docs/module2/rendering',
                component: ComponentCreator('/ur/docs/module2/rendering', 'be7'),
                exact: true
              },
              {
                path: '/ur/docs/module2/sensor-simulation',
                component: ComponentCreator('/ur/docs/module2/sensor-simulation', 'd9d'),
                exact: true
              },
              {
                path: '/ur/docs/module3/chapter1',
                component: ComponentCreator('/ur/docs/module3/chapter1', '7cd'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/module3/isaac-ros',
                component: ComponentCreator('/ur/docs/module3/isaac-ros', '896'),
                exact: true
              },
              {
                path: '/ur/docs/module3/nav2',
                component: ComponentCreator('/ur/docs/module3/nav2', '077'),
                exact: true
              },
              {
                path: '/ur/docs/module3/overview',
                component: ComponentCreator('/ur/docs/module3/overview', '1d0'),
                exact: true
              },
              {
                path: '/ur/docs/module3/photorealistic-simulation',
                component: ComponentCreator('/ur/docs/module3/photorealistic-simulation', '42a'),
                exact: true
              },
              {
                path: '/ur/docs/module4/chapter1',
                component: ComponentCreator('/ur/docs/module4/chapter1', 'da2'),
                exact: true,
                sidebar: "modulesSidebar"
              },
              {
                path: '/ur/docs/module4/cognitive-planning',
                component: ComponentCreator('/ur/docs/module4/cognitive-planning', '789'),
                exact: true
              },
              {
                path: '/ur/docs/module4/llm-integration',
                component: ComponentCreator('/ur/docs/module4/llm-integration', '32f'),
                exact: true
              },
              {
                path: '/ur/docs/module4/overview',
                component: ComponentCreator('/ur/docs/module4/overview', 'e74'),
                exact: true
              },
              {
                path: '/ur/docs/module4/vla',
                component: ComponentCreator('/ur/docs/module4/vla', '51f'),
                exact: true
              },
              {
                path: '/ur/docs/textbook_outline',
                component: ComponentCreator('/ur/docs/textbook_outline', 'e7b'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/ur/docs/tutorial-basics/congratulations', '48c'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/ur/docs/tutorial-basics/create-a-blog-post', 'fe4'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/ur/docs/tutorial-basics/create-a-document', 'c4a'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/ur/docs/tutorial-basics/create-a-page', '3f5'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/ur/docs/tutorial-basics/deploy-your-site', '66d'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/ur/docs/tutorial-basics/markdown-features', '99c'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/ur/docs/tutorial-extras/manage-docs-versions', 'a05'),
                exact: true
              },
              {
                path: '/ur/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/ur/docs/tutorial-extras/translate-your-site', 'c1e'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/ur/',
    component: ComponentCreator('/ur/', '3b1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
