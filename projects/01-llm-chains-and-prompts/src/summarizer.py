"""Text summarization using LangChain Expression Language (LCEL) and Prompt Templates."""

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable

from shared.python.utils.model_factory import get_chat_model
from shared.python.utils.env_loader import load_project_env
from shared.prompts.system_prompts import SUMMARIZER_PROMPT_TEMPLATE

load_project_env()


def create_summarization_chain(llm: BaseChatModel | None = None) -> RunnableSerializable:
    """
    Creates an LCEL summarization chain composed of a PromptTemplate and a ChatModel.
    
    Args:
        llm: Optional chat model instance. If not provided, defaults to local Ollama.
        
    Returns:
        RunnableSerializable: Executable LCEL chain.
    """
    model = llm or get_chat_model(provider="ollama", model_name="gemma4:e2b", temperature=0.2)
    prompt = PromptTemplate(input_variables=["text"], template=SUMMARIZER_PROMPT_TEMPLATE)
    
    # LCEL Composition: PromptTemplate | ChatModel
    return prompt | model


def summarize_text(text: str, llm: BaseChatModel | None = None) -> str:
    """
    Summarizes given text and extracts key findings.
    
    Args:
        text: Input text string to summarize.
        llm: Optional LLM model instance.
        
    Returns:
        str: Summarized response content.
    """
    chain = create_summarization_chain(llm=llm)
    response = chain.invoke(input={"text": text})
    if isinstance(response, BaseMessage):
        return str(response.content)
    return str(response)
