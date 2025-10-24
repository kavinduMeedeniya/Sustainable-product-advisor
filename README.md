# Sustainable-Product-Advisor
Sustainable Product Advisor

The Sustainable Product Advisor is a multi-agent AI system designed to assist users in making environmentally conscious shopping decisions. It enables users to:

	* Discover eco-friendly alternatives to products
	* Analyze the environmental impact through Eco Scores
	* Receive recycling and reuse suggestions

The system is built with four agents:

	Recommendation Agent – Orchestrates the workflow and integrates results.

	Product Info Agent – Fetches detailed product information from external websites.

	Eco Score Calculator Agent – Evaluates the sustainability of products and assigns eco scores.

	Recycling Agent – Suggests recycling, reuse, or disposal methods.

	
System Architecture Diagram


![System Diagram](https://i.postimg.cc/02B6tQvc/System-Diagram-2.png)


System Workflow Explanation

Users interact through a web or app interface.

	The Recommendation Agent serves as the central hub, receiving queries and coordinating with other agents.

	The Product Info Agent retrieves product details from websites such as Patagonia and H&M.

	The Eco Score Calculator Agent analyzes a product's sustainability based on its materials and production practices, then assigns an eco score.

	The Recycling Agent recommends recycling and disposal methods from government and brand-specific recycling programs.

	The Recommendation Agent integrates all results and recommends alternative products, and presents a structured output to the user.


Responsible AI: The system ensures fairness, transparency, and privacy.

	Fairness     → Product recommendations are based on objective eco criteria (not brand bias).
	Transparency → A breakdown accompanies eco score
	Privacy      → No personal data is collected.

Communication Flow:
User → Recommendation Agent → Product Info Agent → Eco Score Calculator Agent → Recycling Agent → Recommendation Agent → User
