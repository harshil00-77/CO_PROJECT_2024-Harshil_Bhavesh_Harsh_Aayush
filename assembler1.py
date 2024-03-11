import sys
from math import floor
import re

INSTRUCTIONS = {
    "add": "0110011",
    "sub": "0110011",
    "sll": "0110011",
    "slt": "0110011",
    "sltu": "0110011",
    "sltiu": "0010011",
    "xor": "0110011",
    "srl": "0110011",
    "or": "0110011",
    "and": "0110011",
    "lw": "0000011",
    "addi": "0010011",
    "jalr": "1100111",
    "sw": "0100011",
    "beq": "1100011",
    "bne": "1100011",
    "bge": "1100011",
    "bgeu": "1100011",
    "blt": "1100011",
    "bltu": "1100011",
    "auipc": "0010111",
    "lui": "0110111",
    "jal": "1101111"
}

REGISTERS = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000", #fp
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
} 

# Read input from stdin
v = sys.stdin.read().split("\n")
v.pop(-1)

# Replace commas, parentheses, and spaces with blank spaces
v = [line.replace(",", " ").replace("(", " ").replace(")", " ") for line in v]

# Split each line by whitespace and append to list 'l'
l = []
for i in v:
    m = i.split()
    l.append(m)

print(l)

# def dectobin(decimal_num, i):
#     if isinstance(decimal_num, str):
#         decimal_num = int(decimal_num)
#     if decimal_num < 0:
#         decimal_num = 0xFFFFFFFF + decimal_num + 1
#     binary_str = bin(decimal_num)[2:]
#     if len(binary_str) > i:
#         print("Error: Immediate value exceeds allowed length for instruction.")
#         sys.exit(1)
#     padded_binary_str = binary_str.zfill(i)
#     return str(padded_binary_str)

def dectobin(decimal, num_bits):
    # Calculate the number of bits needed to represent the absolute value
    abs_decimal = abs(decimal)
    if decimal >= 0:
        min_bits = len(bin(abs_decimal)[2:])
    else:
        min_bits = len(bin(abs_decimal)[3:]) + 1  # Account for the sign bit

    # If the number of bits is not enough, return None
    if num_bits < min_bits:
        return None

    # Convert the absolute value to binary
    binary = bin(abs_decimal)[2:]

    # Pad with zeros if necessary
    binary = '0' * (num_bits - len(binary)) + binary

    # If the number is negative, take the 2's complement
    if decimal < 0:
        # Invert the bits
        binary = ''.join(['1' if bit == '0' else '0' for bit in binary])
        # Add one to get the 2's complement
        binary = bin(int(binary, 2) + 1)[2:]

    return binary
 
def rtype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)
    if len(lst) != 4 or lst[1] not in REGISTERS or lst[2] not in REGISTERS or lst[3] not in REGISTERS:
        print(f"Error: Invalid syntax for R-type instruction.")
        sys.exit(1)

    lmain=[]
    if lst[0]=='add':
        lmain.append("0000000") #append func7
        lmain.append(REGISTERS[lst[3]])
        lmain.append(REGISTERS[lst[2]])
        lmain.append("000") #append func3
        lmain.append(REGISTERS[lst[1]])
        lmain.append(INSTRUCTIONS[lst[0]])
    
    elif lst[0] == 'sub':
        lmain.append("0100000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("000") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'sll':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("001") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'slt':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("010") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'sltu':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("011") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'xor':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("100") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'srl':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("101") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'or':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("110") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    elif lst[0] == 'and':
        lmain.append("0000000") # append func7
        lmain.append(REGISTERS[lst[3]]) # rs2
        lmain.append(REGISTERS[lst[2]]) # rs1
        lmain.append("111") # append func3
        lmain.append(REGISTERS[lst[1]]) # rd
        lmain.append(INSTRUCTIONS[lst[0]]) # opcode
    
    x = ""
    for i in lmain:
        x = x + i
    return x

def itype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)

    if lst[0] == "lw":
        if len(lst) != 4 or lst[1] not in REGISTERS or lst[3] not in REGISTERS:
            print(f"Error: Invalid syntax for 'lw' instruction.")
            sys.exit(1)

    if lst[0] in ["addi", "sltiu", "jalr"]:
        if len(lst) != 4 or lst[1] not in REGISTERS or lst[2] not in REGISTERS:
            print(f"Error: Invalid syntax for '{lst[0]}' instruction.")
            sys.exit(1)
    lmain = []
    if lst[0] == "lw":
        a = dectobin(int(lst[2]),12)
        lmain.append(a)
        b=REGISTERS[lst[3]]
        lmain.append(b)
        lmain.append("010")
        c = REGISTERS[lst[1]]
        lmain.append(c)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0] == "addi":
        a = dectobin(int(lst[3]),12)
        lmain.append(a)
        b=REGISTERS[lst[2]]
        lmain.append(b)
        lmain.append("000")
        c = REGISTERS[lst[1]]
        lmain.append(c)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0] == "sltiu":
        a = dectobin(int(lst[3]),12)
        lmain.append(a)
        b=REGISTERS[lst[2]]
        lmain.append(b)
        lmain.append("011")
        c = REGISTERS[lst[1]]
        lmain.append(c)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0] == "jalr":
        a = dectobin(int(lst[3]),12)
        lmain.append(a)
        b=REGISTERS[lst[2]]
        lmain.append(b)
        lmain.append("000")
        c = REGISTERS[lst[1]]
        lmain.append(c)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)
        
    x = ""
    for i in lmain:
        x = x + i
    return x

