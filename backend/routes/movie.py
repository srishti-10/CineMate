from fastapi import APIRouter, HTTPException
from db.mongo import get_mongo_client
from typing import List, Optional
import random

router = APIRouter()

@router.get("/test-movie-route")
def test_movie_route():
    """
    Simple test to verify the route is working.
    """
    return {"message": "Test movie route is working", "status": "success"}

@router.get("/movies/test")
def test_movies_route():
    """
    Simple test to verify the route is working.
    """
    return {"message": "Movies route is working", "status": "success"}

@router.get("/movies/simple")
def simple_movies():
    """
    Very simple movies endpoint.
    """
    return {"message": "Simple movies endpoint", "movies": []}

@router.get("/movies/count")
def get_movie_count():
    """
    Get the total number of movies in the database.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        count = movies.count_documents({})
        return {"total_movies": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/search/{title}")
def search_movies(title: str, limit: Optional[int] = 10):
    """
    Search movies by title.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Case-insensitive search
        movie_cursor = movies.find(
            {"title": {"$regex": title, "$options": "i"}}
        ).limit(limit)
        
        movie_list = []
        for movie in movie_cursor:
            movie["_id"] = str(movie["_id"])
            movie_list.append(movie)
        
        return {
            "movies": movie_list,
            "search_term": title,
            "count": len(movie_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/")
def list_movies(limit: Optional[int] = 10, skip: Optional[int] = 0):
    """
    List movies from the database with pagination.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Get movies with pagination
        movie_cursor = movies.find().skip(skip).limit(limit)
        
        movie_list = []
        for movie in movie_cursor:
            movie["_id"] = str(movie["_id"])  # Convert ObjectId to string
            movie_list.append(movie)
        
        # Get total count for pagination info
        total_count = movies.count_documents({})
        
        return {
            "movies": movie_list,
            "total": total_count,
            "limit": limit,
            "skip": skip,
            "has_more": (skip + limit) < total_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/{movie_id}")
def get_movie(movie_id: str):
    """
    Get a specific movie by ID.
    """
    try:
        from bson import ObjectId
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        movie = movies.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie["_id"] = str(movie["_id"])
        return movie
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# NEW RECOMMENDATION ENDPOINTS

@router.get("/movies/recommendations/popular")
def get_popular_movies(limit: Optional[int] = 10):
    """
    Get popular movies based on rating and number of reviews.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Get movies with high ratings and many reviews
        pipeline = [
            {"$match": {"num_reviews": {"$gte": 100}}},  # At least 100 reviews
            {"$sort": {"avg_rating": -1, "num_reviews": -1}},
            {"$limit": limit}
        ]
        
        movie_cursor = movies.aggregate(pipeline)
        movie_list = []
        for movie in movie_cursor:
            movie["_id"] = str(movie["_id"])
            movie_list.append(movie)
        
        return {
            "movies": movie_list,
            "recommendation_type": "popular",
            "count": len(movie_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/recommendations/genre/{genre}")
def get_movies_by_genre(genre: str, limit: Optional[int] = 10):
    """
    Get movies by specific genre.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Case-insensitive genre search
        movie_cursor = movies.find(
            {"genres": {"$regex": genre, "$options": "i"}}
        ).sort("avg_rating", -1).limit(limit)
        
        movie_list = []
        for movie in movie_cursor:
            movie["_id"] = str(movie["_id"])
            movie_list.append(movie)
        
        return {
            "movies": movie_list,
            "genre": genre,
            "count": len(movie_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/recommendations/similar/{movie_id}")
def get_similar_movies(movie_id: str, limit: Optional[int] = 5):
    """
    Get similar movies based on genres and rating.
    """
    try:
        from bson import ObjectId
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Get the target movie
        target_movie = movies.find_one({"_id": ObjectId(movie_id)})
        if not target_movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        target_genres = target_movie.get("genres", [])
        target_rating = target_movie.get("avg_rating", 0)
        
        # Find movies with similar genres and rating (simplified approach)
        similar_movies = movies.find({
            "_id": {"$ne": ObjectId(movie_id)},  # Exclude the target movie
            "genres": {"$in": target_genres},  # Share at least one genre
            "avg_rating": {"$gte": max(0, target_rating - 1), "$lte": target_rating + 1}  # Similar rating
        }).sort("avg_rating", -1).limit(limit)
        
        movie_list = []
        for movie in similar_movies:
            movie["_id"] = str(movie["_id"])
            movie_list.append(movie)
        
        return {
            "movies": movie_list,
            "target_movie": target_movie.get("title", "Unknown"),
            "count": len(movie_list)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/recommendations/random")
def get_random_movies(limit: Optional[int] = 10):
    """
    Get random movies for discovery.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Get total count for random sampling
        total_count = movies.count_documents({})
        
        # Get random movies using a simpler approach
        movie_list = []
        if total_count > 0:
            # Get all movies and randomly sample
            all_movies = list(movies.find())
            import random
            random.shuffle(all_movies)
            
            for movie in all_movies[:limit]:
                movie["_id"] = str(movie["_id"])
                movie_list.append(movie)
        
        return {
            "movies": movie_list,
            "recommendation_type": "random",
            "count": len(movie_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/genres/list")
def get_all_genres():
    """
    Get all available genres in the database.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Get all unique genres using a simpler approach
        all_movies = movies.find({}, {"genres": 1})
        all_genres = set()
        
        for movie in all_movies:
            if movie.get("genres"):
                all_genres.update(movie["genres"])
        
        genres_list = sorted(list(all_genres))
        
        return {
            "genres": genres_list,
            "count": len(genres_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Add these new aggregation endpoints after the existing routes

@router.get("/movies/analytics/genre-stats")
def get_genre_statistics():
    """
    MongoDB Aggregation Query 1: Get statistics by genre.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        pipeline = [
            {"$unwind": "$genres"},
            {"$group": {
                "_id": "$genres",
                "count": {"$sum": 1},
                "avg_rating": {"$avg": "$avg_rating"},
                "total_reviews": {"$sum": "$num_reviews"},
                "avg_budget": {"$avg": "$budget"},
                "avg_revenue": {"$avg": "$revenue"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        results = list(movies.aggregate(pipeline))
        
        return {
            "genre_statistics": results,
            "total_genres": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/analytics/yearly-trends")
def get_yearly_trends():
    """
    MongoDB Aggregation Query 2: Get movie trends by year.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        pipeline = [
            {"$match": {"year": {"$gte": 1990, "$lte": 2020}}},
            {"$group": {
                "_id": "$year",
                "movie_count": {"$sum": 1},
                "avg_rating": {"$avg": "$avg_rating"},
                "total_budget": {"$sum": "$budget"},
                "total_revenue": {"$sum": "$revenue"},
                "avg_runtime": {"$avg": "$runtime"}
            }},
            {"$sort": {"_id": 1}},
            {"$limit": 20}
        ]
        
        results = list(movies.aggregate(pipeline))
        
        return {
            "yearly_trends": results,
            "years_analyzed": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/movies/analytics/top-rated")
def get_top_rated_movies_by_decade():
    """
    MongoDB Aggregation Query 3: Get top-rated movies by decade.
    """
    try:
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        pipeline = [
            {"$match": {"year": {"$gte": 1990, "$lte": 2020}}},
            {"$addFields": {
                "decade": {
                    "$concat": [
                        {"$toString": {"$floor": {"$divide": ["$year", 10]}}},
                        "0s"
                    ]
                }
            }},
            {"$group": {
                "_id": "$decade",
                "top_movies": {
                    "$push": {
                        "title": "$title",
                        "year": "$year",
                        "avg_rating": "$avg_rating",
                        "num_reviews": "$num_reviews"
                    }
                }
            }},
            {"$addFields": {
                "top_movies": {
                    "$slice": [
                        {"$sortArray": {
                            "input": "$top_movies",
                            "sortBy": {"avg_rating": -1}
                        }},
                        5
                    ]
                }
            }}
        ]
        
        results = list(movies.aggregate(pipeline))
        
        return {
            "top_rated_by_decade": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 