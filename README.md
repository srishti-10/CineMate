# CineMate - Multi-Database Movie Recommendation System

A comprehensive movie recommendation system that integrates three NoSQL databases: **MongoDB**, **Redis**, and **Neo4j** to demonstrate different database paradigms in a real-world application.

## 🎬 Features

- **Movie Database**: Browse and search through 4800+ movies
- **Smart Recommendations**: AI-powered movie suggestions
- **User Authentication**: Secure user registration and login
- **Real-time Analytics**: Movie trends and statistics
- **Social Features**: User ratings and reviews
- **Performance Optimization**: Redis caching for fast responses
- **Graph-based Recommendations**: Neo4j-powered relationship analysis

## 🏗️ Architecture

### Database Integration

#### 🔷 MongoDB (Document Database)
- **Purpose**: Core application data storage
- **Data**: Movies, users, reviews, ratings
- **Features**: 
  - Complex aggregation queries for analytics
  - Full-text search capabilities
  - Flexible schema for movie metadata

#### 🔶 Redis (Key-Value Store)
- **Purpose**: Caching and session management
- **Features**:
  - Movie data caching (30-minute TTL)
  - User session storage (2-hour TTL)
  - Search result caching (30-minute TTL)
  - Popular movies caching (1-hour TTL)

#### 🔷 Neo4j (Graph Database)
- **Purpose**: Graph-based recommendations and relationships
- **Features**:
  - Movie similarity based on shared genres
  - User recommendation paths
  - Genre popularity analysis
  - Shortest path between movies

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local development)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CineMate
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Neo4j Browser: http://localhost:7474

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   pip install -r requirements.txt
   ```

2. **Start databases**
   ```bash
   docker-compose up mongodb redis neo4j -d
   ```

3. **Run the application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python start_server.py
   
   # Terminal 2 - Frontend
   cd frontend
   streamlit run app.py
   ```

## 📊 Database Queries Examples

### MongoDB Aggregation Queries

#### 1. Genre Statistics
```javascript
db.movies.aggregate([
  { $unwind: "$genres" },
  { $group: {
    _id: "$genres",
    count: { $sum: 1 },
    avg_rating: { $avg: "$avg_rating" },
    total_reviews: { $sum: "$num_reviews" }
  }},
  { $sort: { count: -1 } }
])
```

#### 2. Yearly Trends
```javascript
db.movies.aggregate([
  { $match: { year: { $gte: 1990, $lte: 2020 } } },
  { $group: {
    _id: "$year",
    movie_count: { $sum: 1 },
    avg_rating: { $avg: "$avg_rating" }
  }},
  { $sort: { _id: 1 } }
])
```

### Redis Caching Examples

```python
# Cache movie data
redis_cache.cache_movie_data(movie_id, movie_data, expire=1800)

# Get cached movie
cached_movie = redis_cache.get_cached_movie(movie_id)

# Cache search results
redis_cache.cache_search_results(query, results, expire=1800)
```

### Neo4j Graph Queries

#### 1. Similar Movies
```cypher
MATCH (m1:Movie {id: $movie_id})-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(m2:Movie)
WHERE m1 <> m2
WITH m2, count(g) as shared_genres, m2.avg_rating as rating
ORDER BY shared_genres DESC, rating DESC
LIMIT 5
RETURN m2.title as title, shared_genres, rating
```

#### 2. User Recommendations
```cypher
MATCH (u:User {id: $user_id})-[r:RATED]->(m1:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(m2:Movie)
WHERE r.rating >= 4.0 AND NOT (u)-[:RATED]->(m2)
WITH m2, count(g) as genre_matches, avg(r.rating) as avg_user_rating
ORDER BY genre_matches DESC, avg_user_rating DESC
LIMIT 5
RETURN m2.title as title, genre_matches
```

## 🔧 API Endpoints

### Movies
- `GET /movies/` - List movies with pagination
- `GET /movies/{movie_id}` - Get specific movie
- `GET /movies/search/{title}` - Search movies
- `GET /movies/count` - Get total movie count

### Recommendations
- `GET /movies/recommendations/popular` - Popular movies
- `GET /movies/recommendations/genre/{genre}` - Genre-based recommendations
- `GET /movies/recommendations/similar/{movie_id}` - Similar movies
- `GET /movies/recommendations/random` - Random movies

### Analytics
- `GET /movies/analytics/genre-stats` - Genre statistics
- `GET /movies/analytics/yearly-trends` - Yearly trends
- `GET /movies/analytics/top-rated` - Top-rated by decade

### Graph Queries
- `GET /graph/similar/{movie_id}` - Graph-based similar movies
- `GET /graph/recommendations/{user_id}` - User recommendations
- `GET /graph/popular-genres` - Popular genres analysis

## 📁 Project Structure

```
CineMate/
├── backend/
│   ├── db/
│   │   ├── mongo.py          # MongoDB connection
│   │   ├── redis.py          # Redis caching
│   │   └── neo4j.py          # Neo4j graph database
│   ├── routes/
│   │   ├── movie.py          # Movie endpoints
│   │   ├── user.py           # User endpoints
│   │   └── review.py         # Review endpoints
│   ├── models/               # Data models
│   ├── main.py               # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── app.py                # Streamlit application
│   └── requirements.txt      # Frontend dependencies
├── datasets/                 # Movie data files
├── docker-compose.yml        # Docker services
└── README.md                 # Project documentation
```

## 🧪 Testing

### Test API Endpoints
```bash
cd backend
python test_recommendations.py
python test_fixed_api.py
```

### Test Database Connections
```bash
cd backend
python -c "from db.mongo import get_mongo_client; print('MongoDB: OK')"
python -c "from db.redis import redis_cache; print('Redis: OK')"
python -c "from db.neo4j import neo4j_graph; print('Neo4j: OK')"
```

## 🔍 Performance Optimization

### Redis Caching Strategy
- **Movie Data**: 30-minute TTL for frequently accessed movies
- **Search Results**: 30-minute TTL for repeated searches
- **Popular Movies**: 1-hour TTL for trending content
- **User Sessions**: 2-hour TTL for active users

### MongoDB Indexing
- Index on `title` for search performance
- Index on `year` for temporal queries
- Index on `avg_rating` for recommendation queries
- Compound index on `genres` for genre-based filtering

### Neo4j Graph Optimization
- Index on Movie nodes for fast lookups
- Index on Genre nodes for relationship queries
- Relationship indexes for user ratings

## 🚀 Deployment

### Production Setup
1. Update environment variables in `docker-compose.yml`
2. Set up proper authentication for all databases
3. Configure SSL certificates
4. Set up monitoring and logging
5. Use production-grade Redis and MongoDB instances

### Environment Variables
```bash
# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Backend Development**: [Your Name]
- **Frontend Development**: [Your Name]
- **Database Design**: [Your Name]
- **DevOps & Deployment**: [Your Name]

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for NoSQL Applications Project** 