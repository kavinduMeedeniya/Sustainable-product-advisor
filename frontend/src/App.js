import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ChatMessage from './components/ChatMessage';
import AgenticAi from './newcomponents/AgenticAi';
import Whyd from './newcomponents/Whyd';
import ProFeaturesDashboard from './newcomponents/ProFeaturesDashboard';
import PricingComponent from './newcomponents/PricingComponent';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');

    try {
      const response = await axios.post('https://sustainable-product-advisor.onrender.com/chat', { message: input });
      const data = response.data;

      if (data.error) {
        setMessages((prev) => [...prev, { role: 'assistant', content: { message: `Error: ${data.error}` } }]);
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', content: data }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'assistant', content: { message: 'Error: Failed to connect to the server.' } }]);
    }
  };

  return (
    <div className='full_landing'>
      <AgenticAi />
      <Whyd />
      
    <div className="app">
      <div className="left-panel">
        <div className="network-quality-wrapper">
      <div className="network-quality-container">
        <div className="network-quality-header">
          <h1 className="network-quality-heading">
            Improve the quality<br />
            and performance<br />
            of your Website.
          </h1>
        </div>

        

        <div className="network-quality-footer">
          <div className="network-quality-footer-content">
            <div className="network-quality-logo">Chat • Ask • Buy</div>
            <div className="network-quality-footer-text">
              Sustainable solutions for smarter choices.<br />
  Guided by data, tested in real-world use,<br />
  and refined through countless sustainable product recommendations.
            </div>
          </div>
        </div>
      </div>
    </div>
        
      </div>
      
      <div className="right-panel">
        <div className="chat-container">
          <div className="chat-window">
            {messages.map((msg, index) => (
              <ChatMessage key={index} role={msg.role} content={msg.content} />
            ))}
          </div>
          <div className="input-container">
            <input
              className="input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
            />
            <button className="button" onClick={handleSend}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
    <PricingComponent />
    <ProFeaturesDashboard />
    </div>
  );
}

export default App;
