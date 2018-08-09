from exception.CodeNotFoundError import CodeNotFoundError
from model import TokenCategory
from model.Position import TokenPosition
from model.Token import Token
from model.TokenCategory import TokenCategory


class LexicalAnalyzer:

	TAB_SIZE = 4
	SEPARATORS = {'{': TokenCategory.opBraces, '}': TokenCategory.clBraces, '(': TokenCategory.opParen, ')':
				  TokenCategory.clParen, ',': TokenCategory.comma, '"': None, ' ': None, '\t': None}
	ESCAPE_CHAR = {"\\\"": '\"', "\\\\": '\\', "\\\'": '\'', "\\n": '\n', "\\r": '\r', "\\t": '\t', "\\b": '\b', "\\f":
                   '\f', "\\v": '\v', "\\0": '\0'}
	keyword_token_map = {"bool": TokenCategory.typeBool, "int": TokenCategory.typeInt, "real": TokenCategory.typeReal,
						 "char": TokenCategory.typeChar, "string": TokenCategory.typeString,
						 "array": TokenCategory.typeArray, "as": TokenCategory.asCast, "is": TokenCategory.isType,
						 "while": TokenCategory.whileLoop, "if": TokenCategory.ifSel, "elif": TokenCategory.elifSel,
						 "else": TokenCategory.elseSel, "function": TokenCategory.function,
						 "return": TokenCategory.returnFun, "@isEntryPoint": TokenCategory.entryPoint,
						 "-": TokenCategory.unary, "**": TokenCategory.exp, "*": TokenCategory.mult,
						 "+": TokenCategory.additive, "<<": TokenCategory.bitShift,
						 ">>": TokenCategory.bitShift, "<": TokenCategory.relational, ">": TokenCategory.relational,
						 "<=": TokenCategory.relational, ">=": TokenCategory.relational, "==": TokenCategory.eqOrDiff,
						 "!=": TokenCategory.eqOrDiff, "&": TokenCategory.bitAnd, "|": TokenCategory.bitOr,
						 "&&": TokenCategory.logicAnd, "||": TokenCategory.logicOr, "=": TokenCategory.attrib}
	file = None
	token_buffer = []
	code_lines = []
	lines_qt = 0
	current_line = 0

	def __init__(self, filepath):
		try:
			self.file = open(filepath, 'r', encoding='utf-8')
		except IOError:
			raise CodeNotFoundError("The specified file from " + filepath +
									" could not be found. Please check the path.")
		self.code_lines = self.file.readlines()
		self.file.close()
		self.lines_qt = len(self.code_lines)

	# TODO: ARRUMAR. APENAS POG TEMPORÁRIA
	def next_token(self):
		# print("token_buffer:", self.token_buffer, len(self.token_buffer))
		if not self.token_buffer:
			while True:
				try:
					if self.parse_next_line():
						break
				except EOFError:
					return None
		return self.token_buffer.pop(0)

	def get_category(self, string):
		if string in self.keyword_token_map:
			return self.keyword_token_map[string]
		# try:
		# 	return TokenCategory[string]
		# except KeyError:
		return TokenCategory.classify(string)

	def parse_next_line(self):
		if self.current_line >= self.lines_qt:
			raise EOFError

		line = self.code_lines[self.current_line].strip('\n')
		self.current_line += 1
		new_col, string, col, line_size, tabs = 1, "", 0, len(line), 0
		while col < line_size and (line[col] == ' ' or line[col] == '\t'):
			new_col += 1 if line[col] == ' ' else self.TAB_SIZE
			tabs += 1 if line[col] == '\t' else 0
			col += 1
		if col == line_size:  # empty line
			return False

		while col < line_size:
			c = line[col]
			if c == '\'': # character literal
				string = ""
				col += 1
				if line[col] == '\\':
					col += 1
					if col < line_size:
						string += self.ESCAPE_CHAR["\\" + line[col]]
				else:
					string += line[col]
				col += 1
				if col < line_size and line[col] != '\'':
					while col < line_size and line[col] != '\'':
						string += line[col]
						col += 1
					self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), TokenCategory.unknown, string))
				else:
					self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), TokenCategory.char, string))
				string = ""
				new_col = col + 1 + (self.TAB_SIZE * tabs)
			elif c == '"':  # string literal
				col += 1
				while col < line_size:
					c = line[col]
					if c == '"':
						break
					if c != '\\':
						string += c
					else:
						col += 1
						if col < line_size:
							c = line[col]
						c = self.ESCAPE_CHAR["\\" + c]
						string += c
					col += 1
				self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), TokenCategory.string, string))
				string = ""
				new_col = col + 1 + (self.TAB_SIZE * tabs)
			elif self.is_separator(c):
				if string:
					self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), self.get_category(string), string))
				if c != ' ' and c != '\t':
					ccol = col
					if new_col:
						ccol += 1 + (self.TAB_SIZE * tabs)
					self.token_buffer.append(Token(TokenPosition(self.current_line, ccol), self.SEPARATORS[c], c))
				new_col = col + 2 + (self.TAB_SIZE * tabs)
				string = ""
			else:  # id OR LEXICAL ERROR
				string += c
			col += 1
		if string:
			self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), self.get_category(string), string))

		return True

	def is_separator(self, c):
		return c in self.SEPARATORS
