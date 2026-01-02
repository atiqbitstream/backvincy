#!/usr/bin/env python
"""
Migration script to add hero_description column to about table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_hero_description_column():
    """Add hero_description column to about table"""
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Add the hero_description column
            connection.execute(text("""
                ALTER TABLE about 
                ADD COLUMN IF NOT EXISTS hero_description TEXT;
            """))
            
            # Commit the transaction
            connection.commit()
            
            print("✅ Successfully added hero_description column to about table")
            
    except Exception as e:
        print(f"❌ Error adding hero_description column: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    add_hero_description_column()
