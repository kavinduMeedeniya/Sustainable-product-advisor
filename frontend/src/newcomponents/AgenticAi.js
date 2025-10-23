import React from 'react';
import './AgenticAi.css';

const AgenticAi = () => {
  const handleButtonClick = (e) => {
    e.preventDefault();
    
    // Create ripple effect
    const ripple = document.createElement('span');
    const rect = e.currentTarget.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: rgba(255, 255, 0, 0.3);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s linear;
      pointer-events: none;
    `;
    
    e.currentTarget.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);
  };

  return (
    <main className="hero">
      <div className="user-rating">
        <div className="user-avatars">
          <div className="avatar">
            <img 
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80" 
              alt="User 1"
            />
          </div>
          <div className="avatar">
            <img 
              src="https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80" 
              alt="User 2"
            />
          </div>
          <div className="avatar">
            <img 
              src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80" 
              alt="User 3"
            />
          </div>
        </div>
        <span className="rating-text">Trusted by <strong>20K+ professionals</strong> with a</span>
        <span className="stars">★★★★★</span>
        <span className="rating-text"><strong>4.9 rating</strong></span>
      </div>

      <h1 className="hero-title">
        From <span className="highlight">AI-powered insights</span> to business<br />
        transformation, innovate smarter!
      </h1>

      <p className="hero-subtitle">
        Discover how AgenticAI makes intelligent automation effortless with advanced algorithms and intuitive interfaces.
      </p>

      <div className="cta-buttons">
        <a href="#" className="btn-primary" onClick={handleButtonClick}>
          Get Started
        </a>
        <a href="#" className="btn-secondary" onClick={handleButtonClick}>
          View Demos
        </a>
      </div>
    </main>
  );
};

export default AgenticAi;