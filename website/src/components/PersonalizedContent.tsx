import React from 'react';

interface PersonalizedContentProps {
  children: React.ReactNode;
  userBackground: string; // e.g., 'software' or 'hardware'
  requiredBackground: string; // Background required for this content block
}

export default function PersonalizedContent({
  children,
  userBackground,
  requiredBackground,
}: PersonalizedContentProps): JSX.Element {
  if (userBackground === requiredBackground) {
    return <>{children}</>;
  }
  return null; // Or show a message indicating content is not relevant
}
