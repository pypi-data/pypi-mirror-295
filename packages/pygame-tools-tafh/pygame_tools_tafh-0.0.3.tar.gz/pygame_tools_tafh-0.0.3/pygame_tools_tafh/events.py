class events:

    _events = []

    @staticmethod
    def set(events):
        events._events = events

    @staticmethod
    def get():
        return events._events