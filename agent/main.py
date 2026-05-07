from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from tools.sentiment_tool import analyze_sentiment, detect_intent
from tools.database_tool import save_ticket, save_conversation, save_customer
from tools.rag_tool import search_knowledge_base_rag, populate_embeddings
import os

load_dotenv()

# ─────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────

@tool
def check_sentiment(query: str) -> str:
    """Analyze the sentiment of a customer message"""
    result = analyze_sentiment(query)
    return f"Customer sentiment is {result['sentiment']}"

@tool 
def search_kb(query: str) -> str:
    """Search knowledge base using semantic search.
    Pass the customer's actual message as the query."""
    results = search_knowledge_base_rag(query)
    if not results:
        return "No relevant information found in knowledge base"
    response = ""
    for result in results:
        response += f"Q: {result['question']}\n"
        response += f"A: {result['answer']}\n"
        response += f"Relevance: {result['similarity']}\n\n"
    return response

@tool
def escalate_to_human(reason: str) -> str:
    """Escalate the issue to a human agent
    when you cannot resolve it yourself"""
    return f"Issue escalated to human agent. Reason: {reason}. A human will contact the customer within 24 hours."

# ─────────────────────────────────────────
# AGENT
# ─────────────────────────────────────────

def create_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [check_sentiment, search_kb, escalate_to_human]

    # ReAct prompt works much better with Groq
    prompt = PromptTemplate.from_template("""You are a helpful and empathetic customer support agent.

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Always:
1. Check sentiment first
2. Search knowledge base for relevant answers
3. Respond with empathy and helpfulness
4. Escalate to human if you cannot resolve

Begin!

Question: {input}
Thought: {agent_scratchpad}""")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    return agent_executor

# ─────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────

def process_query(query: str, customer_name: str = "Customer", customer_email: str = "customer@example.com"):
    print(f"\n{'='*60}")
    print(f"Customer: {customer_name}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")

    # Save customer
    customer_id = save_customer(customer_name, customer_email)
    if not customer_id:
        customer_id = 1

    # Detect sentiment and intent
    sentiment_result = analyze_sentiment(query)
    sentiment = sentiment_result['sentiment']
    intent = detect_intent(query)

    print(f"Detected Sentiment: {sentiment}")
    print(f"Detected Intent: {intent}\n")

    # Run agent
    populate_embeddings()
    agent = create_agent()
    response = agent.invoke({"input": query})
    agent_response = response.get('output', '')

    print(f"DEBUG - Agent Response: {agent_response}")

    # Save to database
    ticket_id = save_ticket(customer_id, query, sentiment, intent)
    save_conversation(ticket_id, "user", query)
    save_conversation(ticket_id, "agent", agent_response)

    print(f"\n{'='*60}")
    print(f"Agent Response: {agent_response}")
    print(f"Ticket ID: {ticket_id}")
    print(f"{'='*60}\n")

    return {
        "ticket_id": ticket_id,
        "response": agent_response,
        "sentiment": sentiment,
        "intent": intent
    }

# ─────────────────────────────────────────
# TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    process_query(
        query="I am really frustrated! My bill is wrong and nobody is helping me!",
        customer_name="John Smith",
        customer_email="john@example.com"
    )