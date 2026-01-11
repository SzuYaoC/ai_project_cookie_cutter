#!/usr/bin/env python
"""Post-generation hook to clean up unused MCP services based on project_type."""

import os
import shutil

import secrets

PROJECT_TYPE = "{{ cookiecutter.project_type }}"
USE_AUTH = "{{ cookiecutter.use_auth }}"
BUILD_FRONTEND = "{{ cookiecutter.build_frontend }}"

# Define which MCP services are needed for each project type
MCP_SERVICES_BY_TYPE = {
    "rag": ["search_server", "ingest_server"],
    "chatbot": ["memory_server"],
    "agent": ["tools_server"],
    "multi_agent": ["tools_server", "coordination_server"],
}

ALL_MCP_SERVICES = [
    "search_server",
    "ingest_server", 
    "memory_server",
    "tools_server",
    "coordination_server",
]


def remove_unused_mcp_services():
    """Remove MCP service directories that are not needed for this project type."""
    mcp_dir = os.path.join(os.getcwd(), "mcp_services")
    
    if not os.path.exists(mcp_dir):
        return
    
    needed_services = MCP_SERVICES_BY_TYPE.get(PROJECT_TYPE, [])
    
    for service in ALL_MCP_SERVICES:
        if service not in needed_services:
            service_path = os.path.join(mcp_dir, service)
            if os.path.exists(service_path):
                shutil.rmtree(service_path)
                print(f"Removed unused MCP service: {service}")


def remove_frontend_if_not_needed():
    """Remove frontend directory if not needed."""
    if BUILD_FRONTEND != "yes":
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        if os.path.exists(frontend_dir):
            shutil.rmtree(frontend_dir)
            print("Removed unused frontend directory")


def remove_auth_if_not_needed():
    """Remove auth-related files if not needed."""
    if USE_AUTH != "yes":
        # Remove backend auth files
        backend_auth = os.path.join(os.getcwd(), "backend", "app", "api", "utils", "auth.py")
        if os.path.exists(backend_auth):
            os.remove(backend_auth)
            print("Removed unused backend auth file")

        backend_security = os.path.join(os.getcwd(), "backend", "app", "api", "utils", "security.py")
        if os.path.exists(backend_security):
            os.remove(backend_security)
            print("Removed unused backend security file")

        # Remove frontend auth file (only if frontend exists)
        if BUILD_FRONTEND == "yes":
            frontend_auth = os.path.join(os.getcwd(), "frontend", "src", "auth.py")
            if os.path.exists(frontend_auth):
                os.remove(frontend_auth)
                print("Removed unused frontend auth file")


def remove_empty_docs_dir():
    """Remove empty docs directory if it exists."""
    docs_dir = os.path.join(os.getcwd(), "docs")
    if os.path.exists(docs_dir) and not os.listdir(docs_dir):
        os.rmdir(docs_dir)


def generate_env_file():
    """Generate .env file from .env.example with secure secrets."""
    env_example = ".env.example"
    env_target = ".env"
    
    if not os.path.exists(env_example):
        print(f"Warning: {env_example} not found, skipping .env generation.")
        return

    # Generate secure secrets
    jwt_secret = secrets.token_urlsafe(32)
    chainlit_secret = secrets.token_urlsafe(32)

    with open(env_example, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("JWT_SECRET_KEY="):
            new_lines.append(f"JWT_SECRET_KEY={jwt_secret}\n")
        elif line.startswith("CHAINLIT_AUTH_SECRET="):
            new_lines.append(f"CHAINLIT_AUTH_SECRET={chainlit_secret}\n")
        else:
            new_lines.append(line)

    with open(env_target, "w") as f:
        f.writelines(new_lines)
    
    print(f"✓ Generated {env_target} with secure secrets")


if __name__ == "__main__":
    remove_unused_mcp_services()
    remove_frontend_if_not_needed()
    remove_auth_if_not_needed()
    remove_empty_docs_dir()
    generate_env_file()
    print(f"\n✓ Project generated successfully for type: {PROJECT_TYPE}")
