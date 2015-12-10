import os
try:
        from StringIO import StringIO
except ImportError:
        from io import StringIO

from image_diet.management.commands import check_diet_tools as command


TOOLS_DIR = os.getenv('DIET_TOOLS_DIR', '/usr/local/bin')


def test_find_tools_returns_empty_dict_if_no_tools_are_found():
    tools = ('fakeoptipng',)
    cmds = command.Command.find_tools(tools)
    assert cmds == {}


def test_find_tools_finds_them():
    tools = ('optipng',)
    cmds = command.Command.find_tools(tools)

    path = os.path.join(TOOLS_DIR, 'optipng')
    assert cmds['optipng'] == path


def test_cmds_to_pipelines_returns_correct_dict_when_tools_present():
    commands = {
        'optipng': 'optipng',
        'pngcrush': 'pngcrush',
        'gifsicle': 'gifsicle',
        'jpegoptim': 'jpegoptim',
    }
    expected = {
        'png': ['optipng', 'pngcrush'],
        'gif': ['gifsicle'],
        'jpeg': ['jpegoptim']
    }
    output = command.Command.cmds_to_pipelines(commands)
    assert output == expected


def test_section_to_yaml_returns_empty_string_when_given_no_commands():
    output = command.Command.section_to_yaml('commands', {})
    assert output == ""


def test_section_to_yaml_returns_correct_yaml_when_tools_present():
    tools = {
        'advpng': '/bin/advpng',
        'optipng': '/bin/optipng',
    }
    expected = """\
commands:
  advpng: /bin/advpng
  optipng: /bin/optipng
"""
    output = command.Command.section_to_yaml('commands', tools)
    assert output == expected


def test_handles_output():
    expected = """\
commands:
  optipng: {0}/optipng
pipelines:
  png:
  - optipng

""".format(TOOLS_DIR)

    cmd = command.Command()
    cmd.tools = ('optipng',)
    cmd.stdout = StringIO()

    cmd.handle()
    output = cmd.stdout.getvalue()
    assert output == expected
