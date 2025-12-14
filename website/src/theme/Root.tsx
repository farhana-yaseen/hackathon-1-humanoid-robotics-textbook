import React from "react";
import ChatWidget from "@site/src/components/ChatWidget";
import { AuthProvider } from "@site/src/contexts/AuthContext";
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Inject environment variables to window object for client-side use
// This is a workaround to access environment variables in the browser
declare global {
  interface Window {
    betterAuthUrl: string;
  }
}

export default function Root({ children }) {
  const context = useDocusaurusContext();
  const { betterAuthUrl } = context.siteConfig.customFields as { betterAuthUrl?: string };

  // Set the betterAuthUrl on the window object when the component mounts
  React.useEffect(() => {
    if (typeof window !== 'undefined') {
      window.betterAuthUrl = betterAuthUrl || "http://localhost:3002";
    }
  }, [betterAuthUrl]);

  return (
    <AuthProvider>
      {children}
      <ChatWidget />
    </AuthProvider>
  );
}
