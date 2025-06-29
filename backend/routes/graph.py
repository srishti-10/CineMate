from fastapi import APIRouter, HTTPException
from db.neo4j import neo4j_graph
from typing import List, Optional

router = APIRouter()

@router.get("/graph/similar/{movie_id}")
def get_similar_movies_graph(movie_id: int, limit: Optional[int] = 5):
    """
    Get similar movies using Neo4j graph queries.
    """
    try:
        results = neo4j_graph.get_similar_movies_graph(movie_id, limit)
        return {
            "similar_movies": results,
            "movie_id": movie_id,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph query error: {str(e)}")

@router.get("/graph/recommendations/{user_id}")
def get_user_recommendations_graph(user_id: str, limit: Optional[int] = 5):
    """
    Get personalized movie recommendations for a user using Neo4j.
    """
    try:
        results = neo4j_graph.get_movie_recommendations_for_user(user_id, limit)
        return {
            "recommendations": results,
            "user_id": user_id,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph query error: {str(e)}")

@router.get("/graph/popular-genres")
def get_popular_genres_graph(limit: Optional[int] = 10):
    """
    Get popular genres analysis using Neo4j graph queries.
    """
    try:
        results = neo4j_graph.get_popular_genres(limit)
        return {
            "popular_genres": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph query error: {str(e)}")

@router.get("/graph/shortest-path/{movie1_id}/{movie2_id}")
def get_shortest_path(movie1_id: int, movie2_id: int):
    """
    Find shortest path between two movies through genres.
    """
    try:
        results = neo4j_graph.get_shortest_path_between_movies(movie1_id, movie2_id)
        return {
            "shortest_path": results,
            "movie1_id": movie1_id,
            "movie2_id": movie2_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph query error: {str(e)}")

@router.post("/graph/user/{user_id}")
def create_user_node(user_id: str, username: str):
    """
    Create a user node in Neo4j graph.
    """
    try:
        neo4j_graph.create_user_node(user_id, username)
        return {"message": f"User {username} created successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph operation error: {str(e)}")

@router.post("/graph/rating/{user_id}/{movie_id}")
def create_user_rating(user_id: str, movie_id: int, rating: float):
    """
    Create a user rating relationship in Neo4j.
    """
    try:
        neo4j_graph.create_user_rating(user_id, movie_id, rating)
        return {
            "message": "Rating created successfully",
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph operation error: {str(e)}")

@router.post("/graph/movie/{movie_id}")
def create_movie_node(movie_data: dict):
    """
    Create a movie node in Neo4j graph.
    """
    try:
        neo4j_graph.create_movie_node(movie_data)
        return {"message": "Movie node created successfully", "movie_id": movie_data.get('tmdb_id')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph operation error: {str(e)}")

@router.post("/graph/movie/{movie_id}/genres")
def create_movie_genre_relationships(movie_id: int, genres: List[str]):
    """
    Create genre relationships for a movie.
    """
    try:
        neo4j_graph.create_genre_relationships(movie_id, genres)
        return {
            "message": "Genre relationships created successfully",
            "movie_id": movie_id,
            "genres": genres
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph operation error: {str(e)}") 