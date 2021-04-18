import winsound

class Sequencer:

    def __init__(self, start_state):
        self.data = start_state['data']
        self.count = start_state['count']

        self.input_data = {}
        self.output_data = {}

        for key, item in self.data.items():
            self.output_data[key] = None

    def step(self):
        inc_count = True

        for key, item in self.data.items():
            self.output_data[key] = item[self.count]
            if self.count + 1 >= len(item):
                inc_count = False

        if inc_count:
            self.count += 1
        else:
            self.count = 0

    def input(self, port, value):
        self.input_data[port] = value

    def output(self, port):
        return self.output_data[port] 
        
class Beeper:

    def __init__(self, start_state):
        self.default_length = 250
        self.default_freq = 0

        self.input_data = {'freq':None, 'length':None}
        self.output_data = {}

    def step(self):
        freq = self.input_data['freq']
        if freq == None:
            freq = self.default_freq
        
        length = self.input_data['length']
        if length == None:
            length = self.default_length
        
            
        winsound.Beep(int(440 * 2 ** (freq/12)), length)

    def input(self, port, value):
        self.input_data[port] = value

    def output(self, port):
        return self.output_data[port] 