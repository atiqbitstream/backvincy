#!/usr/bin/env python
"""
Migration script to add image_url column to live_session table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_image_url_column():
    """Add image_url column to live_session table"""
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Add the image_url column
            connection.execute(text("""
                ALTER TABLE live_session 
                ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
            """))
            
            # Commit the transaction
            connection.commit()
            
            print("✅ Successfully added image_url column to live_session table")
            
    except Exception as e:
        print(f"❌ Error adding image_url column: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    add_image_url_column()
