from fastapi import FastAPI

# Import routes with error handling
try:
    from routes.user import router as user_router
    print("✅ User routes imported successfully")
except Exception as e:
    print(f"❌ Error importing user routes: {e}")
    user_router = None

try:
    from routes.movie import router as movie_router
    print("✅ Movie routes imported successfully")
except Exception as e:
    print(f"❌ Error importing movie routes: {e}")
    movie_router = None

try:
    from routes.review import router as review_router
    print("✅ Review routes imported successfully")
except Exception as e:
    print(f"❌ Error importing review routes: {e}")
    review_router = None

try:
    from routes.graph import router as graph_router
    print("✅ Graph routes imported successfully")
except Exception as e:
    print(f"❌ Error importing graph routes: {e}")
    graph_router = None

app = FastAPI(
    title="CineMate API",
    description="A comprehensive movie recommendation system using MongoDB, Redis, and Neo4j",
    version="1.0.0"
)

# Include routers only if they were imported successfully
if user_router:
    app.include_router(user_router)
    print("✅ User router included")

if movie_router:
    app.include_router(movie_router)
    print("✅ Movie router included")

if review_router:
    app.include_router(review_router)
    print("✅ Review router included")

if graph_router:
    app.include_router(graph_router)
    print("✅ Graph router included")

@app.get("/")
def root():
    return {
        "message": "Welcome to CineMate API!",
        "description": "Multi-database movie recommendation system",
        "databases": ["MongoDB", "Redis", "Neo4j"],
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "movies": "/movies/",
            "reviews": "/reviews/",
            "users": "/users/",
            "graph": "/graph/"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "CineMate API is running"}

@app.get("/test-movies")
def test_movies():
    """
    Simple test endpoint to check if we can access movies.
    """
    try:
        from db.mongo import get_mongo_client
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Just get the count
        count = movies.count_documents({})
        return {"message": "Database connection works", "movie_count": count}
        
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__} 