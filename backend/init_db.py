"""
Database initialization script.
Creates all tables and verifies PostgreSQL connection.
Run this before starting the application for the first time.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database.database import init_db, check_db_connection, engine
from database.models import Base
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize the database - create all tables."""
    print("="*80)
    print("DATABASE INITIALIZATION - AI Tutor Orchestrator")
    print("="*80)
    print()
    
    # Display connection info
    print(f"📊 Database URL: {settings.database_url[:50]}...")
    print(f"🌍 Supabase URL: {settings.supabase_url}")
    print()
    
    # Step 1: Check connection
    print("Step 1: Checking database connection...")
    is_connected = await check_db_connection()
    
    if not is_connected:
        print("❌ Failed to connect to database!")
        print("Please check your DATABASE_URL in .env file")
        return False
    
    print("✅ Database connection successful!")
    print()
    
    # Step 2: Create tables
    print("Step 2: Creating database tables...")
    print("Tables to create:")
    print("  - users (student profiles)")
    print("  - conversations (chat sessions)")
    print("  - chat_messages (message history)")
    print("  - tool_executions (tool usage logs)")
    print("  - parameter_extractions (inference analytics)")
    print()
    
    try:
        await init_db()
        print("✅ All tables created successfully!")
        print()
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    # Step 3: Verify tables
    print("Step 3: Verifying table creation...")
    try:
        async with engine.begin() as conn:
            # Query to check if tables exist
            result = await conn.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
            tables = [row[0] for row in result]
            
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"  ✓ {table}")
            print()
            
            expected_tables = [
                'users', 'conversations', 'chat_messages', 
                'tool_executions', 'parameter_extractions'
            ]
            
            missing = set(expected_tables) - set(tables)
            if missing:
                print(f"⚠️  Missing tables: {missing}")
            else:
                print("✅ All expected tables present!")
    
    except Exception as e:
        print(f"⚠️  Could not verify tables: {e}")
    
    print()
    print("="*80)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Start the tools service: python tools_main.py")
    print("2. Start the orchestrator service: python main.py")
    print("3. Run the demo: python final_demo.py")
    print()
    
    return True


async def drop_all_tables():
    """
    DROP all tables (use with caution!).
    This will delete all data.
    """
    print("⚠️  WARNING: This will DELETE ALL DATA!")
    confirm = input("Type 'DELETE ALL DATA' to confirm: ")
    
    if confirm != "DELETE ALL DATA":
        print("Cancelled.")
        return
    
    print("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    print("✅ All tables dropped.")


async def reset_database():
    """Reset database - drop and recreate all tables."""
    print("="*80)
    print("DATABASE RESET")
    print("="*80)
    print()
    
    await drop_all_tables()
    print()
    await initialize_database()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        asyncio.run(reset_database())
    elif len(sys.argv) > 1 and sys.argv[1] == "--drop":
        asyncio.run(drop_all_tables())
    else:
        asyncio.run(initialize_database())
