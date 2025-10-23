import React from 'react';

const ProductResponse = ({ data }) => {
  const { product_info, eco_score, recycling_options, recommendation } = data;

  return (
    <div>
      <div className="product-section">
        <div className="product-title">Product Info</div>
        <p>Name: {product_info.name}</p>
        <p>Brand: {product_info.brand}</p>
        <p>Materials:</p>
        <ul className="product-list">
          {product_info.materials.map((material, index) => (
            <li key={index}>{material}</li>
          ))}
        </ul>
        <p>Description: {product_info.description}</p>
        <p>URL: <a href={product_info.url} className="product-link" target="_blank" rel="noopener noreferrer">{product_info.url}</a></p>
      </div>

      <div className="product-section">
        <div className="product-title">Eco Score</div>
        <p>Score: {eco_score.score}/100</p>
        <p>Reason: {eco_score.reason}</p>
      </div>

      <div className="product-section">
        <div className="product-title">Recycling Options</div>
        <ul className="product-list">
          {recycling_options.options.map((option, index) => (
            <li key={index}>{option}</li>
          ))}
        </ul>
      </div>

      <div className="product-section">
        <div className="product-title">Recommendation</div>
        <p>Recommended Product: {recommendation.recommended_product}</p>
        <p>Reason: {recommendation.reason}</p>
        <p>URL: <a href={recommendation.url} className="product-link" target="_blank" rel="noopener noreferrer">{recommendation.url}</a></p>
      </div>
    </div>
  );
};

export default ProductResponse;