import os
from neo4j import GraphDatabase
from typing import List, Dict, Any

# Neo4j connection configuration
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

class Neo4jGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def close(self):
        self.driver.close()
    
    def create_movie_node(self, movie_data: Dict[str, Any]):
        """
        Create a movie node in Neo4j.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_movie, movie_data)
    
    @staticmethod
    def _create_movie(tx, movie_data):
        query = """
        MERGE (m:Movie {id: $movie_id})
        SET m.title = $title,
            m.year = $year,
            m.avg_rating = $avg_rating,
            m.num_reviews = $num_reviews
        """
        tx.run(query, 
               movie_id=movie_data['tmdb_id'],
               title=movie_data['title'],
               year=movie_data['year'],
               avg_rating=movie_data['avg_rating'],
               num_reviews=movie_data['num_reviews'])
    
    def create_genre_relationships(self, movie_id: int, genres: List[str]):
        """
        Create genre relationships for a movie.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_genre_relationships, movie_id, genres)
    
    @staticmethod
    def _create_genre_relationships(tx, movie_id, genres):
        for genre in genres:
            # Create genre node
            tx.run("MERGE (g:Genre {name: $genre})", genre=genre)
            # Create relationship
            tx.run("""
                MATCH (m:Movie {id: $movie_id})
                MATCH (g:Genre {name: $genre})
                MERGE (m)-[:BELONGS_TO]->(g)
            """, movie_id=movie_id, genre=genre)
    
    def create_user_node(self, user_id: str, username: str):
        """
        Create a user node in Neo4j.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_user, user_id, username)
    
    @staticmethod
    def _create_user(tx, user_id, username):
        query = """
        MERGE (u:User {id: $user_id})
        SET u.username = $username
        """
        tx.run(query, user_id=user_id, username=username)
    
    def create_user_rating(self, user_id: str, movie_id: int, rating: float):
        """
        Create a user rating relationship.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_user_rating, user_id, movie_id, rating)
    
    @staticmethod
    def _create_user_rating(tx, user_id, movie_id, rating):
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (m:Movie {id: $movie_id})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating = $rating
        """
        tx.run(query, user_id=user_id, movie_id=movie_id, rating=rating)
    
    def get_similar_movies_graph(self, movie_id: int, limit: int = 5):
        """
        Neo4j Graph Query: Find similar movies based on shared genres and user ratings.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_similar_movies, movie_id, limit)
            return result
    
    @staticmethod
    def _get_similar_movies(tx, movie_id, limit):
        query = """
        MATCH (m1:Movie {id: $movie_id})-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(m2:Movie)
        WHERE m1 <> m2
        WITH m2, count(g) as shared_genres, m2.avg_rating as rating
        ORDER BY shared_genres DESC, rating DESC
        LIMIT $limit
        RETURN m2.title as title, m2.id as id, shared_genres, rating
        """
        result = tx.run(query, movie_id=movie_id, limit=limit)
        return [record.data() for record in result]
    
    def get_movie_recommendations_for_user(self, user_id: str, limit: int = 5):
        """
        Neo4j Graph Query: Get personalized movie recommendations based on user's rating history.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_user_recommendations, user_id, limit)
            return result
    
    @staticmethod
    def _get_user_recommendations(tx, user_id, limit):
        query = """
        MATCH (u:User {id: $user_id})-[r:RATED]->(m1:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(m2:Movie)
        WHERE r.rating >= 4.0 AND NOT (u)-[:RATED]->(m2)
        WITH m2, count(g) as genre_matches, avg(r.rating) as avg_user_rating, m2.avg_rating as movie_rating
        ORDER BY genre_matches DESC, avg_user_rating DESC, movie_rating DESC
        LIMIT $limit
        RETURN m2.title as title, m2.id as id, genre_matches, movie_rating
        """
        result = tx.run(query, user_id=user_id, limit=limit)
        return [record.data() for record in result]
    
    def get_popular_genres(self, limit: int = 10):
        """
        Neo4j Graph Query: Find most popular genres based on movie ratings.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_popular_genres, limit)
            return result
    
    @staticmethod
    def _get_popular_genres(tx, limit):
        query = """
        MATCH (g:Genre)<-[:BELONGS_TO]-(m:Movie)
        WITH g, count(m) as movie_count, avg(m.avg_rating) as avg_rating
        ORDER BY movie_count DESC, avg_rating DESC
        LIMIT $limit
        RETURN g.name as genre, movie_count, avg_rating
        """
        result = tx.run(query, limit=limit)
        return [record.data() for record in result]
    
    def get_shortest_path_between_movies(self, movie1_id: int, movie2_id: int):
        """
        Neo4j Graph Query: Find shortest path between two movies through genres.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_shortest_path, movie1_id, movie2_id)
            return result
    
    @staticmethod
    def _get_shortest_path(tx, movie1_id, movie2_id):
        query = """
        MATCH path = shortestPath(
            (m1:Movie {id: $movie1_id})-[:BELONGS_TO*]-(m2:Movie {id: $movie2_id})
        )
        RETURN path
        """
        result = tx.run(query, movie1_id=movie1_id, movie2_id=movie2_id)
        return [record.data() for record in result]

# Global Neo4j instance
neo4j_graph = Neo4jGraph() 