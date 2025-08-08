# 🚀 Dynamic Pricing Engine

A sophisticated real-time pricing optimization system that helps businesses maximize revenue through intelligent pricing strategies based on demand, inventory, competition, and customer segments.

## ✨ Features

- **Real-time Price Calculation**: Dynamic pricing based on multiple factors
- **Multiple Pricing Strategies**: Default, Aggressive, and Conservative approaches
- **Customer Segmentation**: Premium, Standard, Budget, and Loyalty pricing tiers
- **Competitor Price Monitoring**: Track and respond to competitor pricing
- **Analytics Dashboard**: Visual insights into pricing performance
- **Interactive Charts**: Real-time price trends and competitor comparison
- **Responsive Design**: Works seamlessly across all devices
- **RESTful API**: Backend API with FastAPI for scalability

## 🛠 Tech Stack

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern gradients and animations
- **Vanilla JavaScript** (ES6+)
- **Chart.js** for data visualization
- **Inter Font** from Google Fonts

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd dynamic-pricing-engine
```

### 2. Install Backend Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. Start the Backend Server
```bash
python main.py
```
The API will be available at `http://localhost:8000`

### 4. Open the Frontend
Open `index.html` in your web browser, or serve it using a local server:
```bash
# Using Python's built-in server
python -m http.server 3000
```
Then visit `http://localhost:3000`

## 🔧 Configuration

### Database
The system uses SQLite by default. The database file (`pricing.db`) will be created automatically on first run.

### API Endpoints
- `POST /calculate-price` - Calculate dynamic price
- `GET /analytics/pricing-performance` - Get pricing analytics
- `POST /competitor-prices/update` - Update competitor prices
- `GET /health` - Health check endpoint

## 📊 How It Works

### Pricing Factors

1. **Demand Score (1-10)**: Higher demand = higher prices
2. **Inventory Levels**: Low stock = price increase
3. **Competitor Pricing**: Automatic competitive positioning
4. **Customer Segments**: 
   - Premium: +20% markup
   - Standard: Base pricing
   - Budget: -15% discount
   - Loyalty: -10% discount
5. **Seasonality Factor**: Seasonal price adjustments (0.5x - 2.0x)

### Pricing Strategies

#### Default Strategy
- Balanced approach considering all factors
- Safe price boundaries (10% above cost, 20% below competitor max)
- Suitable for most products

#### Aggressive Strategy
- Higher base markup (+10%)
- Maximizes profit margins
- Best for unique or high-demand products

#### Conservative Strategy
- Lower base markup (-5%)
- Focus on market penetration
- Ideal for competitive markets

## 🎯 Usage Examples

### Basic Price Calculation
```javascript
const pricingData = {
  product_id: "PROD-001",
  cost_price: 25.00,
  demand_score: 7,
  inventory: 50,
  competitor_price: 45.00,
  customer_segment: "premium",
  seasonality_factor: 1.2
};

fetch('http://localhost:8000/calculate-price', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(pricingData)
})
.then(response => response.json())
.then(data => console.log('Optimal Price:', data.dynamic_price));
```

### Get Analytics
```javascript
fetch('http://localhost:8000/analytics/pricing-performance?days=30')
  .then(response => response.json())
  .then(data => {
    console.log('Revenue Impact:', data.metrics.revenue_impact);
    console.log('Conversion Rate:', data.metrics.conversion_rate);
  });
```

## 📱 User Interface

### Price Calculator
- **Product ID**: Unique identifier for the product
- **Cost Price**: Base cost of the product
- **Demand Score**: Market demand rating (1-10 slider)
- **Inventory**: Current stock levels
- **Competitor Price**: Reference competitor pricing
- **Customer Segment**: Target customer category
- **Seasonality Factor**: Seasonal adjustment multiplier

### Analytics Dashboard
- **Revenue Impact**: Total revenue generated
- **Conversion Rate**: Success rate of pricing strategy
- **Average Price Change**: Pricing volatility metrics
- **Competitor Gap**: Price difference analysis
- **Price Trend Chart**: Historical price visualization

## 🔒 API Security

The API includes CORS middleware for cross-origin requests. For production use, consider adding:
- Authentication and authorization
- Rate limiting
- Input validation and sanitization
- HTTPS encryption

## 🛡 Error Handling

The system includes comprehensive error handling:
- Form validation on the frontend
- API error responses with detailed messages
- Database connection error handling
- Graceful fallbacks for missing data

## 📈 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Analytics data cached for 30 seconds
- **Efficient Charts**: Chart.js with optimized rendering
- **Responsive Design**: Mobile-first approach

## 🧪 Testing

### Manual Testing
1. Fill out the pricing form with test data
2. Verify price calculation results
3. Check analytics dashboard updates
4. Test different customer segments and strategies

### API Testing
Use tools like Postman or curl to test the API endpoints:
```bash
curl -X POST "http://localhost:8000/calculate-price" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "TEST-001",
    "cost_price": 30.00,
    "demand_score": 5,
    "inventory": 100,
    "competitor_price": 50.00
  }'
```

## 🔄 Database Schema

### PricingHistory Table
- `id`: Primary key
- `product_id`: Product identifier
- `timestamp`: Calculation timestamp
- `original_price`: Base price before adjustments
- `dynamic_price`: Final calculated price
- `demand_score`: Demand rating used
- `inventory`: Stock level at calculation time
- `competitor_price`: Reference competitor price
- `strategy_used`: Pricing strategy applied

### CompetitorPrice Table
- `id`: Primary key
- `product_id`: Product identifier
- `competitor_name`: Competitor identifier
- `price`: Competitor's price
- `timestamp`: Price update timestamp
- `is_active`: Price validity flag

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, consider:
- Using PostgreSQL instead of SQLite
- Adding environment variables for configuration
- Implementing proper logging
- Setting up monitoring and health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Open an issue in the repository
- Check the [API documentation](http://localhost:8000/docs) when running
- Review the code comments for implementation details

## 🔄 Version History

- **v2.1**: Current version with analytics dashboard
- **v2.0**: Added customer segmentation and pricing strategies
- **v1.0**: Initial release with basic pricing calculation



---

**Made with ❤️ for intelligent pricing optimization**
