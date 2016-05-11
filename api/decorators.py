class CmdDecorator(object):

    def __init__(self, cmd_name, cmd_aliases, cmd_prefix):
        self.cmd_prefix = cmd_prefix
        self.cmd_name = cmd_name
        self.cmd_aliases = cmd_aliases

    def __call__(self, func):
        func._cmd_prefix = self.cmd_prefix
        func._cmd_name = self.cmd_name
        func._cmd_aliases = self.cmd_aliases
        return func


def cmd_helper(cmd_name, cmd_aliases=None):
    return CmdDecorator(cmd_name, cmd_aliases, 'help')


def cmd_func(cmd_name, cmd_aliases=None):
    return CmdDecorator(cmd_name, cmd_aliases, 'do')


def cmd_completer(cmd_name, cmd_aliases=None):
    return CmdDecorator(cmd_name, cmd_aliases, 'complete')