def stype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)
    if len(lst) != 4 or lst[1] not in REGISTERS or lst[3] not in REGISTERS:
        print(f"Error: Invalid syntax for S-type instruction.")
        sys.exit(1)
    lmain=[]
    if lst[0]=='sw':
        a = dectobin(int(lst[2]),12)
        lmain.append(a[12-11-1:12-5])
        b = REGISTERS[lst[1]]
        lmain.append(b)
        c = REGISTERS[lst[3]]
        lmain.append(c)
        lmain.append('010')
        lmain.append(a[12-4-1:12-0])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    x = ""
    for i in lmain:
        x = x + i
    return x

def utype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)
    if len(lst) != 3 or lst[1] not in REGISTERS:
        print(f"Error: Invalid syntax for U-type instruction.")
        sys.exit(1)

    lmain=[]
    if lst[0]=='lui':
        a = dectobin(int(lst[2]),32)
        lmain.append(a[32-31-1:32-12])
        b = REGISTERS[lst[1]]
        lmain.append(b)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='auipc':
        a = dectobin(int(lst[2]),32)
        lmain.append(a[32-31-1:32-12])
        b = REGISTERS[lst[1]]
        lmain.append(b)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    x = ""
    for i in lmain:
        x = x + i
    return x
    

def jtype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)
    if len(lst) != 3 or lst[1] not in REGISTERS:
        print(f"Error: Invalid syntax for J-type instruction.")
        sys.exit(1)
    lmain=[]
    if lst[0]=='jal':
        a = dectobin(int(lst[2]),21)
        # lmain.append(a[21-20-1])
        # lmain.append(a[21-10-1:21-1])
        # lmain.append(a[21-11-1])
        # lmain.append(a[21-19-1:21-12])
        jump_address = a.zfill(21)  # Zero-fill the binary string to ensure it's 21 bits

        lmain.append(jump_address[0])  # Extracting the first bit
        lmain.append(jump_address[10:20])  # Extracting bits 10-19
        lmain.append(jump_address[9])  # Extracting bit 9
        lmain.append(jump_address[1:9])
        b = REGISTERS[lst[1]]
        lmain.append(b)
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    x = ""
    for i in lmain:
        x = x + i
    return x

def btype(lst):
    if lst[0] not in INSTRUCTIONS:
        print(f"Error: Unknown instruction '{lst[0]}'.")
        sys.exit(1)
    if len(lst) != 4 or lst[1] not in REGISTERS or lst[2] not in REGISTERS:
        print(f"Error: Invalid syntax for B-type instruction.")
        sys.exit(1)

    lmain=[]
    if lst[0]=='beq':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("000")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='bne':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("001")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='blt':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("100")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='bge':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("101")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='bltu':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("110")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    if lst[0]=='bgeu':
        a = dectobin(int(lst[3]),13)
        lmain.append(a[13-12-1])
        lmain.append(a[13-10-1:13-5])
        b = REGISTERS[lst[2]]
        lmain.append(b)
        c = REGISTERS[lst[1]]
        lmain.append(c)
        lmain.append("111")
        lmain.append(a[13-4-1:13-1])
        lmain.append(a[13-11-1])
        d = INSTRUCTIONS[lst[0]]
        lmain.append(d)

    x = ""
    for i in lmain:
        x = x + i
    return x
    
R_Type = ["add","sub","slt","sltu","xor","sll","srl","or" ,"and"]
I_Type = ["lw","addi","sltiu","jalr"]
S_Type  = ["sw"]
B_Type = ["beq","bne","blt","bge", "bltu","bgeu"]
U_Type  = ["lui","auipc"]
J_Type = ["jal"]
Bonus = ["mul","rst","halt","rvrs"]
           
instructions = R_Type + I_Type + S_Type + B_Type + U_Type + J_Type
for x in l:
    if x[0] in instructions:
        if x[0] in R_Type:
            print(rtype(x))
        elif x[0] in I_Type:
            print(itype(x))
        elif x[0] in S_Type:
            print(stype(x))
        elif x[0] in B_Type:
            print(btype(x))
        elif x[0] in U_Type:
            print(utype(x))
        elif x[0] in J_Type:
            print(jtype(x))
    else:
        print(f"Error: Unknown instruction '{x[0]}'.")
        sys.exit(1)