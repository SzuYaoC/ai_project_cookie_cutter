import yaml
import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

def load_prompt_from_yaml(filepath: str) -> ChatPromptTemplate:
    """
    Load a prompt from a YAML file.
    The YAML file should define:
    - _type: prompt
    - input_variables: list of variables
    - template: the prompt string
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
        
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)
        
    if config.get("_type") != "prompt":
        raise ValueError("YAML file must define a prompt type")
        
    return ChatPromptTemplate.from_template(config["template"])


def load_chat_prompt(template_str: str) -> ChatPromptTemplate:
    """
    Load a chat prompt from a string template.
    """
    return ChatPromptTemplate.from_template(template_str)


def load_system_prompt(template_str: str) -> ChatPromptTemplate:
    """Load a system prompt"""
    return ChatPromptTemplate.from_messages([
        ("system", template_str),
        ("user", "{input}")
    ])
