class Token:
	position = None
	value = None
	category = None

	def __init__(self, position, category, value):
		self.position = position
		self.category = category
		self.value = value

	def pretty_print(self):
		print("[%04d, %04d] () {%s}" % (self.position.line, self.position.column, self.value))

	def get_line(self):
		return self.position.line

	def __str__(self):
		return "[%04d, %04d] (%s) {%s}" % (self.position.line, self.position.column, self.category, self.value)