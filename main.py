import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Alidiamond API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Alidiamond Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/categories")
def categories():
    return {
        "items": [
            {"id": 1, "name": "Web Development", "slug": "web-dev", "description": "HTML, CSS, JavaScript, React, and modern tooling."},
            {"id": 2, "name": "Data Science", "slug": "data-science", "description": "Python, Pandas, visualization, and machine learning foundations."},
            {"id": 3, "name": "Design", "slug": "design", "description": "UI/UX, Figma, accessibility, and design systems."},
            {"id": 4, "name": "Cloud & DevOps", "slug": "cloud-devops", "description": "Docker, Kubernetes, CI/CD, and cloud fundamentals."},
            {"id": 5, "name": "Mobile", "slug": "mobile", "description": "iOS, Android, and cross‑platform app development."},
            {"id": 6, "name": "AI & ML", "slug": "ai-ml", "description": "Neural nets, LLMs, and practical AI projects."}
        ]
    }

@app.get("/instructors")
def instructors():
    return {
        "items": [
            {"id": 1, "name": "Ava Thompson", "title": "Senior Frontend Engineer", "rating": 4.9, "students": 18200, "bio": "10+ years building delightful web apps using React and modern CSS."},
            {"id": 2, "name": "Leo Martinez", "title": "Data Scientist", "rating": 4.8, "students": 15650, "bio": "Hands‑on machine learning with a focus on real‑world applications."},
            {"id": 3, "name": "Maya Chen", "title": "Product Designer", "rating": 4.9, "students": 12140, "bio": "Design systems, accessibility, and prototyping in Figma."},
            {"id": 4, "name": "Ethan Patel", "title": "Cloud Architect", "rating": 4.7, "students": 9800, "bio": "DevOps, containers, and scalable cloud architectures."}
        ]
    }

@app.get("/pricing")
def pricing():
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price": 0,
                "period": "forever",
                "features": ["Access to free courses", "Community support", "Weekly newsletter"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 19,
                "period": "month",
                "features": ["All categories", "Certificates", "Downloads & resources", "Priority support"]
            },
            {
                "id": "team",
                "name": "Team",
                "price": 49,
                "period": "month",
                "features": ["Everything in Pro", "Team dashboard", "Seats & SSO", "Dedicated success"]
            }
        ]
    }

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
