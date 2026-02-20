from livekit.agents import function_tool
import logging
import os
from typing import Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger("ecommerce-tools")

# 1. Define the absolute path to your vector database folder
VECTOR_DB_PATH = r"C:\Users\fasal_pgbi6fg\OneDrive\Desktop\Ecommerce-bot\vector_db"

# Initialize Vector Store once at module level for efficiency
try:
    if os.path.exists(VECTOR_DB_PATH):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # allow_dangerous_deserialization is required for loading local FAISS pickle files
        vector_db = FAISS.load_local(
            VECTOR_DB_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        logger.info(f"Successfully loaded FAISS index from {VECTOR_DB_PATH}")
    else:
        logger.error(f"Vector DB path not found: {VECTOR_DB_PATH}")
        vector_db = None
except Exception as e:
    logger.error(f"Failed to load FAISS index: {e}")
    vector_db = None

async def query_rag(query: str) -> str:
    """Helper function to retrieve context from the vector store."""
    if not vector_db:
        return "I'm sorry, my knowledge base is currently offline. Please try again later."
    
    # We perform a similarity search to find the most relevant chunks from the PDF [cite: 5]
    docs = await vector_db.asimilarity_search(query, k=3)
    
    if not docs:
        return "I couldn't find any specific information regarding that in our records."
        
    context = "\n---\n".join([doc.page_content for doc in docs])
    return context

@function_tool
async def get_order_status(order_id: str):
    """
    Look up the current status and delivery information for a specific order ID.
    """
    logger.info(f"RAG lookup for order: {order_id}")
    # Queries the RAG system to find order details like 'Processing', 'Shipped', or 'Delivered' [cite: 54, 102]
    context = await query_rag(f"What is the status of order {order_id} and what are the items?")
    return f"Here is the information I found for {order_id}:\n\n{context}"

@function_tool
async def get_policy_info(topic: str):
    """
    Get store policies regarding shipping tiers, return windows, refunds, or warranty coverage.
    """
    logger.info(f"RAG lookup for policy: {topic}")
    # Searches for policies such as the 45-day return policy or shipping timelines [cite: 53, 62]
    context = await query_rag(f"What is the company policy regarding {topic}?")
    return context

@function_tool
async def get_product_info(product_name: str):
    """
    Check product availability, price, SKU, and technical specifications from the catalog.
    """
    logger.info(f"RAG lookup for product: {product_name}")
    # Retrieves catalog details like SKU, Price, and Stock Status [cite: 6, 11, 12, 14]
    context = await query_rag(f"Provide details, price, and stock status for the product: {product_name}")
    return context

class EcommerceTools:
    @staticmethod
    def get_all_tools():
        return [get_order_status, get_policy_info, get_product_info]