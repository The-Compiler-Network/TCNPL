from exception.CodeNotFoundError import CodeNotFoundError
from model import TokenCategory
from model.Position import TokenPosition
from model.Token import Token
from model.TokenCategory import TokenCategory


class LexicalAnalyzer:

	TAB_SIZE = 4
	separators = {'(': TokenCategory.opParen, ')': TokenCategory.clParen, '{': TokenCategory.opBraces,
				  '}': TokenCategory.clBraces, '[': TokenCategory.opBrackets, ']':TokenCategory.clBrackets,
				  '!': TokenCategory.unary, '~': TokenCategory.unary, '-': TokenCategory.minus, "**": TokenCategory.exp,
				  "*/": TokenCategory.exp, '*': TokenCategory.mult, '/': TokenCategory.mult, '%': TokenCategory.mult,
				  '+': TokenCategory.plus, "<<": TokenCategory.bitShift, ">>": TokenCategory.bitShift, "<>": TokenCategory.unknown,
				  "><": TokenCategory.unknown,
				  '<': TokenCategory.relational, '>': TokenCategory.relational, "<=": TokenCategory.relational,
				  ">=": TokenCategory.relational, "==": TokenCategory.eqOrDiff, "!=": TokenCategory.eqOrDiff,
				  '&': TokenCategory.bitAnd, '|': TokenCategory.bitOr, "&&": TokenCategory.logicAnd,
				  "||": TokenCategory.logicOr, '=': TokenCategory.attrib, ',': TokenCategory.comma, '"': None,
				  ' ': None, '\t': None}
	escape_char = {"\"": '\"', "\\": '\\', "\'": '\'', "n": '\n', "r": '\r', "t": '\t', "b": '\b', "f":
		'\f', "v": '\v', "0": '\0'}
	keyword_token_map = {"bool": TokenCategory.typeBool, "int": TokenCategory.typeInt, "real": TokenCategory.typeReal,
						 "char": TokenCategory.typeChar, "string": TokenCategory.typeString,
						 "array": TokenCategory.typeArray, "as": TokenCategory.asCast, "is": TokenCategory.isType,
						 "while": TokenCategory.whileLoop, "if": TokenCategory.ifSel, "elif": TokenCategory.elifSel,
						 "else": TokenCategory.elseSel, "function": TokenCategory.function,
						 "return": TokenCategory.returnFun, "@isEntryPoint": TokenCategory.entryPoint}
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

	# TODO: ARRUMAR. APENAS POG TEMPORÁRIA
	def next_token(self):
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
		return TokenCategory.classify(string)

	def read_next_line(self):
		line = self.file.readline().strip('\n')
		if line:
			print(line)
			return line
		self.file.close()
		raise EOFError

	def parse_next_line(self):
		line = self.read_next_line()
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
			if c == '\'' or c == '"':  # string and character literals
				string = c
				col += 1
				while col < line_size:
					c = line[col]
					if c == '\\':
						col += 1
						if col < line_size and line[col] in self.escape_char:
							string += self.escape_char[line[col]]
						else:
							string += '\\'
					else:
						string += c
					if c == string[0]:
						break
					col += 1
				category = self.get_category(string)
				if category != TokenCategory.unknown:
					string = string[1:len(string)-1]
				self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), category, string))
				string, new_col = "", col + 1 + (self.TAB_SIZE * tabs)
			elif self.is_separator(c):
				if string:
					self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), self.get_category(string), string))
				if c != ' ' and c != '\t':
					new_col = col + 1 + (self.TAB_SIZE - 1) * tabs
					if c == '*':
						col += 1
						if col < line_size and (line[col] == '/' or line[col] == '*'):
							c += line[col]
						else:
							col -= 1
					if c == '<' or c == '>':
						col += 1
						if col < line_size and (line[col] == '<' or line[col] == '>' or line[col] == '='):
							c += line[col]
						else:
							col -= 1
					if c == '/':
						col += 1
						if col < line_size and line[col] == '/':
							return True
						col -= 1
					self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), self.separators[c], c))
				string, new_col = "", col + 2 + (self.TAB_SIZE - 1) * tabs
			else:
				string += c
			col += 1
		if string:
			self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), self.get_category(string), string))

		return True

	def is_separator(self, c):
		return c in self.separators
