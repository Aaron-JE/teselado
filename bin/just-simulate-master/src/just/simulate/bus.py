import heapq
import random
from collections import defaultdict
from datetime import timedelta
from types import GeneratorType
from typing import Callable, Generator, Optional, Tuple


class Bus(list):
    """Bus."""

    def __init__(self):
        super().__init__()
        self.now = timedelta(0)
        self.subscribers = defaultdict(set)

    def publish(
            self, topic: str,
            data: Optional[dict] = None,
            delay: timedelta = None
    ) -> None:
        """Publish."""
        delay = delay or timedelta(0)
        assert delay >= timedelta(0)
        data = data or dict({})
        randint = random.randint(0, 1_000_000_000)
        event = (self.now + delay, randint, topic, data)
        heapq.heappush(self, event)

    def add_subscription(
            self, topic: str,
            handler: Callable,
            filtering: Optional[Callable] = None
    ) -> None:
        """Add subscription."""
        subscribers = self.subscribers[topic]
        subscribers.add((handler, filtering))

    def has_next(self):
        """Has next."""
        return len(self) > 0

    def scan(self) -> Tuple[Optional[str], Optional[dict]]:
        """Scan."""
        # get event with earliest time
        now, __, topic, data = heapq.heappop(self)
        self.now = now  # advance clock to time of event
        if topic == '__sleep__':
            self._resume_generator(**data)
            return None, None
        subscribers = self.subscribers[topic]
        subscribers |= self.subscribers['*']
        for handler, filtering in subscribers:
            if filtering is None or filtering(data) is True:
                response = handler(data, topic=topic)  # simulate the event
                if isinstance(response, GeneratorType):
                    # support for Env.sleep(timedelta)
                    self._resume_generator(response)

        return topic, data

    def _resume_generator(self, response) -> None:
        """Resume generator."""
        try:
            delay = next(response)
            assert isinstance(delay, timedelta), \
                'Expected `yield Env.sleep(timedelta)`'
            self.publish('__sleep__', {'response': response}, delay)
        except StopIteration:
            pass

    def run(self, until: Optional[timedelta] = None) \
            -> Generator[Tuple[str, dict], None, None]:
        """Run."""
        # get event with earliest time
        while self.has_next() and (until is None or self.now <= until):
            # simulate the event
            topic, data = self.scan()
            yield topic, data
