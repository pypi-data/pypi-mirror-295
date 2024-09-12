from typing import List

import requests

from .types.agent import AgentSpec
from .types.feedback import Feedback, FeedbackInput
from .types.llm import LLM
from .types.run import RunResult
from .types.tool import Tool


class NeuralBridge:
  def __init__(self, base_url: str):
    self.base_url = base_url

  def list_agents(self) -> List[AgentSpec]:
    """Retrieve a list of tasks."""
    url = f"{self.base_url}/list-tasks/"
    response = requests.get(url)
    response.raise_for_status()
    return [AgentSpec.model_validate(item) for item in response.json()]

  def list_tools(self) -> List[Tool]:
    """Retrieve a list of tools."""
    url = f"{self.base_url}/list-tools/"
    response = requests.get(url)
    response.raise_for_status()
    return [Tool.model_validate(item) for item in response.json()]

  def list_llms(self) -> List[LLM]:
    """Retrieve a list of large language models (LLMs)."""
    url = f"{self.base_url}/list-llms/"
    response = requests.get(url)
    response.raise_for_status()
    return [LLM.model_validate(item) for item in response.json()]

  def run_agent(self, agent_id: str, query: str) -> RunResult:
    """Run a specific task with the given query."""
    url = f"{self.base_url}/run-agent/{agent_id}/"
    response = requests.get(url, params={"query": query})
    response.raise_for_status()
    result_data = response.json()
    if "run_id" in result_data and "output" in result_data:
      return RunResult(run_id=result_data["run_id"], output=result_data["output"])
    else:
      raise ValueError("Response JSON does not contain the expected keys 'run_id' and 'output'")

  def add_feedback(self, feedback_input: FeedbackInput) -> Feedback:
    """Add feedback for a task run."""
    url = f"{self.base_url}/add-feedback/"
    response = requests.post(url, json=feedback_input.model_dump())
    response.raise_for_status()
    return Feedback.model_validate(response.json())
