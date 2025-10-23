import React from 'react';
import './Whyd.css';

const Whyd = () => {
  return (
    <div className="whyd-container">
      <div className="whyd-content">
        <h1 className="whyd-headline">
          Your sustainable shopping. <span className="whyd-headline-highlight">Reimagined.</span>
        </h1>
        
        <p className="whyd-description">
          Our AI advisor combines ethical sourcing, environmental impact, and quality to guide you toward conscious purchasing decisions.
        </p>
        
        <div className="whyd-brand-section">
          <div className="whyd-logo">ECOCHOICE</div>
          <div className="whyd-tagline">SMART SUSTAINABILITY</div>
        </div>
      </div>
    </div>
  );
};

export default Whyd;