const BASE_URL = 'http://localhost:8000'; // Adjust to your backend URL

const api = {
  chat: async (message) => {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error('Chat request failed');
    return response.json();
  },
  productInfo: async (query) => {
    const response = await fetch(`${BASE_URL}/product-info`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(query),
    });
    if (!response.ok) throw new Error('Product info request failed');
    const data = await response.json();
    const ecoScore = await api.ecoScore(data);
    const recyclingOptions = await api.recyclingOptions(data);
    const recommendation = await api.recommendation(data, ecoScore, recyclingOptions);
    return { product_info: data, eco_score: ecoScore, recycling_options: recyclingOptions, recommendation };
  },
  ecoScore: async (productInfo) => {
    const response = await fetch(`${BASE_URL}/eco-score`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productInfo),
    });
    if (!response.ok) throw new Error('Eco score request failed');
    return response.json();
  },
  recyclingOptions: async (productInfo) => {
    const response = await fetch(`${BASE_URL}/recycling-options`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productInfo),
    });
    if (!response.ok) throw new Error('Recycling options request failed');
    return response.json();
  },
  recommendation: async (productInfo, ecoScore, recyclingOptions) => {
    const response = await fetch(`${BASE_URL}/recommendation`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...productInfo, eco_score: ecoScore, recycling_options: recyclingOptions }),
    });
    if (!response.ok) throw new Error('Recommendation request failed');
    return response.json();
  },
};

export default api;