class events:

    _events = []

    @staticmethod
    def set(oevents):
        events._events = oevents

    @staticmethod
    def get():
        return events._events