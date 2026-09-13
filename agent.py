from strands import Agent, tool
from strands_tools import calculator, current_time
from strands.vended_tools import http_request
from strands.models.openai import OpenAIModel
from strands_tools import use_computer

model = OpenAIModel(
    client_args={
        "api_key": "5c68e1e7-a36d-4ccd-bdae-39a8d8f7a3d9",
        "base_url": "https://api.nova.amazon.com/v1"
    },
    # **model_config
    model_id="nova-2-lite-v1",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)
CLOSEPILOT_SYSTEM_PROMPT = """You are a helpful assistant that can answer questions and perform tasks for the user. You have access to the following tools: calculator, current_time, http_request, computer_use. Use these tools to help you answer questions and perform tasks for the user."""
CLOSEPILOT_TOOLS = [computer_use, calculator, current_time, http_request]

agent = Agent(
            system_prompt=CLOSEPILOT_SYSTEM_PROMPT,
            model=model,
            tools=CLOSEPILOT_TOOLS,
        )


print("Agent initialized with the following tools:")
result = agent("List the tools available to you and their descriptions.")
print(result)
