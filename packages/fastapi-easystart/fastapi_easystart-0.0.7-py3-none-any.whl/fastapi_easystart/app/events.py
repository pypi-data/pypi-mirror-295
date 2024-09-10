import asyncio
from typing import Callable, Dict, List, Any, Awaitable, Union

ListenerType = Union[Callable[..., None], Callable[..., Awaitable[None]]]


class EventManager:
    def __init__(self):
        self._events: Dict[str, List[ListenerType]] = {}

    def register(self, event_name: str, listener: ListenerType):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(listener)

    def unregister(self, event_name: str, listener: ListenerType):
        if event_name in self._events and listener in self._events[event_name]:
            self._events[event_name].remove(listener)

    def trigger(self, event_name: str, *args: Any, **kwargs: Any):
        if event_name in self._events:
            for listener in self._events[event_name]:
                if asyncio.iscoroutinefunction(listener):
                    asyncio.create_task(listener(*args, **kwargs))
                else:
                    listener(*args, **kwargs)
