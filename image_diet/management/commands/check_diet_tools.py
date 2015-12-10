import copy
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

    # Preferred pipelines. Feels like they (as tools) should be saved in
    # external file, but can't think of a benefit of doing so.
    pipelines = {
        'png': ['optipng', 'advpng', 'pngcrush'],
        'gif': ['gifsicle'],
        'jpeg': ['jpegtran', 'jpegoptim']
    }

    @staticmethod
    def find_tools(tools):
        commands = {}
        for tool in tools:
            path = find_executable(tool)  # Empty string if not found
            if path:
                commands[tool] = path
        return commands

    @classmethod
    def cmds_to_pipelines(cls, commands):
        found = set([x for x in commands])
        pipelines = {}
        for name in cls.pipelines:
            pipelines[name] = [x for x in cls.pipelines[name] if x in found]
            if not len(pipelines[name]):
                del pipelines[name]
        return pipelines

    @staticmethod
    def section_to_yaml(section, commands):
        output = ""
        if commands:
            section = {section: commands}
            output = yaml.dump(section, default_flow_style=False)
        return output

    def handle(self, *args, **options):
        commands = self.find_tools(self.tools)
        pipelines = self.cmds_to_pipelines(commands)
        output = self.section_to_yaml('commands', commands)
        output += self.section_to_yaml('pipelines', pipelines)
        self.stdout.write(output)
        self.stdout.write("\n")
