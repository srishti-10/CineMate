import pandas as pd
from db.mongo import get_mongo_client
import json
import ast
from datetime import datetime

def parse_json_column(json_str):
    """
    Parse JSON-like strings from CSV columns.
    """
    if pd.isna(json_str) or json_str == '':
        return []
    try:
        # Try to parse as literal string (for Python dict format)
        return ast.literal_eval(json_str)
    except:
        try:
            # Try to parse as JSON
            return json.loads(json_str)
        except:
            return []

def extract_genres(genres_str):
    """
    Extract genre names from the genres JSON string.
    """
    genres_list = parse_json_column(genres_str)
    if isinstance(genres_list, list):
        return [genre.get('name', '') for genre in genres_list if isinstance(genre, dict)]
    return []

def extract_year_from_date(date_str):
    """
    Extract year from release date string.
    """
    if pd.isna(date_str) or date_str == '':
        return 0
    try:
        return pd.to_datetime(date_str).year
    except:
        return 0

def load_movies_from_csv(csv_file_path):
    """
    Load movies from movies_metadata.csv into MongoDB.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Connect to MongoDB
        client = get_mongo_client()
        db = client["cinemate"]
        movies = db["movies"]
        
        # Convert DataFrame to list of dictionaries
        movies_data = []
        for _, row in df.iterrows():
            # Extract genres
            genres = extract_genres(row.get("genres", ""))
            
            # Extract year from release date
            year = extract_year_from_date(row.get("release_date", ""))
            
            movie = {
                "title": row.get("title", ""),
                "year": year,
                "genres": genres,
                "description": row.get("overview", ""),
                "director": "",  # Not available in this dataset
                "cast": [],      # Not available in this dataset
                "poster_url": "", # Not available in this dataset
                "avg_rating": float(row.get("vote_average", 0)),
                "num_reviews": int(row.get("vote_count", 0)),
                "tmdb_id": int(row.get("id", 0)),
                "popularity": float(row.get("popularity", 0)),
                "budget": int(row.get("budget", 0)),
                "revenue": int(row.get("revenue", 0)),
                "runtime": float(row.get("runtime", 0)) if pd.notna(row.get("runtime")) else 0,
                "tagline": row.get("tagline", "")
            }
            movies_data.append(movie)
        
        # Insert movies into MongoDB
        if movies_data:
            result = movies.insert_many(movies_data)
            print(f"Successfully loaded {len(result.inserted_ids)} movies")
        else:
            print("No movies to load")
            
    except Exception as e:
        print(f"Error loading movies: {e}")

def load_ratings_from_csv(csv_file_path):
    """
    Load user ratings from ratings_small.csv into MongoDB.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Connect to MongoDB
        client = get_mongo_client()
        db = client["cinemate"]
        reviews = db["reviews"]
        
        # Convert DataFrame to list of dictionaries
        reviews_data = []
        for _, row in df.iterrows():
            # Convert timestamp to datetime
            timestamp = datetime.fromtimestamp(row.get("timestamp", 0))
            
            review = {
                "user_id": str(row.get("userId", "")),
                "movie_id": str(row.get("movieId", "")),
                "rating": float(row.get("rating", 0)),
                "review": "",  # No review text in this dataset
                "created_at": timestamp
            }
            reviews_data.append(review)
        
        # Insert reviews into MongoDB
        if reviews_data:
            result = reviews.insert_many(reviews_data)
            print(f"Successfully loaded {len(result.inserted_ids)} reviews")
        else:
            print("No reviews to load")
            
    except Exception as e:
        print(f"Error loading reviews: {e}")

if __name__ == "__main__":
    # Load movies from movies_metadata.csv
    print("Loading movies...")
    load_movies_from_csv("../datasets/movies_metadata.csv")
    
    # Load ratings from ratings_small.csv
    print("\nLoading ratings...")
    load_ratings_from_csv("../datasets/ratings_small.csv")
    
    print("\nData loading complete!") 