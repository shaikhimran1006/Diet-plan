from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date

DATABASE_URL = "sqlite:///./diet_fitness.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    activity_level = Column(String)
    health_goal = Column(String)
    food_preferences = Column(String)
    allergies = Column(String, nullable=True)
    medical_conditions = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bmr = Column(Float)
    daily_calories = Column(Integer)
    meal_plan = Column(Text)  # JSON string
    macros = Column(Text)  # JSON string
    exercises = Column(Text)  # JSON string
    grocery_list = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)


class WeightLog(Base):
    __tablename__ = "weight_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    weight = Column(Float)  # in kg
    date = Column(Date, default=date.today)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class HydrationLog(Base):
    __tablename__ = "hydration_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    glasses = Column(Integer)  # 8 oz glasses
    date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)


class CalorieLog(Base):
    __tablename__ = "calorie_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    calories = Column(Integer)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    description = Column(String)
    date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise_name = Column(String)
    duration_minutes = Column(Integer)
    calories_burned = Column(Integer, nullable=True)
    date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
