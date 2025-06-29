import streamlit as st
import requests
import json

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except:
        return False

def get_movies():
    """Get movies from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/movies/")
        if response.status_code == 200:
            data = response.json()
            # Extract the movies list from the response
            return data.get('movies', [])
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

def get_movie_count():
    """Get total movie count."""
    try:
        response = requests.get(f"{API_BASE_URL}/movies/count")
        if response.status_code == 200:
            return response.json().get("total_movies", 0)
        return 0
    except:
        return 0

# Main app
st.title("CineMate 🎬")
st.write("Your smart movie recommendation system")

# Check API connection
if not test_api_connection():
    st.error("⚠️ Cannot connect to the API. Make sure the backend is running on http://localhost:8000")
    st.stop()

st.success("✅ Connected to API successfully!")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Movies", "About"])

if page == "Movies":
    st.header("🎬 Movie Database")
    
    # Get movie count
    total_movies = get_movie_count()
    st.info(f"Total movies in database: {total_movies}")
    
    # Get and display movies
    movies = get_movies()
    
    if movies and len(movies) > 0:
        st.success(f"✅ Loaded {len(movies)} movies from the database")
        
        # Search functionality
        search_term = st.text_input("🔍 Search movies by title:")
        
        # Filter movies based on search
        if search_term:
            filtered_movies = [m for m in movies if search_term.lower() in m.get('title', '').lower()]
            st.write(f"Found {len(filtered_movies)} movies matching '{search_term}'")
        else:
            filtered_movies = movies
        
        # Display movies (limit to first 20)
        display_movies = filtered_movies[:20] if len(filtered_movies) > 20 else filtered_movies
        
        for i, movie in enumerate(display_movies):
            with st.expander(f"{movie.get('title', 'Unknown')} ({movie.get('year', 'N/A')})"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if movie.get('poster_url'):
                        st.image(movie.get('poster_url'), width=150)
                    else:
                        st.write("No poster available")
                
                with col2:
                    st.write(f"**Year:** {movie.get('year', 'N/A')}")
                    st.write(f"**Genres:** {', '.join(movie.get('genres', []))}")
                    st.write(f"**Rating:** {movie.get('avg_rating', 'N/A')}/10")
                    st.write(f"**Reviews:** {movie.get('num_reviews', 0)}")
                    
                    if movie.get('description'):
                        st.write(f"**Description:** {movie.get('description')[:200]}...")
                    
                    if movie.get('tagline'):
                        st.write(f"**Tagline:** {movie.get('tagline')}")
    else:
        st.error("❌ No movies found or API error occurred")

elif page == "About":
    st.header("About CineMate")
    st.write("""
    CineMate is a smart movie recommendation system built with:
    
    - **Backend:** FastAPI with MongoDB, Redis, and Neo4j
    - **Frontend:** Streamlit
    - **Databases:** 
        - MongoDB (movie data)
        - Redis (caching)
        - Neo4j (social graph)
    
    Features:
    - Browse movies
    - Search functionality
    - Movie recommendations (coming soon)
    - User ratings and reviews
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for NoSQL Applications Project") 