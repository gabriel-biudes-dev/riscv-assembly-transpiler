import os

class FormatR():
    """Format R instruction class
    """
    def __init__(self, format, opcode, funct3, funct7, rs1, rs2, rd, name, str):
        self.format = format
        self.opcode = opcode
        self.funct3 = funct3
        self.funct7 = funct7
        self.rs1 = rs1
        self.rs2 = rs2
        self.rd = rd
        self.name = name
        self.str = str

class FormatI():
    """Format I instruction class
    """
    def __init__(self, format, opcode, funct3, imm, rs1, rd, name, str):
        self.format = format
        self.opcode = opcode
        self.funct3 = funct3
        self.imm = imm
        self.rs1 = rs1
        self.rd = rd
        self.name = name
        self.str = str

class FormatS():
    """Format S instruction class
    """
    def __init__(self, format, opcode, funct3, imm, imm2, rs1, rs2, name, str):
        self.format = format
        self.opcode = opcode
        self.funct3 = funct3
        self.imm = imm
        self.imm2 = imm2
        self.rs1 = rs1
        self.rs2 = rs2
        self.name = name
        self.str = str

class FormatB():
    """Format B instruction class
    """
    def __init__(self, format, opcode, funct3, imm, imm2, rs1, rs2, name, str):
        self.format = format
        self.opcode = opcode
        self.funct3 = funct3
        self.imm = imm
        self.imm2 = imm2
        self.rs1 = rs1
        self.rs2 = rs2
        self.name = name
        self.str = str

def loadFile(filename):
    """Loads text file to memory

    Args:
        filename (str): File name

    Returns:
        list[str]: Array of file content splitted by line
    """
    with open(filename, 'r') as file: content = file.read()
    content = content.split('\n')
    content = [i for i in content if i != '']
    return content

def getopcode(instruction):
    """Gets the operation code from a instruction

    Args:
        instruction (str): Instruction in binary

    Returns:
        str: Opcode
    """
    return instruction[25:32]

def getformat(opcode):
    """Gets the format from a instruction

    Args:
        opcode (str): Instruction opcode

    Returns:
        str: Instruction format
    """
    if opcode == '0110011': return 'R'
    if opcode == '0000011': return 'I'
    if opcode == '0010011': return 'I'
    if opcode == '0100011': return 'S'
    if opcode == '1100011': return 'B'

def getR(str):
    """Gets R instrunction object from a binary instrunction

    Args:
        str (str): Binary instrunction

    Returns:
        FormatR: Instrunction object
    """
    funct7 = str[0:7]
    rs2 = str[7:12]
    rs1 = str[12:17]
    funct3 = str[17:20]
    rd = str[20:25]
    opcode = getopcode(str)
    if funct3 == '000' and funct7 == '0000000': name = 'add'
    if funct3 == '000' and funct7 == '0100000': name = 'sub'
    if funct3 == '111' and funct7 == '0000000': name = 'and'
    if funct3 == '110' and funct7 == '0000000': name = 'or'
    instruction = FormatR('R', opcode, funct3, funct7, rs1, rs2, rd, name, str)
    return instruction

def getI(str):
    """Gets I instrunction object from a binary instrunction

    Args:
        str (str): Binary instrunction

    Returns:
        FormatI: Instrunction object
    """
    imm = str[0:12]
    rs1 = str[12:17]
    funct3 = str[17:20]
    rd = str[20:25]
    opcode = getopcode(str)
    if opcode == '0010011': name = 'addi'
    if opcode == '0000011': name = 'lw'
    instruction = FormatI('I', opcode, funct3, imm, rs1, rd, name, str)
    return instruction

def getS(str):
    """Gets S instrunction object from a binary instrunction

    Args:
        str (str): Binary instrunction

    Returns:
        FormatS: Instrunction object
    """
    imm = str[0:7]
    rs2 = str[7:12]
    rs1 = str[12:17]
    funct3 = str[17:20]
    imm2 = str[20:25]
    opcode = getopcode(str)
    name = 'sw'
    instruction = FormatS('S', opcode, funct3, imm, imm2, rs1, rs2, name, str)
    return instruction

def getB(str):
    """Gets B instrunction object from a binary instrunction

    Args:
        str (str): Binary instrunction

    Returns:
        FormatB: Instrunction object
    """
    imm = str[0:7]
    rs2 = str[7:12]
    rs1 = str[12:17]
    funct3 = str[17:20]
    imm2 = str[20:25]
    opcode = getopcode(str)
    if funct3 == '000': name = 'beq'
    if funct3 == '001': name = 'bne'
    instruction = FormatB('B', opcode, funct3, imm, imm2, rs1, rs2, name, str)
    return instruction

