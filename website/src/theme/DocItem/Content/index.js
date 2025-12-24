import React, { useEffect, useState } from 'react';
import Content from '@theme-original/DocItem/Content';
import PersonalizeContent from '@site/src/components/PersonalizeContent';
import TranslateContent from '@site/src/components/TranslateContent';

export default function ContentWrapper(props) {
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [hasInitialized, setHasInitialized] = useState(false);

  // Extract content and title from props when available
  useEffect(() => {
    if (props.content && !hasInitialized) {
      // Extract the content title
      const extractedTitle = props.content.metadata?.title || 'Chapter';
      setTitle(extractedTitle);

      // For the content, we'll use a placeholder since we can't easily extract the full rendered content
      // The actual personalization/translation components will work with the full document
      setContent(`This is the content of the chapter: ${extractedTitle}`);
      setHasInitialized(true);
    }
  }, [props, hasInitialized]);

  return (
    <>
      <PersonalizeContent chapterTitle={title} chapterContent={content} />
      <TranslateContent chapterTitle={title} chapterContent={content} />
      <Content {...props} />
    </>
  );
}