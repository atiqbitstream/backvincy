#!/usr/bin/env python3
"""
Migration script to update existing user_hub records to inactive status
and apply the new default status behavior.

Run this script after updating the model to ensure existing data is consistent.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate_user_hub_status():
    """Update existing user_hub records to have inactive status by default"""
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()
            
            try:
                # Update existing records to inactive status (False)
                # This ensures all existing submissions require admin approval
                result = connection.execute(
                    text("UPDATE user_hub SET status = false WHERE status = true")
                )
                
                print(f"Updated {result.rowcount} user_hub records to inactive status")
                
                # Update the default value in the database schema
                connection.execute(
                    text("ALTER TABLE user_hub ALTER COLUMN status SET DEFAULT false")
                )
                
                print("Updated user_hub table default status to false")
                
                # Commit the transaction
                trans.commit()
                print("Migration completed successfully!")
                
            except Exception as e:
                # Rollback on error
                trans.rollback()
                print(f"Error during migration: {e}")
                raise
                
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting user_hub status migration...")
    migrate_user_hub_status()