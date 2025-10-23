import React, { useEffect } from 'react';

const PricingComponent = () => {
  useEffect(() => {
    // Animate cards on load
    const cards = document.querySelectorAll('.pricing-card');
    cards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      card.style.transition = 'all 0.6s ease';
      
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
        if (card.classList.contains('featured')) {
          card.style.transform = 'scale(1.05) translateY(0)';
        }
      }, index * 150);
    });
  }, []);

  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        .container {
          margin: 0 auto;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
          background: #000000;
          color: #ffffff;
          min-height: 100vh;
          padding: 60px 20px;
        }

        .pricing-header {
          text-align: center;
          margin-bottom: 60px;
        }

        .pricing-label {
          font-size: 12px;
          color: #00b3ff;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 20px;
          font-weight: 600;
        }

        .pricing-title {
          font-size: 48px;
          font-weight: 700;
          line-height: 1.2;
          margin-bottom: 20px;
          color: #ffffff;
        }

        .pricing-subtitle {
          font-size: 18px;
          color: #cccccc;
          line-height: 1.5;
          max-width: 600px;
          margin: 0 auto 40px;
        }

        .pricing-cards {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 24px;
          max-width: 1000px;
          margin: 0 auto;
        }

        .pricing-card {
          background: #1a1a1a;
          border: 1px solid #333333;
          border-radius: 16px;
          padding: 40px 30px;
          position: relative;
          transition: all 0.3s ease;
        }

        .pricing-card:hover {
          transform: translateY(-4px);
          border-color: #00b3ff;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .pricing-card.featured {
          background: #00b3ff;
          color: #000;
          border-color: #00b3ff;
          transform: scale(1.05);
        }

        .pricing-card.featured:hover {
          transform: scale(1.05) translateY(-4px);
        }

        .plan-name {
          font-size: 20px;
          font-weight: 600;
          margin-bottom: 20px;
          color: inherit;
        }

        .plan-price {
          font-size: 40px;
          font-weight: 800;
          margin-bottom: 8px;
          display: flex;
          align-items: baseline;
        }

        .plan-price .currency {
          font-size: 24px;
          margin-right: 2px;
        }

        .plan-price .period {
          font-size: 18px;
          font-weight: 400;
          margin-left: 4px;
          opacity: 0.7;
        }

        .plan-description {
          font-size: 14px;
          margin-bottom: 30px;
          opacity: 0.8;
          line-height: 1.4;
        }

        .features-title {
          font-size: 14px;
          font-weight: 600;
          margin-bottom: 16px;
          color: inherit;
        }

        .features-list {
          list-style: none;
        }

        .features-list li {
          display: flex;
          align-items: flex-start;
          margin-bottom: 12px;
          font-size: 14px;
          line-height: 1.4;
          opacity: 0.9;
        }

        .features-list li::before {
          content: "✓";
          color: #00b3ff;
          font-weight: bold;
          font-size: 14px;
          margin-right: 12px;
          margin-top: 2px;
          flex-shrink: 0;
        }

        .pricing-card.featured .features-list li::before {
          color: #000;
        }

        @media (max-width: 968px) {
          .pricing-title {
            font-size: 36px;
          }
          
          .pricing-cards {
            grid-template-columns: 1fr;
            gap: 20px;
            max-width: 400px;
          }
          
          .pricing-card.featured {
            transform: none;
          }
          
          .pricing-card.featured:hover {
            transform: translateY(-4px);
          }
        }

        @media (max-width: 640px) {
          .pricing-title {
            font-size: 32px;
          }
          
          .pricing-card {
            padding: 30px 20px;
          }
        }
      `}</style>
      <div className="container">
        <div className="pricing-header">
          <div className="pricing-label">Pricing</div>
          <h1 className="pricing-title">
            Choose the Perfect<br />Plan for Your Business
          </h1>
          <p className="pricing-subtitle">
            Whether you're just starting or scaling up, find the plan that fits your needs and helps you achieve your business goals.
          </p>
        </div>

        <div className="pricing-cards">
          {/* Free Plan */}
          <div className="pricing-card">
            <h3 className="plan-name">Free</h3>
            <div className="plan-price">
              <span className="currency">LKR</span>0<span className="period">/Day</span>
            </div>
            <p className="plan-description">Perfect for startups or individuals just getting started.</p>
            
            <div className="features-title">Free Plan includes:</div>
            <ul className="features-list">
              <li>Access to basic features</li>
              <li>Up to 10 Requests</li>
              <li>Include 2 Agents</li>
              <li>Community support</li>
              <li>Free Security</li>
            </ul>
          </div>

          {/* Pro Plan (Featured) */}
          <div className="pricing-card featured">
            <h3 className="plan-name">Pro</h3>
            <div className="plan-price">
              <span className="currency">LKR</span>3999<span className="period">/month</span>
            </div>
            <p className="plan-description">Great plan for growing store that want the best features.</p>
            
            <div className="features-title">All free plan features, plus:</div>
            <ul className="features-list">
              <li>Advanced features</li>
              <li>Include 3 Agents</li>
              <li>Advanced AI capabilities</li>
              <li>Priority Support</li>
              <li>Secure Privacy</li>
            </ul>
          </div>

          {/* Team Plan */}
          <div className="pricing-card">
            <h3 className="plan-name">Team</h3>
            <div className="plan-price">
              <span className="currency">LKR</span>6999<span className="period">/month</span>
            </div>
            <p className="plan-description">Designed for large stors that need advanced tools.</p>
            
            <div className="features-title">All Pro plan features, plus:</div>
            <ul className="features-list">
              <li>Everything in Pro</li>
              <li>All AI Agents</li>
              <li>Unlimited automations</li>
              <li>Premium integrations</li>
              <li>Priority support</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
};

export default PricingComponent;