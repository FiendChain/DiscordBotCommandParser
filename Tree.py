import re
from Command import Command

class Tree:
    def __init__(self, empty=None, default=None, keywords={}, regex={}, description=None):
        self.empty = empty
        self.default = default
        self.keywords = {}
        self.regex = {}
        self.description = description
        # add keywords and regex
        self.add_keywords(keywords)
        self.add_regexes(regex)

    def get_branch(self, keyword):
        if not keyword or len(keyword) <= 2:
            return self.empty
        if keyword in self.keywords:
            return self.keywords[keyword]
        for regex, command in self.regex.items():
            results = re.findall(regex, keyword)
            if results:
                return command
        return self.default

    # setters for empty and default
    @property
    def empty(self):
        return self._empty
    
    @empty.setter
    def empty(self, command):
        if not command:
            self._empty = command
        else:
            command = self.convert_command(command)
            self._empty = command

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, command):
        if not command:
            self._default = command
        else:
            command = self.convert_command(command)
            self._default = command

    # add multiple keywords and regex
    def add_keywords(self, keywords):
        for keyword, command in keywords.items():
            self.add_keyword(keyword, command)

    def add_regexes(self, regexes):
        for regex, command in regexes.items():
            self.add_regex(regex, command)

    # add keyword/regex
    def add_keyword(self, keyword, command):
        if keyword in self.keywords:
            raise KeyError('Keyword \'{}\' already taken in {}'.format(keyword, self))
        command = self.convert_command(command)
        self.keywords[keyword] = command

    def add_regex(self, regex, command):
        if regex in self.regex:
            raise KeyError('Regex pattern \'{}\' already taken in {}'.format(regex, self))
        command = self.convert_command(command)
        self.regex[regex] = command

    # function decorators to dynamically add existing functions
    def register_keyword(self, keyword, description=None):
        def decorator(func):
            command = Command(func, description)
            self.add_keyword(keyword, command)
            return func
        return decorator

    def register_regex(self, regex, description=None):
        def decorator(func):
            command = Command(func, description)
            self.add_regex(regex, command)
            return func
        return decorator

    # convert intro appropriate object, otherwise raise TypeError
    def convert_command(self, command):
        if isinstance(command, Command):
            return command
        if callable(command):
            command = Command(command)
        elif not isinstance(command, (Tree, Command)):
            raise TypeError('Command must be callable or Command/Tree object\n{}'.format(command))
        return command

    @property
    def help(self):
        command_list = []
        if self.empty:  # valid command
            command_list.append('\'\': {}'.format(self.empty.description))
        commands = list(self.keywords.items()) + list(self.regex.items())
        command_list.extend(('{}: {}'.format(key, command.description) for key, command in commands))
        return "\n".join(command_list)

    def __str__(self):
        branch_count = len(self.keywords) + len(self.regex)
        return "<Tree object> depth: {}, default: {}, empty: {}"\
            .format(branch_count, self.default, self.empty)
    
    def __repr__(self):
        return self.__str__()