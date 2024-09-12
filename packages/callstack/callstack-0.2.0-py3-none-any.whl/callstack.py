import sys
import os

class Frame:
	"""
	Represents a frame in the call stack, encapsulating details about the execution context.

    Attributes:
        path (str): The file path of the code in this frame.
        package (str): The package name of the module, if any.
        module (str): The name of the module.
        line (int): The line number in the source code.
        cls (str): The name of the class the code belongs to, if any.
        clsRef (type): Direct reference to the class object, if resolvable.
        function (str): The name of the function or method.
        fqn (str): Fully Qualified Name of the class.
        protected (bool): Indicates if the access level is protected (same class or subclass).
        internal (bool): Indicates if the call is internal to the package.
        location (str): Formatted string representing the code location.
    """

	def __init__(self, frame):
		self.path = frame.f_code.co_filename
		self.package = frame.f_globals['__package__']
		self.module = frame.f_globals['__name__']
		self.line = frame.f_lineno
		self.cls = getClassName(frame.f_code.co_filename, frame.f_lineno)
		self.clsRef = frame.f_globals.get(self.cls, None)
		self.function = frame.f_code.co_name
		self.fqn = f"{self.package}{'.' if self.package else ''}{os.path.splitext(os.path.basename(self.path))[0]}{'.' + self.cls if self.cls else ''}"

		# Indeterminable without stack context.  Only set from getContext()
		self.protected = False
		self.internal = False

		locArr = [f"{self.module}:{self.line}"]

		if self.cls:
			locArr.append(f" > {self.cls}")

		if self.function and self.function != "<module>":
			if not self.cls:
				locArr.append(" > ")
			locArr.append(f".{self.function}()" if self.cls else f"{self.function}()")

		self.location = "".join(locArr)


_classMapping = {}

def get():
	""" Returns the callstack as a list of Frames """
	stack = []
	frame = sys._getframe(1)
	while frame:
		stack.append(Frame(frame))
		frame = frame.f_back
	return stack


def getOrigin():
	""" Returns a Frame object representing the origin of the call, one level up the stack from where getOrigin() is called. """
	return Frame(sys._getframe(2))


def getContext():
	"""
	Analyzes the call stack to determine the context of the calling frame relative to its caller.

    Returns:
        Frame: A frame object populated with context-specific attributes indicating
        the relationship between the calling frame and its immediate caller in terms of
        class inheritance (protected) and package containment (internal).
    """
	callingFrame = sys._getframe(1)
	origin = Frame(callingFrame)
	context = Frame(callingFrame.f_back)

	context.protected = issubclass(context.clsRef, origin.clsRef) if context.clsRef and origin.clsRef else False
	context.internal = (origin.package == context.package)

	return context


def parseFile(filepath):
	"""
	Parses Python modules as text files, mapping line ranges to class names in the internal cache.

	Args:
		filepath (str): Path to the Python file to be parsed.

	The function reads through the provided file line by line, identifying class definitions
	and tracking their line numbers to create a map of class names against their line ranges.
	This map is used later to determine class context from line numbers during stack frame analysis.
	"""

	# classMap is the mapping for this file. Each entry is a tuple of (start, end) line numbers,
	# paired to a class string. Module code is provided as an empty string ""
	classMap = {}

	try:
		# Open the file and read all lines into a list
		with open(filepath, 'r') as file:
			lines = file.readlines()

		# Prepare to track class definitions and their indentations
		stack = []  # Each new class definition is pushed/popped here.

		# This is what each entry in the stack will look like
		current = {
			"cls": "",	# The current class context, empty string for module-level code
			"line": 1, 		# The first line of the current context
			"indent": 0
		}

		indentMultiple = 0	# Each file can have its own indentation metric.  Tabs, spaces, 2/3/4 characters?  We assume the multiple based on the first instance.
		openDoubleComment = False  # Are we inside a multi-line double-quoted comment?
		openSingleComment = False  # Are we inside a multi-line single-quoted comment?

		# Iterate over each line in the file
		for i, fullLine in enumerate(lines, start=1):
			line = fullLine.strip()

			# Skip empty lines
			if line == "":
				continue

			# Calculate the current line's indentation
			indent = max(0, len(fullLine) - len(line) - 1)

			# Detect and set the basic indentation unit.  "0" is considered not set/detected.
			if indentMultiple == 0 and indent > 0:
				indentMultiple = indent
				stack[-1]["indent"] = indent

			# Manage multi-line comments
			if openDoubleComment and '"""' in line:
				openDoubleComment = False
			elif line.startswith('"""'):
				quote_count = line.count('"""')
				if quote_count == 1:
					openDoubleComment = True

			if openSingleComment and "'''" in line:
				openSingleComment = False
			elif line.startswith("'''"):
				quote_count = line.count('"""')
				if quote_count == 1:
					openSingleComment = True

			if not openDoubleComment and not openSingleComment:
				# Begin relevant parsing of actual code...

				if line.startswith("class "):
					# Close the last class entry
					if current["line"] < (i - 1):
						classMap[(current["line"], i - 1)] = current["cls"]

					# Start a new class entry
					current["cls"] = line.split()[1].split('(')[0].strip(':')
					current["line"] = i
					stack.append({
						"cls":current["cls"],
						"line":current["line"],
						"indent": indent + indentMultiple
					})

				elif len(stack) == 0:
					stack.append({
						"cls": "",
						"line": current["line"],
						"indent": indent
					})

				elif indent < stack[-1]["indent"]:
					# Handle exiting class scope based on indentation
					# Save the last class as the next entry in the classMap
					classMap[(stack[-1]["line"], i - 1)] = stack[-1]["cls"]

					# Working from the end of our array, we'll cleanup until we match the same indentation.
					for j in range(len(stack) - 1, -1, -1):
						entry = stack[j]

						if indent < entry["indent"]:
							stack.pop()
						elif indent == entry["indent"]:
							current["cls"] = entry["cls"]
							current["line"] = i
							entry["line"] = i
							break

		# Close any remaining open classes
		if current["cls"]:
			classMap[(current["line"], len(lines))] = current["cls"]

		# I tried parsing the FQN in parseFile, but the package can vary beyond simply the path, as it could be assembled from across disparate locations.
		# We'll populate the value from the sys._getframe() method, as it is Python's understanding of the package.

		_classMapping[filepath] = classMap
	except IOError:
		print(f"Error reading file: {filepath}")
	except SyntaxError:
		print(f"Syntax error in file: {filepath}")


def getClassName(path, linenumber):
	""" Returns the class name for a given line number in the specified file using pre-sorted class line ranges. """

	# Ensure the class map is parsed and available
	if path not in _classMapping:
		parseFile(path)

	classMap = _classMapping.get(path, {})
	sortedKeys = list(classMap.keys())
	left = 0
	right = len(sortedKeys) - 1

	while left <= right:
		mid = (left + right) // 2
		start = sortedKeys[mid][0]
		end = sortedKeys[mid][1]
		if start <= linenumber <= end:
			return classMap[(start, end)]
		elif linenumber < start:
			right = mid - 1
		else:
			left = mid + 1

	return None