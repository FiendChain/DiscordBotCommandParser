from Tree import Tree
from Command import Command
import re

def parse_command(tree, command, prefix="!"):
    if command.startswith(prefix):
        args = re.split(r'\s+', command[1:])
        if args and args[0] == 'help':
            return parse_help(tree, args[1:])
        return parse_args(tree, args)
    return lambda: print('Command must start with \'!\'')

def parse_help(tree, args):
    if len(args) == 0:
        branch = tree
    else:
        branch = tree.get_branch(args[0])
    # if tree and still further to go
    if isinstance(branch, Tree) and len(args) > 0:
        return parse_help(branch, args[1:])
    # if reached end of valid path
    else:
        return lambda: show_help(branch)

def show_help(branch):
    if not branch:
        print("Invalid command for help!")
        return
    if isinstance(branch, Tree):
        print("Valid commands are:\n{}".format(branch.help))
    elif isinstance(branch, Command):
        print("Description: {0.description}".format(branch))
    elif isinstance(branch, str):
        print(branch)
    else:
        print("Help for {}".format(branch))
        print(">> output:", end=' ')
        branch()

def parse_args(tree, args):
    if len(args) == 0:
        branch = tree.get_branch(None)
    else:
        branch = tree.get_branch(args[0])
    if isinstance(branch, Tree):
        return parse_args(branch, args[1:])
    else:
        return branch

base_commands = Tree(
    regex={
        r"<@\d+>": Command(
            lambda: print('User being flagged !(user)'),
            "Flags a user",
        )
    },
)

insult_commands = Tree(
    description="Insult various people",
    empty=Command(
        lambda: print('You insulted yourself'),
        "Insult your dignity",
    ),
    keywords={
        "stats": Tree(
            description="Lists stats of insults",
            empty=Command(
                lambda: print('You got your own insult stats'),
                "Get your insult stats"
            ),
            regex={
                r"<@\d+>": Command(
                    lambda: print("You got (user) insult stats"),
                    "Get another user's stats"
                ),
            },
        ),
        "reset": Command(
            lambda: print("Resetting insults database"),
            "Rests the insults database",
        ),
    },
)

@insult_commands.register_keyword("decorated", "A function added via a decorator")
def decorated_function():
    print("I am decorated")

base_commands.add_keyword('insult', insult_commands)

while True:
    command = input('Enter command: ')
    func = parse_command(base_commands, command)
    if func:
        func()
    else:
        print('Invalid command')


