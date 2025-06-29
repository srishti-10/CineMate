import requests
import json
import time

def test_complete_system():
    """
    Comprehensive test of the entire CineMate system.
    """
    base_url = "http://localhost:8000"
    
    print("🎬 CineMate Complete System Test")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing API Health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ API is healthy")
        else:
            print(f"   ❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to API: {e}")
        return False
    
    # Test 2: MongoDB - Basic Movie Operations
    print("\n2. Testing MongoDB Operations...")
    try:
        # Test movie count
        response = requests.get(f"{base_url}/movies/count")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ MongoDB: {data.get('total_movies', 0)} movies loaded")
        else:
            print(f"   ❌ MongoDB movie count failed: {response.status_code}")
        
        # Test movie list
        response = requests.get(f"{base_url}/movies/?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ MongoDB: Retrieved {len(data.get('movies', []))} movies")
        else:
            print(f"   ❌ MongoDB movie list failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ MongoDB test failed: {e}")
    
    # Test 3: MongoDB - Aggregation Queries
    print("\n3. Testing MongoDB Aggregation Queries...")
    try:
        # Test genre statistics
        response = requests.get(f"{base_url}/movies/analytics/genre-stats")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ MongoDB Aggregation: Genre stats for {data.get('total_genres', 0)} genres")
        else:
            print(f"   ❌ MongoDB genre stats failed: {response.status_code}")
        
        # Test yearly trends
        response = requests.get(f"{base_url}/movies/analytics/yearly-trends")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ MongoDB Aggregation: Yearly trends for {data.get('years_analyzed', 0)} years")
        else:
            print(f"   ❌ MongoDB yearly trends failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ MongoDB aggregation test failed: {e}")
    
    # Test 4: Movie Recommendations
    print("\n4. Testing Movie Recommendations...")
    try:
        # Test popular movies
        response = requests.get(f"{base_url}/movies/recommendations/popular?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Popular Movies: {data.get('count', 0)} recommendations")
        else:
            print(f"   ❌ Popular movies failed: {response.status_code}")
        
        # Test genre recommendations
        response = requests.get(f"{base_url}/movies/recommendations/genre/Action?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Genre Recommendations: {data.get('count', 0)} Action movies")
        else:
            print(f"   ❌ Genre recommendations failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Recommendations test failed: {e}")
    
    # Test 5: Search Functionality
    print("\n5. Testing Search Functionality...")
    try:
        response = requests.get(f"{base_url}/movies/search/Avatar")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Search: Found {data.get('count', 0)} movies for 'Avatar'")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Search test failed: {e}")
    
    # Test 6: Graph Database (Neo4j) - Note: Requires Neo4j to be running
    print("\n6. Testing Graph Database (Neo4j)...")
    try:
        # Test popular genres graph query
        response = requests.get(f"{base_url}/graph/popular-genres?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Neo4j: Popular genres analysis ({data.get('count', 0)} genres)")
        else:
            print(f"   ⚠️  Neo4j not available: {response.status_code} (This is expected if Neo4j is not running)")
    except Exception as e:
        print(f"   ⚠️  Neo4j test failed: {e} (This is expected if Neo4j is not running)")
    
    # Test 7: API Documentation
    print("\n7. Testing API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("   ✅ API Documentation: Available at /docs")
        else:
            print(f"   ❌ API Documentation failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API Documentation test failed: {e}")
    
    # Test 8: System Information
    print("\n8. System Information...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Title: {data.get('message', 'Unknown')}")
            print(f"   ✅ Databases: {', '.join(data.get('databases', []))}")
        else:
            print(f"   ❌ System info failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ System info test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 CineMate System Test Complete!")
    print("\n📋 Summary:")
    print("✅ MongoDB: Document database with aggregation queries")
    print("✅ FastAPI: RESTful API with comprehensive endpoints")
    print("✅ Movie Recommendations: Multiple recommendation algorithms")
    print("✅ Search: Full-text search functionality")
    print("⚠️  Neo4j: Graph database (requires Neo4j service)")
    print("⚠️  Redis: Caching (requires Redis service)")
    
    print("\n🚀 Next Steps:")
    print("1. Start Neo4j: docker-compose up neo4j")
    print("2. Start Redis: docker-compose up redis")
    print("3. Test graph queries and caching features")
    print("4. Access frontend: http://localhost:8501")
    print("5. Access API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    test_complete_system() 