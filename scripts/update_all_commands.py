"""
    Parses all files in discord_commands extracting the command and the
    object name for the command, then writes it to
    discord_commands/all_commands.py
"""

import os
import re


cmd_file_pattern = re.compile(r'\w*_command\.py')


def get_all_command_files():
    """Gets all files matching the cmd_file_pattern"""
    result = []
    for root, _, files in os.walk("discord_commands/"):
        # Skip __pycache__ folders
        if root.endswith('__pycache__'):
            continue

        for f in files:
            if cmd_file_pattern.match(f):
                result.append(root + "/" + f)

    return result


def build_all_commands(files):
    """
    Builds a dictionary of all of the commands

    :param files: list

    :return: dictionary of command to class name for the command
    """

    cmd_pattern = re.compile(r'self\._command = \"(![a-zA-Z0-9]*)\"')
    class_pattern = re.compile(r'class ([a-zA-Z0-9]*)\(')
    cmds = {}
    files_to_remove = []

    for f in files:
        command = class_name = ""
        for _, line in enumerate(open(f)):
            cmd_match = cmd_pattern.search(line)
            class_match = class_pattern.search(line)
            if cmd_match:
                command = cmd_match.group(1)

            if class_match:
                class_name = class_match.group(1)

        if class_name and command:
            cmds[command] = {'class': class_name, 'file': f}
        else:
            files_to_remove.append(f)

    # Remove files that had no command
    for f in files_to_remove:
        files.remove(f)

    return cmds, files


def write_new_all_commands(cmd_dict, files):
    """
    Writes a new all_commands.py using the commands given in cmd_dict

    :param cmd_dict: dict
    :param files: list
    """
    fo = open('discord_commands/all_commands.py', 'w')
    fo.write('"""\n\tHouses a dictionary holding references to every command' +
             'available\n\tThis file is generated by scripts/' + 'update_all_commands.py\n"""\n')

    # Generate import lines
    for f in files:
        from_string = "from ."
        import_string = " import "
        modules = f.replace('discord_commands/', '')
        modules = modules.replace('.py', '')
        modules = modules.split('/')

        for module in modules:
            from_string += module + "."

        # Remove the trailing period
        from_string = from_string[:-1]
        for value in cmd_dict.values():
            if value['file'] == f:
                import_string += value['class']
        fo.write(from_string + import_string + "\n")

    # Write out command dict
    fo.write("\n\ncommands = {\n")
    for command, value in cmd_dict.items():
        print("Inserting entry for {}".format(command))
        fo.write("\t'{0}': {1},\n".format(command, value['class']))
    fo.write("}\n")


if __name__ == "__main__":
    cmd_files = get_all_command_files()
    commands, cmd_files = build_all_commands(cmd_files)
    write_new_all_commands(commands, cmd_files)
