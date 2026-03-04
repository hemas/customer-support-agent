from sentence_transformers import SentenceTransformer
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Load the sentence transformer model
# This converts text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def generate_embedding(text):
    """Convert text to vector"""
    embedding = model.encode(text)
    return embedding.tolist()

def populate_embeddings():
    """Generate embeddings for all knowledge base entries"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get all entries without embeddings
        cursor.execute("""
            SELECT id, question, answer 
            FROM knowledge_base 
            WHERE embedding IS NULL
        """)
        entries = cursor.fetchall()

        print(f"Generating embeddings for {len(entries)} entries...")

        for entry_id, question, answer in entries:
            # Combine question and answer for better search
            text = f"{question} {answer}"
            embedding = generate_embedding(text)

            # Save embedding to database
            cursor.execute("""
                UPDATE knowledge_base 
                SET embedding = %s 
                WHERE id = %s
            """, (embedding, entry_id))

        conn.commit()
        print(f"✅ Generated embeddings for {len(entries)} entries!")

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def search_knowledge_base_rag(query, limit=3):
    """Search knowledge base using semantic similarity"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Convert query to vector
        query_embedding = generate_embedding(query)

        # Search for most similar entries using vector similarity
        cursor.execute("""
            SELECT question, answer,
            1 - (embedding <=> %s::vector) as similarity
            FROM knowledge_base
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, limit))

        results = cursor.fetchall()

        # Format results
        formatted = []
        for question, answer, similarity in results:
            formatted.append({
                "question": question,
                "answer": answer,
                "similarity": round(similarity, 2)
            })

        return formatted

    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Test it
if __name__ == "__main__":
    print("Step 1 — Generating embeddings...")
    populate_embeddings()

    print("\nStep 2 — Testing RAG search...")
    test_queries = [
        "I was charged twice this month",
        "I cannot login to my account",
        "I want to return my order",
        "My package has not arrived"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = search_knowledge_base_rag(query)
        for result in results:
            print(f"  Similarity: {result['similarity']}")
            print(f"  Q: {result['question']}")
            print(f"  A: {result['answer'][:80]}...")
