"""Few-shot guided password generator demonstrating structured prompting and parameter tuning."""

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable

from shared.python.utils.model_factory import get_chat_model
from shared.python.utils.env_loader import load_project_env
from shared.prompts.system_prompts import PASSWORD_GENERATION_PROMPT

load_project_env()

FEW_SHOT_PASSWORD_TEMPLATE = """Input: cat
Output:
C@t5xRm2k
cA7t!nKp3
cAt3$wLz9

Input: moonlight
Output:
m00nL!ght4
M0onl1Gh@3
m0OnL!9htx

Input: robot
Output:
r0B0t!Kx3
R0b0T@j7n
r0b#T5wNk

Input: {input_password}
Output:"""


def create_password_chain(llm: BaseChatModel | None = None, use_few_shot: bool = True) -> RunnableSerializable:
    """
    Creates an LCEL chain for password generation.
    
    Args:
        llm: Chat model instance.
        use_few_shot: If True, uses the few-shot template; otherwise uses structured instructions.
        
    Returns:
        RunnableSerializable: LCEL chain.
    """
    model = llm or get_chat_model(provider="ollama", model_name="gemma3:1b", temperature=0.2)
    template_str = FEW_SHOT_PASSWORD_TEMPLATE if use_few_shot else PASSWORD_GENERATION_PROMPT
    prompt = PromptTemplate(input_variables=["input_password"], template=template_str)
    
    return prompt | model


def generate_password(input_password: str, llm: BaseChatModel | None = None, use_few_shot: bool = True) -> str:
    """
    Generates 3 secure, readable passwords based on an inspiration word.
    
    Args:
        input_password: Base seed word.
        llm: Optional chat model.
        use_few_shot: Whether to apply few-shot prompt framing.
        
    Returns:
        str: Generated passwords formatted one per line.
    """
    chain = create_password_chain(llm=llm, use_few_shot=use_few_shot)
    response = chain.invoke(input={"input_password": input_password})
    if isinstance(response, BaseMessage):
        return str(response.content).strip()
    return str(response).strip()
