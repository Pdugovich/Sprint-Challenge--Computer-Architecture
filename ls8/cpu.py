"""CPU functionality."""

import sys

class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""Construct a new CPU."""
		# Looking further down the file, I can see what they expect to be here
		# We need a register which they expect to be self.reg, which holds 8
		self.reg = [0] * 8
		# We need memory, which looks like they expect to be self.ram
		self.ram = [0] * 256
		# Probably a program counter also
		self.pc = 0
		# Identifying reg[7] as the pointer for the stack
		# the stack starts at 243
		self.reg[7] = 243
		# Setting a flag last 3 digits are less, greater, or equal
		self.fl = 0b00000000
		# Setting running up here so I can mess with it in methods
		self.running = False
		self.operations = {
			# # ALU ops
			0b10100000: self.ADD,
			0b10100001: self.SUB,
			0b10100010: self.MUL,
			0b10100011: self.DIV,
			0b10100100: self.MOD,

			0b01100101: self.INC, 
			0b01100110: self.DEC,

			0b10100111: self.CMP,

			0b10101000: self.AND,
			0b01101001: self.NOT,
			0b10101010: self.OR,
			0b10101011: self.XOR,
			# 0b10101100: self.SHL,
			# 0b10101101: self.SHR,

			# # PC mutators
			0b01010000: self.CALL,
			0b00010001: self.RET,

			# 0b01010010: self.INT,
			# 0b00010011: self.IRET,

			0b01010100: self.JMP,
			0b01010101: self.JEQ,
			0b01010110: self.JNE,
			# 0b01010111: self.JGT,
			# 0b01011000: self.JLT,
			# 0b01011001: self.JLE,
			# 0b01011010: self.JGE,

			# # Other
			# 0b00000000: self.NOP,

			0b00000001: self.HLT,

			0b10000010: self.LDI,

			# 0b10000011: self.LD,
			# 0b10000100: self.ST,

			0b01000101: self.PUSH,
			0b01000110: self.POP,

			0b01000111: self.PRN,
			#0b01001000: self.PRA
		}
	
	# adds two registers together, then saves to a
	def ADD(self, operand_a, operand_b):
		self.reg[operand_a] += self.reg[operand_b]
	
	# Subtracts reg b from a, then saves to a
	def SUB(self, operand_a, operand_b):
		self.reg[operand_a] -= self.reg[operand_b]
	
	# Multiply two registers together and set register a to the result
	def MUL(self, operand_a, operand_b):
		self.reg[operand_a] *= self.reg[operand_b]
	
	# Divide a by b, storing in A
	# if b is 0, print error and halt
	def DIV(self, operand_a, operand_b):
		if self.reg[operand_b] != 0:
			self.reg[operand_a] = self.reg[operand_a] / self.reg[operand_b]
		elif self.reg[operand_b] == 0:
			print("ERROR: Cannot divide by 0.")
			self.HLT(operand_a, operand_b)


	# Divide op_a by op_b, then store remainder in reg_a
	# if value in reg_b is 0, print error and halt
	def MOD(self, operand_a, operand_b):
		if self.reg[operand_b] != 0:
			self.reg[operand_a] = self.reg[operand_a] % self.reg[operand_b]
		elif self.reg[operand_b] == 0:
			print("ERROR: Cannot divide by 0.")
			self.HLT(operand_a, operand_b)
	
	# Increment a register by 1
	def INC(self, operand_a, operand_b):
		self.reg[operand_a] += 1

	# Decrement a register by 1
	def DEC(self, operand_a, operand_b):
		self.reg[operand_a] -= 1

	def CALL(self, operand_a, operand_b):
		# the address of instruction to stack
		self.reg[7] -= 1
		self.ram[self.reg[7]] = self.pc + 2

		# set the PC to the value in the given register
		self.pc = self.reg[operand_a]

	def RET(self, operand_a, operand_b):
		self.pc = self.ram[self.reg[7]]
		self.reg[7] +=1 


	# Jump to the address stored in the given register
	def JMP(self, operand_a, operand_b):
		self.pc = self.reg[operand_a]

	# if equal is set to true, jump to the address stored in the register
	def JEQ(self, operand_a, operand_b):
		if self.fl == 0b00000001:
			self.pc = self.reg[operand_a]
		else:
			self.pc += 2

	# if equal is set to FALSE, jump to register address
	def JNE(self, operand_a, operand_b):
		if self.fl != 0b00000001:
			self.pc = self.reg[operand_a]
		else:
			self.pc += 2

	#
	def CMP(self, operand_a, operand_b):
		"""
		Compare the values in two registers.

		If they are equal, set the Equal E flag to 1, otherwise set it to 0.

		If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

		If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
		"""
		if self.reg[operand_a] == self.reg[operand_b]:
			self.fl = 0b00000001
		elif self.reg[operand_a] < self.reg[operand_b]:
			self.fl = 0b00000100
		elif self.reg[operand_a] > self.reg[operand_b]:
			self.fl = 0b00000010

	def AND(self, operand_a, operand_b):
		self.reg[operand_a] = (self.reg[operand_a] & self.reg[operand_b])
	
	def NOT(self, operand_a, operand_b):
		self.reg[operand_a] = ~self.reg[operand_a]

	def OR(self, operand_a, operand_b):
		self.reg[operand_a] = (self.reg[operand_a] | self.reg[operand_b])

	def XOR(self, operand_a, operand_b):
		self.reg[operand_a] = (self.reg[operand_a] ^ self.reg[operand_b])

	# Halts the program
	def HLT(self, operand_a, operand_b):
		self.running = False

	# sets a register to a specific value
	def LDI(self, operand_a, operand_b):
		self.reg[operand_a] = operand_b

	# decrement the stack pointer and push onto stack
	def PUSH(self, operand_a, operand_b):
		self.reg[7] -= 1
		self.ram[self.reg[7]] = self.reg[operand_a]

	# Pop from the stack and increment the stack pointer
	def POP(self, operand_a, operand_b):
		self.reg[operand_a] = self.ram[self.reg[7]]
		if self.reg[7] <= 242:
			self.reg[7] +=1
		else:
			self.reg[7] = 243
	
	# Print a value at a register
	def PRN(self, operand_a, operand_b):
		print(self.reg[operand_a])

	

	def ram_read(self, address):
		return self.ram[address]

	def ram_write(self, to_write, address):
		self.ram[address] = to_write

	def load(self):
		"""Load a program into memory."""
		program_filename = sys.argv[1]
		
		# Making sure the file is the right type
		if program_filename[-4:] == '.ls8':
			# Just a counter to keep track of where we're writing the program
			write_at_address = 0
			with open(program_filename) as f:
				for line in f:
					line = line.split('#')
					line = line[0].strip()

					if line == '':
						continue
					# Converting to a binary. Nums are the same under the hood
					self.ram[write_at_address] = int(line,2)

					write_at_address += 1
		else:
			raise Exception("Unsupported file type. File name must end with .ls8")


	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		#elif op == "SUB": etc
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pc,
			#self.fl,
			#self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()

	def run(self):
		"""Run the CPU."""
		self.pc = 0
		self.running = True
		while self.running == True:
			# Read the memory stored at current pc
			# Store that value in Instruction Register(IR)
			ir = self.ram_read(self.pc)

			# Using ram_read(), store bytes pc+1 and + 2
			# into variables operand_a and b in case
			# the instructions call for them
			operand_a = self.ram_read(self.pc + 1)
			# print("{0:b}".format(ir))
			operand_b = self.ram_read(self.pc + 2)


			# Then, depending(if) on the opcode, perform
			# the action 

			# Checking to make sure the given code is in our
			# list
			if ir in self.operations.keys():
				"""
				Instruction Layout: AABCDDDD
				AA = Number of operands for this opcode, 0-2
				B = 1 if this is an ALU operation
				C = 1 if this instruction sets the pc
				DDDD = Instruction identifier
				"""
				# Isolating number of operands
				num_operands = (0b11000000 & ir) >> 6
				# Isolating if this is an ALU operation
				is_alu = (0b00100000 & ir) >> 5
				# Isolating if this instruction sets the pc
				sets_pc = (0b00010000 & ir) >> 4

				# Calling that operation's method
				# Do the thing!
				self.operations[ir](operand_a, operand_b)
				
				# Only increment by an automatic amount if 
				# sets_pc == 0
				if sets_pc == 0:
				# Increment program counter by num_operands +1
				# to account for itself
					self.pc += num_operands + 1
