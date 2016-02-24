"""
    Command for getting helptext for another command
"""

from .command import BaseCommand

class HelpCommand(BaseCommand):
    """
        Displays help for a command

        Required arguments:
            If left empty will list all available commands on system
            Otherwise pass in a command,
            Command (i.e. !dankmemes)

        Supported options:
            None
    """

    def __init__(self, command_str):
        super(HelpCommand, self).__init__(command_str)
        self._command = "!help"

    def run(self):
        from .all_commands import commands
        if self._args:
            return commands[self._args[0]].help()
        else:
            ret_str = "Commands: \n"
            for command in commands.keys():
                ret_str += "- " + command + "\n"
            return ret_str

    @staticmethod
    def help():
        return """
            Displays help for a command

            Required arguments:
                Command (i.e. !dankmemes)

            Supported options:
                None
        """