def getinstruction(str, format):
    """Generic function to get instrunctions from all formats

    Args:
        str (str): Binary instrunction
        format (str): Instrunction format

    Returns:
        Instrunction: Instrunction object
    """
    instruction = None
    if format == 'R': instruction = getR(str)
    if format == 'I': instruction = getI(str)
    if format == 'S': instruction = getS(str)
    if format == 'B': instruction = getB(str)
    return instruction

def getinstructions(filecontent):
    """Gets all instrunctions from the text file

    Args:
        filecontent (list[str]): List of instrunctions on the file splitted by line

    Returns:
        list[Instrunctions]: List of instrunction class objects
    """
    instructions = []
    for x in filecontent:
        opcode = getopcode(x)
        format = getformat(opcode)
        instruction = getinstruction(x, format)
        instructions.append(instruction)
    return instructions

def getIntAddi(strbin):
    """Gets integer value of addi instructions IMM

    Args:
        strbin (str): Binary string

    Returns:
        int: Integer Value
    """
    signal = strbin[0]
    finalstr = strbin[1:len(strbin)]
    x = int(finalstr , 2)
    num_bits = 12
    if signal == '0': return x
    return x - (1 << num_bits)

def getIntB(strbin):
    """Gets integer value of B instructions IMM

    Args:
        strbin (str): Binary string

    Returns:
        int: Integer value
    """
    signal = strbin[0]
    finalstr = strbin[11]
    finalstr = finalstr + strbin[1]
    finalstr = finalstr + strbin[2]
    finalstr = finalstr + strbin[3]
    finalstr = finalstr + strbin[4]
    finalstr = finalstr + strbin[5]
    finalstr = finalstr + strbin[6]
    finalstr = finalstr + strbin[7]
    finalstr = finalstr + strbin[8]
    finalstr = finalstr + strbin[9]
    finalstr = finalstr + strbin[10]
    finalstr = finalstr + '0'
    x = int(finalstr , 2)
    num_bits = 12
    if signal == '0': return x
    return x - (1 << num_bits)

def translate(instruction):
    """Translates a instrunction to assembly code

    Args:
        instruction (Instrunction): Instrunction object

    Returns:
        str: Instrunction in assembly code
    """
    if instruction.format == 'R':
        template = instruction.name + ' xA, xB, xC'
        template = template.replace('A', str(int(instruction.rd, 2)))
        template = template.replace('B', str(int(instruction.rs1, 2)))
        template = template.replace('C', str(int(instruction.rs2, 2)))
    if instruction.name == 'addi': 
        template = instruction.name + ' xA, xB, Z'
        template = template.replace('A', str(int(instruction.rd, 2)))
        template = template.replace('B', str(int(instruction.rs1, 2)))
        template = template.replace('Z', str(getIntAddi(instruction.imm)))
    if instruction.name == 'lw' or instruction.name == 'sw':
        template = instruction.name + ' xA, Z(xB)'
        if instruction.name == 'lw': 
            template = template.replace('A', str(int(instruction.rd, 2)))
            template = template.replace('Z', str(int(instruction.imm, 2)))
        else: 
            template = template.replace('A', str(int(instruction.rs2, 2)))
            template = template.replace('Z', str(int(instruction.imm2, 2)))
        template = template.replace('B', str(int(instruction.rs1, 2)))
    if instruction.format == 'B':
        template = instruction.name + ' xZ, xK, M'
        template = template.replace('Z', str(int(instruction.rs1, 2)))
        template = template.replace('K', str(int(instruction.rs2, 2)))
        immf = instruction.imm + instruction.imm2
        immf = getIntB(immf)
        template = template.replace('M', str(immf))
    return template

def getflags(instrunction):
    """Gets CPU flags from a instrunction execution

    Args:
        instrunction (Instrunction): Instrunction object

    Returns:
        list[int]: List of flags
    """
    flags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if instrunction.format == 'R':
        flags[0] = 1
        flags[1] = 1
        flags[7] = 1
    if instrunction.format == 'B':
        flags[2] = 1
        flags[8] = 1
    if instrunction.name == 'lw':
        flags[1] = 1
        flags[3] = 1
        flags[4] = 1
        flags[6] = 1
    if instrunction.name == 'addi':
        flags[1] = 1
        flags[6] = 1
    if instrunction.name == 'sw':
        flags[5] = 1
        flags[6] = 1
    return flags

def showflags(instrunction):
    """Shows CPU flags from an instrunction

    Args:
        instrunction (Instrunction): Instrunction object
    """
    flagnames = ['RegDst', 'RegWrite', 'Branch', 'MemToReg', 'MemRead', 'MemWrite', 'ALUSource', 'ALUOp1', 'ALUOp0']
    flags = getflags(instrunction)
    for index, x in enumerate(flagnames): print(f'{flagnames[index]}: {flags[index]}')

