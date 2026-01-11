"""
Chainlit application - varies by project type
"""
import chainlit as cl
from chainlit.context import get_context
from chainlit.types import ThreadDict
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
import httpx
from src.config import API_BASE_URL, DATABASE_URL
from src.auth import login


## ----------------------
## Connect to database
## ----------------------
@cl.data_layer
def data_layer():
    return SQLAlchemyDataLayer(
        conninfo=DATABASE_URL,
    )


## ----------------------
## Authentication
## ----------------------
@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    # Call backend for authentication
    try:
        payload = await login(username, password)
    except httpx.HTTPStatusError:
        return None
    
    user = payload.get("user", None)
    identifier = user.pop("username")

    access = payload.get("tokens", None)
    user.update(access)

    return cl.User(
        identifier=identifier,
        metadata=user
    )




{% if cookiecutter.project_type == 'rag' %}
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome! Ask me questions and I'll search our knowledge base.").send()
    ctx = get_context()
    user = getattr(ctx.session, "user", None)
    identifier = user.identifier if user else "anonymous"
    metadata = user.metadata if user else {}
    cl.user_session.set("user_identifier", identifier)
    cl.user_session.set("role", metadata.get("role", "analyst"))  # Must be "analyst" or "compliance"
    cl.user_session.set("access_token", metadata.get("access_token", None))
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])

    


@cl.on_message
async def on_message(message: cl.Message):
    # ------- Get User Session ------

    ## Get conversation thread id
    thread_id = cl.context.session.thread_id

    # Store user message
    role =  cl.user_session.get("role")

    history = cl.user_session.get("history")
    context =  cl.user_session.get("context")

    # Access Token
    access = cl.user_session.get("access_token")
    if not access:
        await cl.Message("Not authenticated. Please log in again.").send()
        return


    """Handle RAG queries"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/ask",
                json={"question": message.content, "k": 5},
                headers={"Authorization": f"Bearer {access}"},
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
    ctx = get_context()
    user = getattr(ctx.session, "user", None)
    identifier = user.identifier if user else "anonymous"
    metadata = user.metadata if user else {}
    cl.user_session.set("user_identifier", identifier)
    cl.user_session.set("role", metadata.get("role", "analyst"))  # Must be "analyst" or "compliance"
    cl.user_session.set("access_token", metadata.get("access_token", None))
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])
    await cl.Message(content="Hello! How can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    # ------- Get User Session ------

    ## Get conversation thread id
    thread_id = cl.context.session.thread_id

    # Store user message
    role =  cl.user_session.get("role")

    history = cl.user_session.get("history")
    context =  cl.user_session.get("context")

    # Access Token
    access = cl.user_session.get("access_token")
    if not access:
        await cl.Message("Not authenticated. Please log in again.").send()
        return

    """Handle chat messages"""
    history = cl.user_session.get("history", [])
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE_URL}/chat",
                json={"message": message.content, "history": history},
                headers={"Authorization": f"Bearer {access}"},
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
    ctx = get_context()
    user = getattr(ctx.session, "user", None)
    identifier = user.identifier if user else "anonymous"
    metadata = user.metadata if user else {}
    cl.user_session.set("user_identifier", identifier)
    cl.user_session.set("role", metadata.get("role", "analyst"))  # Must be "analyst" or "compliance"
    cl.user_session.set("access_token", metadata.get("access_token", None))
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])


@cl.on_message
async def on_message(message: cl.Message):
    # ------- Get User Session ------

    ## Get conversation thread id
    thread_id = cl.context.session.thread_id

    # Store user message
    role =  cl.user_session.get("role")

    history = cl.user_session.get("history")
    context =  cl.user_session.get("context")

    # Access Token
    access = cl.user_session.get("access_token")
    if not access:
        await cl.Message("Not authenticated. Please log in again.").send()
        return



    """Handle agent tasks"""
    async with httpx.AsyncClient() as client:
        try:
            msg = cl.Message(content="🔄 Working on your task...")
            await msg.send()
            
            response = await client.post(
                f"{API_BASE_URL}/agent",
                json={"task": message.content},
                headers={"Authorization": f"Bearer {access}"},
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
    ctx = get_context()
    user = getattr(ctx.session, "user", None)
    identifier = user.identifier if user else "anonymous"
    metadata = user.metadata if user else {}
    cl.user_session.set("user_identifier", identifier)
    cl.user_session.set("role", metadata.get("role", "analyst"))  # Must be "analyst" or "compliance"
    cl.user_session.set("access_token", metadata.get("access_token", None))
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])


@cl.on_message
async def on_message(message: cl.Message):
    """Handle multi-agent tasks"""
    # ------- Get User Session ------

    ## Get conversation thread id
    thread_id = cl.context.session.thread_id

    # Store user message
    role =  cl.user_session.get("role")

    history = cl.user_session.get("history")
    context =  cl.user_session.get("context")

    # Access Token
    access = cl.user_session.get("access_token")
    if not access:
        await cl.Message("Not authenticated. Please log in again.").send()
        return


    async with httpx.AsyncClient() as client:
        try:
            msg = cl.Message(content="🤖 Coordinating agents...")
            await msg.send()
            
            response = await client.post(
                f"{API_BASE_URL}/multi-agent",
                json={"task": message.content},
                headers={"Authorization": f"Bearer {access}"},
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



## ----------------------
## Load historical chart
## ----------------------
@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    cl.user_session.set("conversation_id", thread["id"])