import json
import asyncio
from typing import Dict, Any
from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator, OrchestratorConfig
from multi_agent_orchestrator.agents import BedrockLLMAgent, BedrockLLMAgentOptions, AgentResponse
from multi_agent_orchestrator.types import ConversationMessage

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator(OrchestratorConfig(
    # Configuration options
))

# Add agents e.g Tech Agent
tech_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
    name="Tech Agent",
    streaming=False,
    description="Specializes in technology areas including software development, hardware, AI, \
            cybersecurity, blockchain, cloud computing, emerging tech innovations, and pricing/costs \
            related to technology products and services.",
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
))

orchestrator.add_agent(tech_agent)

def serialize_agent_response(response: Any) -> Dict[str, Any]:

    text_response = ''
    if isinstance(response, AgentResponse) and response.streaming is False:
        # Handle regular response
        if isinstance(response.output, str):
            text_response = response.output
        elif isinstance(response.output, ConversationMessage):
                text_response = response.output.content[0].get('text')

    """Convert AgentResponse into a JSON-serializable dictionary."""
    return {
        "metadata": {
            "agent_id": response.metadata.agent_id,
            "agent_name": response.metadata.agent_name,
            "user_input": response.metadata.user_input,
            "session_id": response.metadata.session_id,
        },
        "output": text_response,
        "streaming": response.streaming,
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        user_input = event.get('query')
        user_id = event.get('userId')
        session_id = event.get('sessionId')
        response = asyncio.run(orchestrator.route_request(user_input, user_id, session_id))

        # Serialize the AgentResponse to a JSON-compatible format
        serialized_response = serialize_agent_response(response)

        return {
            "statusCode": 200,
            "body": json.dumps(serialized_response)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
