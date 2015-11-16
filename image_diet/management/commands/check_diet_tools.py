from distutils.spawn import find_executable
from django.core.management.base import BaseCommand
import yaml

class Command(BaseCommand):
    help = ("Check which popular external compression tools are "
            "available and suggest commands section configuration.")

    # List of popular external tools to search for
    tools = (
        'jpegoptim',
        'jpegtran',
        'gifsicle',
        'optipng',
        'advpng',
        'pngcrush',
    )

    @staticmethod
    def find_tools(tools):
        commands = {}
        for tool in tools:
            path = find_executable(tool)  # Empty string if not found
            if path:
                commands[tool] = path
        return commands

    @staticmethod
    def cmds_to_yaml(commands):
        output = ""
        if commands:
            section = {'commands': commands}
            output = yaml.dump(section, default_flow_style=False)
        return output

    def handle(self, *args, **options):
        commands = self.find_tools(self.tools)
        output = self.cmds_to_yaml(commands)
        self.stdout.write(output)
        self.stdout.write("\n")
