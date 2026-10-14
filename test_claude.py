import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

model = os.getenv("AGENT_MODEL", "claude-sonnet-4-20250514")
client = ChatAnthropic(model=model, api_key=os.getenv("ANTHROPIC_API_KEY"))

reply = client.invoke("Say hello in one sentence.")
print("CLAUDE REPLY:", reply.content)