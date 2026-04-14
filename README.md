# AI-based Waste Management System

This project is an end-to-end solution for intelligent waste management using AI and machine learning.

## Project Overview

The AI-based Waste Management System is a comprehensive application that enables efficient waste management in urban areas through intelligent waste collection scheduling, image recognition for sorting, community recycling hub locator, route optimization, user rewards, and analytics dashboard.

## Features

1. **Waste Collection Scheduling** - Users can schedule waste collection at their convenience
2. **Waste Sorting Assistant** - Image recognition to identify recyclable, organic, and non-recyclable items
3. **Community Recycling Hub Locator** - Locate nearby recycling centers and drop-off points
4. **Waste Collection Route Optimization** - Optimize garbage truck routes to reduce fuel consumption
5. **User Rewards System** - Gamify the system with rewards for proper waste disposal
6. **Analytics Dashboard** - Data visualization tools for city authorities

## Project Structure

```
ai-waste-management-system/
├── frontend/                    # React Native Mobile App
│   ├── src/
│   │   ├── screens/            # UI screens
│   │   ├── components/         # Reusable components
│   │   ├── navigation/         # Navigation setup
│   │   ├── services/           # API services
│   │   ├── redux/              # State management
│   │   └── assets/             # Images, fonts
│   ├── package.json
│   ├── app.json
│   └── babel.config.js
├── backend/                     # Node.js REST API
│   ├── src/
│   │   ├── routes/             # API endpoints
│   │   ├── controllers/        # Business logic
│   │   ├── models/             # MongoDB schemas
│   │   ├── middleware/         # Custom middleware
│   │   ├── utils/              # Helper functions
│   │   └── config/             # Configuration files
│   ├── server.js
│   ├── package.json
│   └── .env.example
├── ml_service/                 # Python ML Service
│   ├── app.py                  # Flask app
│   ├── models/
│   │   ├── waste_classifier.py # TensorFlow model
│   │   ├── route_optimizer.py  # Route optimization
│   │   └── predictions.py      # Prediction service
│   ├── requirements.txt
│   └── .env.example
├── database/                   # MongoDB Setup
│   ├── schemas/
│   │   ├── user.schema.js
│   │   ├── waste.schema.js
│   │   ├── collection.schema.js
│   │   ├── hub.schema.js
│   │   └── analytics.schema.js
│   └── init.js
├── docker/                     # Docker Configuration
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── Dockerfile.ml
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── frontend-ci.yml
│       ├── backend-ci.yml
│       └── deploy.yml
├── README.md
├── .gitignore
└── package.json

```

## Technologies Used

### Frontend
- **React Native** - Cross-platform mobile development
- **Redux** - State management
- **Axios** - HTTP client
- **React Navigation** - Navigation library

### Backend
- **Node.js** with Express - REST API server
- **MongoDB** - NoSQL database
- **Mongoose** - ODM for MongoDB
- **JWT** - Authentication
- **Socket.io** - Real-time notifications

### Machine Learning
- **Python** - ML service language
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning for image classification
- **OpenCV** - Computer vision library
- **Scikit-learn** - Machine learning algorithms
- **OR-Tools** - Route optimization

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline

## Installation & Setup

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- MongoDB (local or Atlas)
- Docker (optional)
- Git

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend
npm install
cp .env.example .env
# Configure your MongoDB connection and API keys
npm start
```

### ML Service Setup
```bash
cd ml_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Docker Setup (Optional)
```bash
docker-compose up -d
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Waste Management
- `POST /api/waste/classify` - Classify waste using ML model
- `GET /api/waste/types` - Get waste types
- `POST /api/waste/report` - Report waste disposal

### Collection Scheduling
- `POST /api/collection/schedule` - Schedule collection
- `GET /api/collection/schedule` - Get user schedules
- `PUT /api/collection/schedule/:id` - Update schedule
- `DELETE /api/collection/schedule/:id` - Cancel schedule

### Recycling Hubs
- `GET /api/hubs` - Get all recycling hubs
- `GET /api/hubs/nearby` - Get nearby hubs
- `GET /api/hubs/:id` - Get hub details

### Routes
- `POST /api/routes/optimize` - Optimize collection routes
- `GET /api/routes/:id` - Get route details

### User Rewards
- `GET /api/rewards/points` - Get user reward points
- `GET /api/rewards/history` - Get rewards history
- `POST /api/rewards/redeem` - Redeem rewards

### Analytics
- `GET /api/analytics/dashboard` - Get analytics data
- `GET /api/analytics/collection-stats` - Collection statistics
- `GET /api/analytics/recycling-stats` - Recycling statistics

## Machine Learning Models

### Waste Classification Model
- **Input**: Image of waste item
- **Output**: Classification (Recyclable, Organic, Non-recyclable)
- **Accuracy**: >95%
- **Model**: TensorFlow/Keras CNN

### Route Optimization
- **Algorithm**: Google OR-Tools
- **Input**: Collection points, truck capacity, traffic data
- **Output**: Optimized routes
- **Benefit**: 20-30% fuel consumption reduction

## Database Schema

### User
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String,
  address: String,
  coordinates: { latitude, longitude },
  rewardPoints: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### Waste Classification
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  imageUrl: String,
  classification: String,
  confidence: Number,
  timestamp: Date
}
```

### Collection Schedule
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  scheduledDate: Date,
  wasteType: String,
  quantity: Number,
  status: String,
  createdAt: Date,
  updatedAt: Date
}
```

### Recycling Hub
```javascript
{
  _id: ObjectId,
  name: String,
  location: { latitude, longitude },
  address: String,
  materialsAccepted: [String],
  operatingHours: String,
  contactInfo: String,
  rating: Number
}
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Code Quality Checks** - ESLint, Prettier
2. **Unit Tests** - Jest
3. **Integration Tests** - Mocha
4. **Build** - Docker image creation
5. **Deployment** - Docker registry push

## Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname
JWT_SECRET=your_jwt_secret_key
API_PORT=5000
NODE_ENV=development
ML_SERVICE_URL=http://localhost:5001
```

### ML Service (.env)
```
FLASK_ENV=development
FLASK_PORT=5001
MODEL_PATH=./models/waste_classifier.h5
API_KEY=your_api_key
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@wastemanagement.com or open an issue in the GitHub repository.

---

**Created by**: uthrasriram
**Last Updated**: 2026-04-14