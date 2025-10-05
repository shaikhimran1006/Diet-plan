"""
Initialize database with a default user for testing
"""
from database import SessionLocal, User, Base, engine
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
db = SessionLocal()

try:
    # Check if user 1 exists
    user = db.query(User).filter(User.id == 1).first()
    
    if user:
        print(f"✅ User 1 already exists:")
        print(f"   Age: {user.age}")
        print(f"   Gender: {user.gender}")
        print(f"   Height: {user.height} cm")
        print(f"   Weight: {user.weight} kg")
        print(f"   Activity: {user.activity_level}")
        print(f"   Health Goal: {user.health_goal}")
    else:
        print("❌ No user found. Creating default user...")
        
        # Create default user
        new_user = User(
            age=25,
            gender="male",
            height=175.0,
            weight=70.0,
            activity_level="moderate",
            health_goal="weight_loss",
            food_preferences="balanced",
            allergies=None,
            medical_conditions=None,
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ Created user with ID: {new_user.id}")
        print(f"   Age: {new_user.age}")
        print(f"   Gender: {new_user.gender}")
        print(f"   Height: {new_user.height} cm")
        print(f"   Weight: {new_user.weight} kg")
        print(f"   Activity: {new_user.activity_level}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

print("\n✨ Database initialized!")
print("\n💡 Next steps:")
print("   1. Open http://localhost:5174 in your browser")
print("   2. The Dashboard will load user data")
print("   3. Generate a diet plan to see recommendations")
print("   4. Start logging weight, calories, exercise, etc.")