def loadregisters():
    """Loads CPU registers

    Returns:
        list[int]: CPU registers
    """
    registers = []
    for x in range(32): registers.append(0)
    return registers

def loadmemory():
    """Loads memory

    Returns:
        list[int]: Memory
    """
    memory = []
    for x in range(256): memory.append(0)
    return memory

def showmenu():
    """Show the application menu
    """
    print('1)Executar instrução')
    print('2)Mostrar registradores')
    print('3)Mostrar memória')

def showregisters(registers):
    """Shows current registers values

    Args:
        registers (list[int]): List of registers
    """
    print('\n[REGISTRADORES]')
    for index, x in enumerate(registers):
        print(f'x{index} ', end = '')
        if index < 10: print(' ', end = '')
        print('= %3d' % x, end = '')
        if (index + 1) % 4 == 0: print()
        else: print("\t\t", end = '')

def showmemory(memory):
    """Shows current memory values

    Args:
        memory (list[int]): Memory
    """
    print('\n[MEMÓRIA]')
    for index, x in enumerate(memory):
        print(f'[{index}] ', end = '')
        if index < 10: print(' ', end = '')
        if index < 100: print(' ', end = '')
        print('= %3d' % x, end = '')
        if (index + 1) % 4 == 0: print()
        else: print("\t\t", end = '')

def execute(instruction, memory, registers, pc):
    """Executes instruction

    Args:
        instruction (Instruction): Instruction object
        memory (list[int]): Memory
        registers (list[int]): Registers
        pc (int): Current PC value

    Returns:
        list[int]: New values for memory, registers and PC
    """
    if instruction.name == 'addi':
        rd = int(instruction.rd, 2)
        rs1 = int(instruction.rs1, 2)
        imm = getIntAddi(instruction.imm)
        registers[rd] = registers[rs1] + imm
    if instruction.format == 'R':
        rd = int(instruction.rd, 2)
        rs1 = int(instruction.rs1, 2)
        rs2 = int(instruction.rs2, 2)
        if instruction.name == 'add': registers[rd] = registers[rs1] + registers[rs2]
        if instruction.name == 'sub': registers[rd] = registers[rs1] - registers[rs2]
        if instruction.name == 'and': registers[rd] = registers[rs1] & registers[rs2]
        if instruction.name == 'or': registers[rd] = registers[rs1] | registers[rs2]
    if instruction.name == 'lw':
        rd = int(instruction.rd, 2)
        rs1 = int(instruction.rs1, 2)
        imm = int(instruction.imm, 2)
        registers[rd] = memory[registers[rs1] + int(imm / 4)]
    if instruction.name == 'sw':
        rs1 = int(instruction.rs1, 2)
        rs2 = int(instruction.rs2, 2)
        imm = int(instruction.imm2, 2)
        memory[registers[rs1] + int(imm / 4)] = registers[rs2]
    if instruction.format == 'B':
        rs1 = int(instruction.rs1, 2)
        rs2 = int(instruction.rs2, 2)
        imm = instruction.imm
        imm2 = instruction.imm2
        immfinal = imm + imm2
        immfinal = getIntB(immfinal)
        if instruction.name == 'beq':
            if registers[rs1] == registers[rs2]: pc = pc + immfinal - 4
        if instruction.name == 'bne':
            if registers[rs1] != registers[rs2]: pc = pc + immfinal - 4
    return memory, registers, pc

def main():
    """Main function
    """
    filename = str(input('Insira o nome do arquivo a ser carregado: '))
    filecontent = loadFile(filename)
    instructions = getinstructions(filecontent)
    registers = loadregisters()
    memory = loadmemory()
    pc = 0
    maxpc = len(instructions) * 4
    while pc < maxpc:
        print('\nLista de instruções a serem executadas:\n')
        for index, x in enumerate(instructions):
            if index >= (pc / 4): print('\t' + translate(x))
        print(f'\nPC = {pc}\n')
        showmenu()
        answer = int(input('Escolha a opção: '))
        if answer == 1:
            if os.name == 'nt': os.system('cls')
            else: os.system('clear')
            print(f'\nInstrução executada: {translate(instructions[int(pc / 4)])}\n')
            print('Flags da instrução:\n')
            showflags(instructions[int(pc / 4)])
            memory, registers, pc = execute(instructions[int(pc / 4)], memory, registers, pc)
            pc = pc + 4
        if answer == 2: showregisters(registers)
        if answer == 3: showmemory(memory)
    showmemory(memory)
    showregisters(registers)
    print('\nNão há mais instruções a serem executadas')
    end = input()

if __name__ == '__main__': main()