from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq LLM with a SUPPORTED model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",  # ✅ supported model
    temperature=0.7
)

if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are")
    print(response.content)
