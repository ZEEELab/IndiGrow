class IndiEvent:
    """
    Class responsible for checking if event should trigger - contains a subclass which
    has a __run_handler__ function and potentially some state.
    """
    
    def __init__(self, subclass, first_trigger, trigger_every):
        self.subclass = subclass
        self.first_trigger = first_trigger
        self.trigger_every = trigger_every

    def __run_handler__(self, step):
        """
        Check to see if it is time for the event to trigger, if so, call the event function.
        """
        if self.first_trigger <= step and step % self.trigger_every == 0:
            self.subclass.__run_handler__()