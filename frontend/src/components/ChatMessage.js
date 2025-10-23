import React from 'react';
import ProductResponse from './ProductResponse';

const ChatMessage = ({ role, content }) => {
  const isUser = role === 'user';
  const messageClass = isUser ? 'user-message' : 'assistant-message';

  if (isUser) {
    return <div className={`message ${messageClass}`}>{content}</div>;
  }

  // For assistant: check if it's a simple message or product response
  if (content.message) {
    return <div className={`message ${messageClass} ${content.message.startsWith('Error:') ? 'error-message' : ''}`}>{content.message}</div>;
  } else if (content.type === 'product') {
    return (
      <div className={`message ${messageClass}`}>
        <ProductResponse data={content} />
      </div>
    );
  }

  return <div className={`message ${messageClass}`}>Unknown response type.</div>;
};

export default ChatMessage;