'''
Credits: Samarth Singla
'''

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("filename")
args = parser.parse_args()

opnameToCode = {'add':'00000', 'sub':'00001', 'cmp':'00101'}

get_bin = lambda x, n: format(x, 'b').zfill(n)

def getModandOperation(op):
    if(op[-1] == 'u'):
        return 1, op[:-1]
    elif op[-1] == 'h':
        return 2, op[:-1]
    else:
        return 0, op

def parse_instr(arg):

    mod, opname = getModandOperation(arg[0])
    opcode = opnameToCode[opname]

    nrd = int(arg[1][1:])
    rd = get_bin(nrd, 4)

    nrs1 = int(arg[2][1:])
    rs1 = get_bin(nrs1, 4)

    isImm = arg[3][0] != 'r'

    finStr = None
    if isImm:
        imm = int(arg[3])
        finStr = f"{opcode}{get_bin(isImm,1)}{rd}{rs1}{get_bin(mod, 2)}{get_bin(imm, 16)}"
    else:
        nrs2 = int(arg[3][1:])
        rs2 = get_bin(nrs2, 4)
        finStr = f"{opcode}{get_bin(isImm,1)}{rd}{rs1}{rs2}{get_bin(0,14)}"
    return finStr

def get_littleendian(hexInstr):
    L = [hexInstr[i:i+2] for i in range(0, len(hexInstr), 2)]
    L.reverse()
    return " ".join(L)

default_instr = "00 00 00 00"

def construct_imem(hexList, fname):
    batchInstr = list(map(get_littleendian, hexList))
    for _ in range((4-len(batchInstr)%4)%4):
        batchInstr.append(default_instr)
    lines = [" ".join(batchInstr[i:i+4]) for i in range(0,len(batchInstr),4)]
    with open(f"{fname}.imem", 'w+') as opfile:
        opfile.write("v3.0 hex words addressed\n")
        for i in range(len(lines)):
            opfile.write(f"{str(hex(16*i))[2:]}: {lines[i]}\n")
    
    # print(batchInstr)

hexListInstr = []
with open(f"{args.filename}.risc") as prog:
    instr = prog.readline()
    while instr:
        binInstr = parse_instr(instr.split())
        # print("binInstr",binInstr)
        hexInstr = hex(int(binInstr,2))

        hexListInstr.append(str(hexInstr)[2:].zfill(8))
        instr = prog.readline()

construct_imem(hexListInstr, args.filename)