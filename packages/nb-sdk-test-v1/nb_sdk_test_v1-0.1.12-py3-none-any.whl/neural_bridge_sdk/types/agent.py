from enum import Enum
from typing import List

from pydantic import BaseModel


class AgentType(str, Enum):
  AGENT = "agent"
  MULTI_AGENT = "multi-agent"
  CODE_AGENT = "code-agent"
  LANGGRAPH_AGENT = "langgraph-agent"


class ReleaseEnvironment(str, Enum):
  DEV = "dev"
  PROD = "prod"
  LOCAL = "local"


class AgentConfig(BaseModel):
  name: str
  description: str
  enabled_envs: List[ReleaseEnvironment] = []
  readme: str = ""
  conversation_starters: List[str] = []


class AgentSpec(BaseModel):
  agent_id: str
  agent_config: AgentConfig
  agent_type: AgentType
  tools: List[str]
  llms: List[str]
  tool_snippets: str
