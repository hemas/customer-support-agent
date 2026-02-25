import psycopg2
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        #password=os.getenv("DB_PASSWORD")
    )
    return conn

def save_customer(name, email):
    """Save a new customer to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customers (name, email)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """, (name, email))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    except Exception as e:
        print(f"Error saving customer: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def save_ticket(customer_id, query, sentiment, intent):
    """Save a new support ticket"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tickets (customer_id, query, sentiment, intent)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (customer_id, query, sentiment, intent))
        ticket_id = cursor.fetchone()[0]
        conn.commit()
        return ticket_id
    except Exception as e:
        print(f"Error saving ticket: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def save_conversation(ticket_id, role, message):
    """Save a message in a conversation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO conversations (ticket_id, role, message)
            VALUES (%s, %s, %s)
        """, (ticket_id, role, message))
        conn.commit()
    except Exception as e:
        print(f"Error saving conversation: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def search_knowledge_base(category):
    """Search knowledge base by category"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT question, answer
            FROM knowledge_base
            WHERE category = %s
            LIMIT 3
        """, (category,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Test the connection
if __name__ == "__main__":
    print("Testing database connection...")
    conn = get_db_connection()
    print("✅ Database connected successfully!")
    conn.close()

    print("\nTesting knowledge base search...")
    results = search_knowledge_base("billing")
    for question, answer in results:
        print(f"Q: {question}")
        print(f"A: {answer}\n")