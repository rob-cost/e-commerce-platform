from app.schemas.user import UserCreate
from .test_utils import client, TestingSessionLocal
from app.models.user import User

# test create user
def test_create_user():
    payload = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@gmail.com'
    }

    response = client.post("/users", json=payload)
    print(response.text)

    data = response.json()

    assert response.status_code == 200
    assert data['username'] == "testuser"
    assert data['email'] == "test@gmail.com"

    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == 'testuser').first()
    assert user.hashed_password != 'testpassword'  # Ensure password is hashed
    assert user.hashed_password.startswith('$2b$')


# test check duplicate user
def test_create_duplicate_user():
    payload = {
        'username': 'testuser2',
        'password': 'testpassword',
        'email': 'test2@gmail.com'
    }
    response1 = client.post("/users", json=payload)
    print(f"\n=== First Request ===")
    print(f"Status: {response1.status_code}")
    print(f"Body: {response1.json()}")

    assert response1.status_code == 200

    response2 = client.post("/users", json=payload)
    print(f"\n=== Second Request (Duplicate) ===")
    print(f"Status: {response2.status_code}")
    print(f"Body: {response2.json()}")

    assert response2.status_code == 400
    assert response2.json()['detail'] == 'User already exists'

# test update profile
def test_update_user():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == 'testuser').first()

    print(f"\n=== Request User ===")
    print(f"User: {user.id}")

    payload = {
        'username': 'new_username',
        'password': 'testpassword',
        'email': 'test@gmail.com'
    }

    response = client.put(f"/users/{user.id}", json=payload)

    print(f"\n=== Request (Update) ===")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")

    assert response.status_code == 200

    data = response.json()

    assert data['username'] == 'new_username'
    
