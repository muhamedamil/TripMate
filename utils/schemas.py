from typing import Literal
from pydantic import BaseModel, Field

class NextStep(BaseModel):
    """
    It represents the supervisor's decision on which agent should act next.
    """
    next_actor: Literal["TransportAgent", "HotelAgent", "ItineraryAgent", "FINISH"] = Field(
        ...,
        description="The next agent to call or 'FINISH' if the user's request is fully satisfied.",
    )
    