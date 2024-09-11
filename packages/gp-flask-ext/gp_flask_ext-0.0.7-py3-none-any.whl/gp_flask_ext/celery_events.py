import threading
from loguru import logger

class Monitor(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.state = app.events.State()
        self.should_stop = False
        self.daemon = True

    def run(self):
        with self.app.connection() as connection:
            recv = self.app.events.Receiver(connection, handlers={
                '*': self.on_event,
            })
            recv.capture(limit=None, timeout=None, wakeup=True)

    def on_event(self, event):
        self.state.event(event)
        event_type = event['type']
        if event_type.startswith('task-'):
            logger.info(f"Received event: {event}")