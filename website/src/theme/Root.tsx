import React from 'react';
import type {PropsWithChildren} from 'react';

// Assuming Better Auth SDK has an initialization function
// import { initBetterAuth } from '@better-auth/sdk';

export default function Root({children}: PropsWithChildren): JSX.Element {
  // Initialize Better Auth SDK here
  // initBetterAuth({
  //   clientId: 'YOUR_CLIENT_ID',
  //   domain: 'YOUR_DOMAIN',
  //   // ... other configuration options
  // });

  return (
    <>
      {children}
    </>
  );
}
