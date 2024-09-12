from pydantic import BaseModel


class Tool(BaseModel):
  """Represents a tool."""

  name: str
  description: str
  url: str
