# src/globals.py
import asyncio
from typing import Optional

ml_models = {}

# Agent state management
agent_task: Optional[asyncio.Task] = None
agent_running = False
current_ticker = None
