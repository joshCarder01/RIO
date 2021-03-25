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
    'prt' :Command(cmd_str = 'prt',  cmd_b = 0x01, flg_f = ['0','flag:i','flag:c','RF1'], arg_f = ['f','f','DATA']),
    
    # Logic
    'and' :Command(cmd_str = 'and',  cmd_b = 0x10, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'not' :Command(cmd_str = 'not',  cmd_b = 0x11, flg_f = ['0','DR','RF1','0'],   arg_f = ['DR','DATA']),
    'or'  :Command(cmd_str = 'or',   cmd_b = 0x12, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'bsl' :Command(cmd_str = 'bsl',  cmd_b = 0x13, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'bsr' :Command(cmd_str = 'bsr',  cmd_b = 0x14, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'xor' :Command(cmd_str = 'xor',  cmd_b = 0x15, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),

    # Math
    'add' :Command(cmd_str = 'add',  cmd_b = 0x20, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'sub' :Command(cmd_str = 'sub',  cmd_b = 0x21, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'mul' :Command(cmd_str = 'mul',  cmd_b = 0x22, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'div' :Command(cmd_str = 'div',  cmd_b = 0x23, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),
    'mod' :Command(cmd_str = 'mod',  cmd_b = 0x24, flg_f = ['0','DR','RF1','RF2'], arg_f = ['DR','DATA','DATA']),

    # Branch
    'br'  :Command(cmd_str = 'br',   cmd_b = 0x30, flg_f = ['0','flag:p','flag:n','flag:z'], arg_f = ['f','f','f','AD']),
    'jmp' :Command(cmd_str = 'jmp',  cmd_b = 0x31, flg_f = ['0','0','0','SR'], arg_f = ['f','f','f','AD']),
    

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


def to_token_list(filename):
    return_list = []
    data_list = []

    found_end = False
    end_index = 0

    file_handle = open(filename, 'r')
    for line in file_handle:

        # get items
        return_list += [line.replace(',', ' ').lower().strip().split(";")[0].split()]
        # disregard if empty line
        if not return_list[-1]:
            return_list.pop()
        # find the end
        if 'end' in return_list[-1]:
            found_end = True
            end_index = len(return_list)
        # gather all hardcoded value saving
        if 'fill' in return_list[-1] or 'blkw' in return_list[-1] or 'strz' in return_list[-1]:
            data_list += [return_list.pop()]

    if not found_end:
        return "ERROR:no end found"

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

        print(line_number, line)



    return (return_list, data_list, end_index)


print(to_token_list("test.rio"))