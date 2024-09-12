from typing import Any, Dict, List

from typing_extensions import TypedDict

from neural_bridge_sdk.types.message import Message


class RunResult(TypedDict):
  """
  Results for running an agent.
  """

  run_id: str
  messages: List[Message]
  output: Dict[str, Any]
