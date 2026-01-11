"""
Chainlit application - varies by project type
"""
import chainlit as cl
import httpx
import os

API_BASE_URL = os.environ.get("API_BASE_URL", "http://api:8000")

{% if cookiecutter.project_type == 'rag' %}
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome! Ask me questions and I'll search our knowledge base.").send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle RAG queries"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/ask",
                json={"question": message.content, "k": 5},
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            
            answer = data.get("answer", "No response")
            citations = data.get("citations", [])
            
            await cl.Message(content=answer).send()
            
            if citations:
                citation_text = "\n".join([f"- {c['title']}: {c['text'][:100]}..." for c in citations])
                await cl.Message(content=f"**Sources:**\n{citation_text}").send()
                
        except Exception as e:
            await cl.Message(content=f"Error: {e}").send()

{% elif cookiecutter.project_type == 'chatbot' %}
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! How can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle chat messages"""
    history = cl.user_session.get("history", [])
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/chat",
                json={"message": message.content, "history": history},
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            
            answer = data.get("response", "No response")
            history.append({"role": "user", "content": message.content})
            history.append({"role": "assistant", "content": answer})
            cl.user_session.set("history", history[-20:])  # Keep last 20 messages
            
            await cl.Message(content=answer).send()
                
        except Exception as e:
            await cl.Message(content=f"Error: {e}").send()

{% elif cookiecutter.project_type == 'agent' %}
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="I'm an AI agent with tools. Give me a task to complete!").send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle agent tasks"""
    async with httpx.AsyncClient() as client:
        try:
            msg = cl.Message(content="🔄 Working on your task...")
            await msg.send()
            
            response = await client.post(
                f"{API_BASE_URL}/agent",
                json={"task": message.content},
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            
            result = data.get("result", "No result")
            reasoning = data.get("reasoning", "")
            tool_calls = data.get("tool_calls", [])
            
            msg.content = f"**Result:** {result}"
            if reasoning:
                msg.content += f"\n\n**Reasoning:** {reasoning}"
            if tool_calls:
                tools_used = ", ".join([t.get("name", "unknown") for t in tool_calls])
                msg.content += f"\n\n**Tools used:** {tools_used}"
            await msg.update()
                
        except Exception as e:
            await cl.Message(content=f"Error: {e}").send()

{% elif cookiecutter.project_type == 'multi_agent' %}
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="I'm a multi-agent system. Describe your complex task!").send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle multi-agent tasks"""
    async with httpx.AsyncClient() as client:
        try:
            msg = cl.Message(content="🤖 Coordinating agents...")
            await msg.send()
            
            response = await client.post(
                f"{API_BASE_URL}/multi-agent",
                json={"task": message.content},
                timeout=180.0
            )
            response.raise_for_status()
            data = response.json()
            
            result = data.get("result", "No result")
            agent_outputs = data.get("agent_outputs", {})
            
            msg.content = f"**Final Result:**\n{result}"
            await msg.update()
            
            if agent_outputs:
                for agent, output in agent_outputs.items():
                    await cl.Message(content=f"**{agent.title()} Agent:**\n{output[:500]}...").send()
                
        except Exception as e:
            await cl.Message(content=f"Error: {e}").send()

{% endif %}
