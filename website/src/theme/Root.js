import React from "react";
import ChatWidget from "@site/src/components/ChatWidget";
import { AuthProvider } from "@site/src/contexts/AuthContext";
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Root({ children }) {
  const context = useDocusaurusContext();
  const { betterAuthUrl } = context.siteConfig.customFields || {};

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