import React, { useEffect, useRef } from 'react';
import './ProFeaturesDashboard.css';

const ProFeaturesDashboard = () => {
  const statCardsRef = useRef([]);

  // Animation function for number counting
  const animateNumbers = () => {
    const numbers = document.querySelectorAll('.snd-pro-features-stat-number');
    
    numbers.forEach((number, index) => {
      const target = parseInt(number.textContent);
      const increment = target / 100;
      let current = 0;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        number.textContent = Math.floor(current) + '%';
      }, 20);
    });
  };

  useEffect(() => {
    // Trigger number animation when component mounts
    const timer = setTimeout(animateNumbers, 800);

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
        }
      });
    }, { threshold: 0.1 });

    // Observe all stat cards
    statCardsRef.current.forEach(card => {
      if (card) observer.observe(card);
    });

    // Cleanup function
    return () => {
      clearTimeout(timer);
      statCardsRef.current.forEach(card => {
        if (card) observer.unobserve(card);
      });
    };
  }, []);

  // Stats data for easier management
  const statsData = [
    {
      id: 1,
      percentage: "95%",
      label: "Faster ESG data processing with automated analysis"
    },
    {
      id: 2,
      percentage: "78%",
      label: "Increase in client satisfaction through detailed sustainability reports"
    },
    {
      id: 3,
      percentage: "60%",
      label: "Time saved on compliance documentation"
    }
  ];

  return (
    <div className="snd-pro-features-dashboard">
      <div className="snd-pro-features-container">
        <div className="snd-pro-features-left-section">
          <h1 className="snd-pro-features-main-title">
            Pro<br />features
          </h1>
          <p className="snd-pro-features-description">
            Advanced sustainability analysis tools designed for professional advisers. 
            Access comprehensive ESG data, automated reporting, and real-time environmental 
            impact tracking to deliver exceptional value to your clients.
          </p>
          <p className="snd-pro-features-source-note">
            Key benefits of upgrading to Sustainable Product Adviser Pro
          </p>
        </div>

        <div className="snd-pro-features-stats-grid">
          {statsData.map((stat, index) => (
            <div 
              key={stat.id}
              ref={el => statCardsRef.current[index] = el}
              className="snd-pro-features-stat-card"
            >
              <span className="snd-pro-features-stat-number">{stat.percentage}</span>
              <div className="snd-pro-features-stat-label">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProFeaturesDashboard;