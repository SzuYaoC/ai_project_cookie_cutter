#!/usr/bin/env python
"""Post-generation hook to clean up unused MCP services based on project_type."""

import os
import shutil

PROJECT_TYPE = "{{ cookiecutter.project_type }}"

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


def remove_empty_docs_dir():
    """Remove empty docs directory if it exists."""
    docs_dir = os.path.join(os.getcwd(), "docs")
    if os.path.exists(docs_dir) and not os.listdir(docs_dir):
        os.rmdir(docs_dir)


if __name__ == "__main__":
    remove_unused_mcp_services()
    remove_empty_docs_dir()
    print(f"\n✓ Project generated successfully for type: {PROJECT_TYPE}")
