from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # Using Annotated with operator .add ensures that messages
    # are appended to the history rather than replaced._AddableT1
    messages: Annotated[List[dict], operator.add]
    current_query: str
    documents: List[dict]
    plan: List[str]
    execution_steps: Annotated[List[dict], operator.add]
    status: str
    final_answer: str

    
