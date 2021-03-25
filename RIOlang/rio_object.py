class RIO_Object():


    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', None)
        self.max_registers = kwargs.get('max_registers', 8)
        self.max_com = kwargs.get('max_com', 8)
        self.register = []
        self.com = []
        self.instance = self.program_runner()

    def run_tick(self):
        next(self.instance)

    def program_runner(self):
        file_handle = open(self.filename, "rb")
        file_bytes = list(file_handle.read())
        file_handle.close()
        while len(file_bytes) < 255:
            file_bytes += [0]
        print(len(file_bytes))
        print(file_bytes)
        yield
        #for n, b in enumerate(file_bytes):
        #    if n % 4 == 0:
        #        print("----")
        #    yield
        #    print("{0:08b}".format(b))


computer = RIO_Object(filename = "test.rb")
while True:
    computer.run_tick()

