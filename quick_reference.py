#!/usr/bin/env python3
"""
Quick reference for LLM Knowledge Base operations.

Run this file to see available commands and current system status.
"""

import subprocess
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_section(title, items):
    print(f"\n{title}:")
    for item in items:
        print(f"  • {item}")

def check_env():
    """Check if .env is configured"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("   Copy .env.example to .env and add your ANTHROPIC_API_KEY")
        return False
    
    env_content = env_file.read_text()
    if "sk-" not in env_content and "your_api_key" in env_content:
        print("⚠️  ANTHROPIC_API_KEY not set in .env!")
        print("   Add your API key from https://console.anthropic.com")
        return False
    
    return True

def main():
    print_header("🧠 LLM Knowledge Base Quick Reference")
    
    # Check setup
    if check_env():
        print("✅ Configuration looks good!\n")
    
    # Getting started
    print_section("Getting Started", [
        "1. cd cli && python main.py init",
        "2. cd .. && python create_examples.py",
        "3. ./start.sh (or start.bat on Windows)",
        "4. Open frontend/index.html in browser",
        "5. cd cli && python main.py --help"
    ])
    
    # CLI Commands
    print_section("CLI Commands", [
        "init - Initialize knowledge base directories",
        "compile [SOURCE] - Compile a single document",
        "compile-all - Compile all raw documents",
        "search [QUERY] - Search the wiki",
        "query [QUESTION] - Ask a question",
        "summarize [TOPIC] - Generate a summary",
        "index - Generate wiki index",
        "health - Check system status"
    ])
    
    # API Endpoints
    print_section("API Endpoints (http://localhost:8000)", [
        "POST /qa/query - Ask a question",
        "POST /search - Search documents",
        "POST /wiki/compile - Compile a document",
        "POST /wiki/compile-all - Compile all",
        "GET /wiki/index - Get wiki index",
        "GET /wiki/backlinks - Get article links",
        "GET /health - System status"
    ])
    
    # Directories
    print_section("Key Directories", [
        "data/raw/ - Raw source documents",
        "data/wiki/ - Compiled wiki articles",
        "data/output/ - Query results",
        "backend/ - FastAPI server",
        "cli/ - Command-line interface",
        "frontend/ - Web UI"
    ])
    
    # Documentation
    print_section("Documentation Files", [
        "README.md - Complete guide",
        "QUICKSTART.md - 5-minute setup",
        "DEVELOPMENT.md - Architecture",
        "SCALING.md - Performance tips",
        "PROJECT_MANIFEST.md - Full project details"
    ])
    
    # Tips
    print_section("Pro Tips", [
        "Use web UI for interactive exploration",
        "Use CLI for automation and scripting",
        "Use API for programmatic access",
        "Check SCALING.md for wikis > 500 articles",
        "Outputs saved to data/output/ for review"
    ])
    
    print_header("Ready to get started?")
    print("cd llm-knowledge-base")
    print("python quick_reference.py  # Run this anytime for help\n")

if __name__ == "__main__":
    main()
