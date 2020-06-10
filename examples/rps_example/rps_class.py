class rps_class:
    beats = {'rock' : 'scissors',
             'paper' : 'rock',
             'scissors' : 'paper'}
    def __init__(self, rps_type):
        self.type = rps_type
        self.__IndiGrow__ = None

    def __fitness__(self):
        self.__IndiGrow__.mark_as_dirty(all_dirty=True)
        beat_type = self.beats[self.type]
        beat_node = self.__IndiGrow__.find_all_attributes({'type':beat_type})
        return beat_node[0]['frequency']

    def __mutate__(self):
        pass