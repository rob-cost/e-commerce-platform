import pytest
from fastapi.testclient import TestClient                 # FastAPI's test client that simulates HTTP requests without running a real server
from sqlalchemy import create_engine                      # Creates database connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool                    # Special connection pool that keeps a single persistent connection (crucial for in-memory databases)

from app.database import Base, get_db                     # Base = mdoel we delcared, get_db = db to override
from app.main import app

# 1. Create in-memory SQLite test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"            # creates DB entirely in RAM

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},            # SQLite normally restricts access to one thread. This disables that check (needed for FastAPI's async nature)
    poolclass=StaticPool                                  # keeps ONE persistent connection alive
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine        # each time TestingSessionLocal() is called, we get a new database session.
)

# 2. Create tables
Base.metadata.create_all(bind=engine)                     # creates all database tables

# 3. Dependency override                                  # overrides FastAPI db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 4. Create module-level client
client = TestClient(app)                                  # creates a client tha can make request to FastAPI

# 5. Optional: Keep fixture for cleanup
@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)