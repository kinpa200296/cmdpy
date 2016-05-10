def __cmd_decorator(func, cmd_name, cmd_prefix):
    func._cmd_prefix = cmd_prefix
    func._cmd_name = cmd_name
    return func


def cmd_helper(func, cmd_name):
    return __cmd_decorator(func, cmd_name, 'help')


def cmd_func(func, cmd_name):
    return __cmd_decorator(func, cmd_name, 'do')


def cmd_completer(func, cmd_name):
    return __cmd_decorator(func, cmd_name, 'complete')
