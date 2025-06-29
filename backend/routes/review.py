from fastapi import APIRouter, HTTPException, Query
from models.review import Review
from db.mongo import get_mongo_client
from datetime import datetime

router = APIRouter()

@router.post("/reviews/")
def add_review(review: Review):
    """
    Add a new review for a movie. Updates movie's avg_rating and num_reviews.
    """
    client = get_mongo_client()
    db = client["cinemate"]
    reviews = db["reviews"]
    movies = db["movies"]

    # Check if user already reviewed this movie
    if reviews.find_one({"user_id": review.user_id, "movie_id": review.movie_id}):
        raise HTTPException(status_code=400, detail="User already reviewed this movie.")

    review_dict = review.dict()
    review_dict["created_at"] = datetime.utcnow()
    reviews.insert_one(review_dict)

    # Update movie's avg_rating and num_reviews
    all_reviews = list(reviews.find({"movie_id": review.movie_id}))
    num_reviews = len(all_reviews)
    avg_rating = sum(r["rating"] for r in all_reviews) / num_reviews
    movies.update_one({"_id": review.movie_id}, {"$set": {"avg_rating": avg_rating, "num_reviews": num_reviews}})

    return {"msg": "Review added successfully."}

@router.get("/reviews/")
def list_reviews(movie_id: str = Query(None), user_id: str = Query(None)):
    """
    List all reviews, or filter by movie_id or user_id.
    """
    client = get_mongo_client()
    db = client["cinemate"]
    reviews = db["reviews"]
    query = {}
    if movie_id:
        query["movie_id"] = movie_id
    if user_id:
        query["user_id"] = user_id
    review_list = []
    for review in reviews.find(query):
        review["_id"] = str(review["_id"])
        review_list.append(review)
    return review_list 