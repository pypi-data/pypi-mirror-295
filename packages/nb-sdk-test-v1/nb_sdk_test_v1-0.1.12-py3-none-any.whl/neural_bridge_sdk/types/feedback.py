from typing import Optional

from pydantic import BaseModel


class FeedbackInput(BaseModel):
  """Server inputs to created a feedback."""

  run_id: str
  metric_name: str
  score: float
  notes: Optional[str] = None


class Feedback(FeedbackInput):
  """Full feedback entry: inputs + feedback id generated on server side."""

  feedback_id: str
