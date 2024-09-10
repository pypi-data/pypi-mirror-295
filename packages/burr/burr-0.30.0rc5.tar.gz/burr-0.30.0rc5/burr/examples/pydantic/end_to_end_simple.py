from typing import Optional
import pydantic

from burr.integrations.pydantic import pydantic_action


class ApplicationState(pydantic.BaseModel):
    chat_history: list[dict[str, str]] = pydantic.Field(default_factory=list)
    prompt: Optional[str]=None
    response: Optional[str] =None


@pydantic_action(reads=["chat_history"], writes=["chat_history", "prompt"])
def human_input(state: ApplicationState, ) -> ApplicationState:
    state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    state.prompt = prompt
    return state