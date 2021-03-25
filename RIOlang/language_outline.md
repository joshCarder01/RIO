Outline

    RIO is a effectivly a 32 bit word language, meaning it will look at 32 bits at a time to run an instruction.
    However, addresses are marked every 16 bits, registers store 16 bits, and most numbers deal in 8 bits


How most instructions are going to work out
    
    line 1  |0 1 2 3 4 5 6 7|8 9 A B C D E F|
            |    op code    |f|s|s|d| DR/SR |

    line 2  |0 1 2 3 4 5 6 7|8 9 A B C D E F|
            |  num or reg   |  num or reg   |
                            OR
            |     address label offset      |

    'op code' - operation to be performed

    'f' - an optional flag for the operation

    's' - flags that represent if 'num or reg' of the code will be used as an 8 bit number or 4 bit register

    'd' - flag that represents if operation will return something to the destination register

    'DR/SR' - destination or source register

    'num or reg' - represents either a number or register

    'address label offset' - offset from line previous (the line with the op code) to the destination 


Registers
    
    hold 16 bit values
    
    There can be up to 16 total registers, however may not use that many?

    'r0' - commonly used in trap commands

    'r1' - commonly used in trap commands

    'r6' - stack pointer

    'r7' - return address


Instruction set

                                |0 1 2 3 4 5 6 7|8 9 A B C D E F| |0 1 2 3 4 5 6 7|8 9 A B C D E F|

    DEBUG
    0x00|PRT |print             |0 0 0 0 0 0 0 0|0 s f f 0 0 0 0| |  num or reg   |0 0 0 0 0 0 0 0|

    LOGIC
    0x10|AND |and               |0 0 0 1 0 0 0 0|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x11|NOT |not               |0 0 0 1 0 0 0 1|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x12|OR  |or                |0 0 0 1 0 0 1 0|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x13|BSL |bit shift left    |0 0 0 1 0 0 1 1|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x14|BSR |bit shift right   |0 0 0 1 0 1 0 0|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x15|XOR |xor               |0 0 0 1 0 1 0 1|0 s s d|  DR   | |  num or reg   |  num or reg   |

    MATH
    0x20|ADD |add               |0 0 1 0 0 0 0 0|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x21|SUB |subtract          |0 0 1 0 0 0 0 1|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x22|MUL |multiply          |0 0 1 0 0 0 1 0|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x23|DIV |divide            |0 0 1 0 0 0 1 1|0 s s d|  DR   | |  num or reg   |  num or reg   |
    0x24|MOD |modulus           |0 0 1 0 0 1 0 0|0 s s d|  DR   | |  num or reg   |  num or reg   |

    BRANCH
    0x30|BR  |branch            |0 0 1 1 0 0 0 0|0 p n z 0 0 0 0| |     address label offset      |
    0x31|JMP |jump              |0 0 1 1 0 0 0 1|0 0 0 1|  SR   | |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x31|RET |return            |0 0 1 1 0 0 0 1|0 0 0 1|1 1 1 1| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x32|JSR |jump to subroutine|0 0 1 1 0 0 1 0|1 0 0 0|0 0 0 0| |     address label offset      |
    0x32|JSRR|JSR at register   |0 0 1 1 0 0 1 0|0 0 0 1|  SR   | |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x33|END |end prgram        |0 0 1 1 0 0 1 1|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x34|ORIG|program start     |0 0 1 1 0 1 0 0|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x35|HALT|halt CPU          |0 0 1 1 0 1 0 1|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|

    LOAD / STORE
    0x40|LD  |DR=mem[adrs]      |0 1 0 0 0 0 0 0|0 0 0 1|  DR   | |     address label offset      |
    0x41|LDI |DR=mem[mem[adrs]] |0 1 0 0 0 0 0 1|0 0 0 1|  DR   | |     address label offset      |
    0x42|LDR |DR=mem[SR+val]    |0 1 0 0 0 0 1 0|0 0 0 1|  DR   | |  num or reg   |  num or reg   |
    0x43|LEA |DR=adrs           |0 1 0 0 0 0 1 1|0 0 0 1|  DR   | |     address label offset      |
    0x44|ST  |mem[adrs]=SR      |0 1 0 0 0 1 0 0|0 0 0 1|  SR   | |     address label offset      |
    0x45|STI |mem[mem[adrs]]=SR |0 1 0 0 0 1 0 1|0 0 0 1|  SR   | |     address label offset      |
    0x46|STR |mem[SR+val]=SR    |0 1 0 0 0 1 1 0|0 0 0 1|  SR   | |  num or reg   |  num or reg   |
    0x47|FILL|fill 16 bits      |0 1 0 0 0 1 1 1|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x47|BLKW|reserve N bits    |0 1 0 0 0 1 1 1|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
    0x47|STRZ|bits for str      |0 1 0 0 0 1 1 1|0 0 0 0|0 0 0 0| |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|

    IO
    0x50|SBR |serial buf read   |0 1 0 1 0 0 0 0|0 0 0 0|  DR   | |  num or reg   |0 0 0 0 0 0 0 0|
    0x51|SBW |serial buf write  |0 1 0 1 0 0 0 1|0 0 0 0|  SR   | |  num or reg   |0 0 0 0 0 0 0 0|

Compiler Order

    - turn file into token list
        - shift labels to the front of the next operation line
        - ex
            "label2 add R1 #1 R1 ;comment"
            "label3 add R2 #2 R2 ;comment2"
            Turns into
            [
                ["label2", "add", "R1", "#1", "R1"],
                ["label3", "add", "R2", "#2", "R2"]
            ]
