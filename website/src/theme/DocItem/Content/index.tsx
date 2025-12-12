import React, { JSX } from 'react';
import Content from '@theme-original/DocItem/Content';
import ChapterControls from '@site/src/components/ChapterControls';

export default function ContentWrapper(props): JSX.Element {
  // Placeholder for personalization logic
  const handlePersonalizeClick = () => {
    console.log('Personalize button clicked!');
    // Here you would trigger the personalization logic (T012)
  };

  return (
    <>
      <ChapterControls onPersonalizeClick={handlePersonalizeClick} />
      <Content {...props} />
    </>
  );
}
