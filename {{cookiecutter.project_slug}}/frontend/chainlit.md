# Welcome to {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

{% if cookiecutter.project_type == 'rag' %}
Ask me questions and I'll search our knowledge base to find answers with citations.
{% elif cookiecutter.project_type == 'chatbot' %}
I'm here to chat! Ask me anything.
{% elif cookiecutter.project_type == 'agent' %}
I'm an AI agent with tools. Give me a task and I'll work on it!
{% elif cookiecutter.project_type == 'multi_agent' %}
I coordinate multiple AI agents to tackle complex tasks. Describe what you need!
{% endif %}
