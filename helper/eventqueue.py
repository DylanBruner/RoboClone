import threading, time
from api.events.event import Event

class EventQueue:
    def __init__(self):
        self._events = []
        self._consumers = {}
        self._alive = True
    
    def push(self, event: Event) -> None:
        print("Pushing", event.__class__)
        self._events.append(event)
    
    def register(self, consumer_func: callable, event: Event) -> None:
        print("Registering", consumer_func, "for", event.__class__)
        self._consumers.setdefault(event.__class__, []).append(consumer_func)

    def _run(self) -> None:
        while self._alive:
            if len(self._events) < 1: continue
            event = self._events.pop(0)
            for consumer in self._consumers.get(type(event), []):
                consumer(event)
            
            time.sleep(0.1)

    def run(self) -> None:
        threading.Thread(target=self._run, daemon=True).start()