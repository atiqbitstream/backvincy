import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def add_created_by_column():
    """Add created_by column to user_hub table if it doesn't exist"""
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        try:
            # Check if column already exists
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user_hub' 
                AND column_name = 'created_by'
            """))
            
            if result.fetchone() is None:
                # Column doesn't exist, add it
                session.execute(text("""
                    ALTER TABLE user_hub 
                    ADD COLUMN created_by VARCHAR(100)
                """))
                session.commit()
                print("✅ Successfully added created_by column to user_hub table")
            else:
                print("ℹ️  created_by column already exists in user_hub table")
                
        except Exception as e:
            print(f"❌ Error adding created_by column: {e}")
            session.rollback()

if __name__ == "__main__":
    add_created_by_column()