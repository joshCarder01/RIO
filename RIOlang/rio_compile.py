class Command:

    def __init__(self, **kwargs):
        # Creating properties kwargs.get(property, default_value)
        
        # string name
        self.cmd_str = kwargs.get('cmd_str', None)

        # default bytes
        self.cmd_b = kwargs.get('cmd_b', None)
        self.flg_b = kwargs.get('flg_b', None)
        self.reg_b = kwargs.get('reg_b', None)
        self.pld_b = kwargs.get('pld_b', None)

        # format how args will be compiled and collected
        self.flg_f = kwargs.get('flg_f', None)
        self.arg_f = kwargs.get('arg_f', None)

        # options for flag group
        self.flg_o = kwargs.get('flg_o', None)

commands = {
    
    # Debug
    'prt' :Command(cmd_str = 'prt',  cmd_b = 0x01, flg_f = ['0','flag:i','flag:c','RF1'], arg_f = ['f','DATA1']),
    
    # Logic
    'and' :Command(cmd_str = 'and',  cmd_b = 0x10, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'not' :Command(cmd_str = 'not',  cmd_b = 0x11, flg_f = ['0','DR','RF1','0'],   arg_f = ['DR','DATA1']),
    'or'  :Command(cmd_str = 'or',   cmd_b = 0x12, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'bsl' :Command(cmd_str = 'bsl',  cmd_b = 0x13, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'bsr' :Command(cmd_str = 'bsr',  cmd_b = 0x14, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'xor' :Command(cmd_str = 'xor',  cmd_b = 0x15, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),

    # Math
    'add' :Command(cmd_str = 'add',  cmd_b = 0x20, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'sub' :Command(cmd_str = 'sub',  cmd_b = 0x21, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'mul' :Command(cmd_str = 'mul',  cmd_b = 0x22, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'div' :Command(cmd_str = 'div',  cmd_b = 0x23, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'mod' :Command(cmd_str = 'mod',  cmd_b = 0x24, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),

    # Branch
    'br'  :Command(cmd_str = 'br',   cmd_b = 0x30, flg_f = ['0','flag:p','flag:n','flag:z'], arg_f = ['f','AD']),
    'jmp' :Command(cmd_str = 'jmp',  cmd_b = 0x31, flg_f = ['0','SR','0','0'], arg_f = ['SR']),
    'ret' :Command(cmd_str = 'ret',  cmd_b = 0x31, flg_f = ['0','1','0','0'], reg_b = 7),
    'jsr' :Command(cmd_str = 'jsr',  cmd_b = 0x32, flg_f = ['1','0','0','0'], arg_f = ['AD']),
    'jsrr':Command(cmd_str = 'jsrr', cmd_b = 0x32, flg_f = ['0','SR','0','0'], arg_f = ['SR']),
    'end' :Command(cmd_str = 'end',  cmd_b = 0x33, flg_f = ['0','SR','0','0'], arg_f = ['SR']),
    
    # Load/Store
    'ld'  :Command(cmd_str = 'ld',   cmd_b = 0x40, flg_f = ['0','DR','0','0'], arg_f = ['DR','AD']),
    'ldi' :Command(cmd_str = 'ldi',  cmd_b = 0x41, flg_f = ['0','DR','0','0'], arg_f = ['DR','AD']),
    'ldr' :Command(cmd_str = 'ldr',  cmd_b = 0x42, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA1','DATA2']),
    'lea' :Command(cmd_str = 'lea',  cmd_b = 0x43, flg_f = ['0','DR','0','0'], arg_f = ['DR','AD']),
    'st'  :Command(cmd_str = 'st',   cmd_b = 0x44, flg_f = ['0','SR','0','0'], arg_f = ['SR','AD']),
    'sti' :Command(cmd_str = 'sti',  cmd_b = 0x45, flg_f = ['0','SR','0','0'], arg_f = ['SR','AD']),
    'str' :Command(cmd_str = 'str',  cmd_b = 0x46, flg_f = ['0','SR','RF1','RF2'], arg_f = ['SR','DATA1','DATA2']),
    #'fill':None,#Command(cmd_str = 'fill', cmd_b = 0x47, flg_f = ['0','SR','RF1','RF2'], arg_f = ['SR','DATA1','DATA2']),

    # IO
    'sbr' :Command(cmd_str = 'sbr',  cmd_b = 0x50, flg_f = ['0','DR','RF1','0'], arg_f = ['DR','DATA1']),
    'sbw' :Command(cmd_str = 'sbw',  cmd_b = 0x51, flg_f = ['0','SR','RF1','0'], arg_f = ['SR','DATA1']),    


}

def is_valid_hex(num_string):
    try:
        return num_string[0] == 'x' and int(num_string[1:], 16) < 256
    except:
        return False

def is_valid_bin(num_string):
    try:
        return num_string[0] == 'b' and int(num_string[1:], 2) < 256
    except:
        return False

def is_valid_dec(num_string):
    try:
        return num_string[0] == '#' and int(num_string[1:]) < 256
    except:
        return False

def is_valid_reg(reg_string, max_registers = 8):
    try:
        return reg_string[0] == 'r' and int(reg_string[1:]) < max_registers
    except:
        return False

def is_valid_num(num_string):
    return is_valid_hex(num_string) or is_valid_dec(num_string) or is_valid_bin(num_string)

def num_to_int(str_num):
    if isinstance(str_num, str):
        if is_valid_hex(str_num):
            return int(str_num[1:],16)
        elif is_valid_bin(str_num):
            return int(str_num[1:],2)
        elif is_valid_dec(str_num):
            return int(str_num[1:])
        elif is_valid_reg(str_num):
            return int(str_num[1:])
        else:
            return False
    else:
        return False

def print_bytes(bytea, split = 4):
    for n, b in enumerate(bytea):
        print("{0:08b}".format(b), end = ' ')
        if (n + 1) % split == 0:
            print()
        
        


def to_token_list(filename):
    cmd_list = []
    data_list = []
    data_bytes = bytearray()
    label_dict = {}

    found_end = False
    end_index = 0

    file_handle = open(filename, 'r')
    for line in file_handle:

        # get items
        cmd_list += [line.replace(',', ' ').lower().strip().split(";")[0].split()]
        # disregard if empty line
        if not cmd_list[-1]:
            cmd_list.pop()
        # find the end
        if 'end' in cmd_list[-1]:
            found_end = True
            end_index = len(cmd_list)
        # gather all hardcoded value saving
        if 'fill' in cmd_list[-1] or 'blkw' in cmd_list[-1] or 'strz' in cmd_list[-1]:
            data_list += [cmd_list.pop()]

    if not found_end:
        return ("ERROR:no end found",0,0)

    # convert all larger blocks to fills
    for line_number, line in enumerate(data_list):
        if 'blkw' in line and num_to_int(line[line.index('blkw') + 1]):
            for _ in range(num_to_int(line[line.index('blkw') + 1]) - 1):
                data_list.insert(line_number + 1, ['fill', '#0'])
            data_list[line_number][line.index('blkw') + 1] = '#0'
            data_list[line_number][line.index('blkw')] = 'fill'

        if 'strz' in line:
            for c in line[line.index('strz') + 1][:0:-1]:
                data_list.insert(line_number + 1, ['fill', '#' + str(ord(c))])
            data_list[line_number][line.index('strz') + 1] = '#' + str(ord(line[line.index('strz') + 1][0]))
            data_list[line_number][line.index('strz')] = 'fill'

    for line_number, line in enumerate(cmd_list):
        if line[0] not in commands:
            label_dict[line[0]] = line_number * 2
            cmd_list[line_number] = cmd_list[line_number][1:]

    for line_number, line in enumerate(data_list):
        if line[0] != 'fill':
            label_dict[line[0]] = line_number + (end_index * 2)
            data_list[line_number] = data_list[line_number][1:]

    for line in data_list:
        data_bytes.append(num_to_int(line[-1]))

    #print_bytes(data_bytes, split=2)

    #print(label_dict)


    return (cmd_list, label_dict, data_bytes)

def to_bytes(token_list, label_dict):
    return_bytes = bytearray()
    command_obj = None

    # Errror if there is still no command
    if token_list[0] not in commands:
        return "ERROR: command not found"
    else:
        command_obj = commands[token_list[0]]


    return_bytes.append(command_obj.cmd_b)

    # setup min and max number of expected args
    max_args = len(token_list[1:])
    min_args = 0
    for arg in command_arg_f[1:]:
        if arg != 'DR' or arg != 'f':
            min_args += 1

    if len(token_list[1:]) < min_args or len(token_list[1:]) > max_args:
        return "ERROR: bad number of args"

    if len(token_list[1:]) == min_args:
        command_obj.arg_f.remove('DR')
        command_obj.arg_f.remove('f')

    # if there is data for flg_b, use it
    if not command_obj.flg_b == None:
        return_bytes.append(command_obj.flg_b)
    else:
        '''
        args in = [#3,#3]
        args ex = [DR,n ,n ]
        flags   = [DR,rf,rf]
        '''
        flag_bytes = 0
        payload_bytes = 0
        for arg_number, arg in command_obj.arg_f:
            
            if arg == 'DR' and is_valid_reg(token_list[arg_number]):
                flag_bytes += (1 << 4 - command_obj.flag_f.index('DR') - 1)
            elif arg == 'DR':
                return 'ERROR: expected register'

            elif arg == 'SR' and is_valid_reg(token_list[arg_number]):
                flag_bytes += (1 << 4 - command_obj.flag_f.index('SR') - 1)
            elif arg == 'SR':
                return 'ERROR: expected register'

            elif arg == 'DATA1' and is_valid_reg(token_list[arg_number]):
                flag_bytes += (1 << 4 - command_obj.flag_f.index('RF1') - 1)
                payload_bytes += (num_to_int(token_list[arg_number]) << 4)
            elif arg == 'DATA1' and is_valid_num(token_list[arg_number]):
                payload_bytes += (num_to_int(token_list[arg_number]) << 4)
            elif arg == 'DATA1':
                return 'ERROR: expected register or num'

            elif arg == 'DATA2' and is_valid_reg(token_list[arg_number]):
                flag_bytes += (1 << 4 - command_obj.flag_f.index('RF2') - 1)
                payload_bytes += (num_to_int(token_list[arg_number]))
            elif arg == 'DATA2' and is_valid_num(token_list[arg_number]):
                payload_bytes += (num_to_int(token_list[arg_number]))
            elif arg == 'DATA2':
                return 'ERROR: expected register or num'

            elif arg == 'AD' and token_list[arg_number] in label_dict:
                payload_bytes += label_dict[token_list[arg_number]]
            elif arg == 'AD':
                return 'ERROR: expected address'

            elif 'flag:' in arg and arg[-1] in token_list[arg_number]:
                flag_bytes += (1 << 4 - command_obj.flag_f.index(arg) - 1)
                

def compile(filename):
    cmd_bytes = bytearray()
    cmd_list, label_dict, data_bytes = to_token_list(filename)
    if "ERROR" in cmd_list:
        print(cmd_list)
        return 
    print(cmd_list)
    print()
    print(label_dict)
    print()
    print_bytes(data_bytes, split=2)


compile("RIOlang/test.rio")