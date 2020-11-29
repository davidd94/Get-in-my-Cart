import asyncio
import sys


def get_event_loop():
    """Get loop of asyncio"""
    if sys.platform == "win32":
        return asyncio.ProactorEventLoop()
    return asyncio.new_event_loop()
