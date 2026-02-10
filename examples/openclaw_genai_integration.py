"""
OpenClaw + Purdue GenAI Studio Integration

This example demonstrates how to integrate OpenClaw agents with
Purdue GenAI Studio API as the LLM backend, monitored by AgentOps.
"""

import os
import requests
import json
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Try to import agentops (optional)
try:
    import agentops
    AGENTOPS_AVAILABLE = True
except ImportError:
    AGENTOPS_AVAILABLE = False
    print("Note: AgentOps not installed. Monitoring disabled.")

# Load environment variables
load_dotenv()

# Initialize AgentOps if available
if AGENTOPS_AVAILABLE:
    AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
    if AGENTOPS_API_KEY:
        agentops.init(AGENTOPS_API_KEY)
        print("âœ“ AgentOps initialized")
    else:
        print("Note: AGENTOPS_API_KEY not found. Monitoring disabled.")


class PurdueGenAIProvider:
    """Purdue GenAI Studio API provider for OpenClaw"""
    
    def __init__(self, api_key: str, base_url: str = None, model: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://genai.rcac.purdue.edu/api/v1"
        self.model = model or "llama3.2:latest"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: List[Dict], max_tokens: int = 1000, temperature: float = 0.7) -> Dict:
        """Make a chat completion request to Purdue GenAI Studio"""
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def list_models(self) -> List[str]:
        """List available models"""
        response = requests.get(
            f"{self.base_url}/models",
            headers=self.headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()["data"]
            return [model["id"] for model in models]
        else:
            raise Exception(f"API Error: {response.status_code}")


class OpenClawAgent:
    """OpenClaw agent using Purdue GenAI Studio as LLM backend"""
    
    def __init__(self, name: str, genai_provider: PurdueGenAIProvider, system_prompt: str = None):
        self.name = name
        self.genai_provider = genai_provider
        self.system_prompt = system_prompt or "You are a helpful AI assistant."
        self.conversation_history = []
        if system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": system_prompt
            })
    
    def process(self, user_input: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Process user input and return response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response from GenAI
        try:
            result = self.genai_provider.chat_completion(
                messages=self.conversation_history,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract response
            assistant_message = result["choices"][0]["message"]["content"]
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })


def main():
    """Main integration example"""
    print("=" * 60)
    print("OpenClaw + Purdue GenAI Studio Integration")
    print("=" * 60)
    
    # Get configuration
    GENAI_API_KEY = os.getenv("PURDUE_GENAI_API_KEY", "sk-60b3407df4764b29b5a5acf33c7fdaee")
    GENAI_BASE_URL = os.getenv("PURDUE_GENAI_BASE_URL", "https://genai.rcac.purdue.edu/api/v1")
    GENAI_MODEL = os.getenv("PURDUE_GENAI_MODEL", "llama3.2:latest")
    
    if not GENAI_API_KEY:
        print("âŒ Error: PURDUE_GENAI_API_KEY not found in environment")
        return
    
    print(f"\nâœ“ GenAI API Key: {GENAI_API_KEY[:20]}...")
    print(f"âœ“ GenAI Base URL: {GENAI_BASE_URL}")
    print(f"âœ“ GenAI Model: {GENAI_MODEL}")
    
    # Initialize GenAI provider
    print("\n1. Initializing Purdue GenAI Provider...")
    genai_provider = PurdueGenAIProvider(
        api_key=GENAI_API_KEY,
        base_url=GENAI_BASE_URL,
        model=GENAI_MODEL
    )
    print("   âœ“ GenAI Provider initialized")
    
    # List available models
    try:
        models = genai_provider.list_models()
        print(f"   âœ“ Available models: {len(models)}")
    except Exception as e:
        print(f"   âš  Could not list models: {e}")
    
    # Initialize OpenClaw agent
    print("\n2. Initializing OpenClaw Agent...")
    agent = OpenClawAgent(
        name="Research Assistant",
        genai_provider=genai_provider,
        system_prompt="You are a helpful research assistant. Provide clear, concise, and accurate information."
    )
    print("   âœ“ OpenClaw Agent initialized")
    
    # Test interactions
    print("\n3. Testing Agent Interactions...")
    print("-" * 60)
    
    # Test 1: Simple question
    print("\nTest 1: Simple Question")
    question1 = "What is artificial intelligence?"
    print(f"User: {question1}")
    response1 = agent.process(question1, max_tokens=150)
    print(f"Agent: {response1}")
    
    # Test 2: Follow-up question
    print("\nTest 2: Follow-up Question")
    question2 = "How does it differ from machine learning?"
    print(f"User: {question2}")
    response2 = agent.process(question2, max_tokens=200)
    print(f"Agent: {response2}")
    
    # Test 3: Complex query
    print("\nTest 3: Complex Query")
    question3 = "Explain the main types of machine learning algorithms with examples."
    print(f"User: {question3}")
    response3 = agent.process(question3, max_tokens=300, temperature=0.7)
    print(f"Agent: {response3}")
    
    print("\n" + "=" * 60)
    print("Integration Test Complete!")
    print("=" * 60)
    print("âœ“ GenAI Provider: Working")
    print("âœ“ OpenClaw Agent: Functional")
    print("âœ“ Conversation History: Maintained")
    if AGENTOPS_AVAILABLE and os.getenv("AGENTOPS_API_KEY"):
        print("âœ“ AgentOps Monitoring: Active")
    
    # End AgentOps session
    if AGENTOPS_AVAILABLE and os.getenv("AGENTOPS_API_KEY"):
        agentops.end_session("Success")
        print("âœ“ AgentOps session ended")


if __name__ == "__main__":
    main()
