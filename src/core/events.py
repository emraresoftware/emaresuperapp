"""
Emare SuperApp — Event Bus
Modüller arası olay tabanlı iletişim sistemi.
"""
from typing import Callable, Dict, List, Any
import asyncio
import logging

logger = logging.getLogger("superapp.events")


class EventBus:
    """Basit async event bus — modüller arası iletişim için."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, handler: Callable):
        """Bir event'e handler kaydet."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.debug(f"Handler registered for '{event_name}'")

    def off(self, event_name: str, handler: Callable):
        """Handler kaydını sil."""
        if event_name in self._handlers:
            self._handlers[event_name] = [
                h for h in self._handlers[event_name] if h != handler
            ]

    async def emit(self, event_name: str, data: Any = None):
        """Event yayınla — tüm handler'ları çalıştır."""
        handlers = self._handlers.get(event_name, [])
        if not handlers:
            return
        logger.info(f"Event '{event_name}' emitted → {len(handlers)} handlers")
        tasks = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(data))
            else:
                handler(data)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


# Singleton instance
event_bus = EventBus()
