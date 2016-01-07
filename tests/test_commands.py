import os
from os.path import abspath, dirname, join
import pyimagediet.helpers as helpers
import pytest
try:
        from StringIO import StringIO
except ImportError:
        from io import StringIO

from image_diet.management.commands import check_diet_tools as check
from image_diet.management.commands import diet_images as diet


TOOLS_DIR = os.getenv('DIET_TOOLS_DIR', '/usr/local/bin')
TEST_DIR = join(abspath(dirname(__file__)), 'test_files')


#
# CHECK_DIET_TOOLS TESTS
#
def test_check_diet_tools_output():
    expected = """\
commands:
  optipng: {0}/optipng
pipelines:
  png:
  - optipng

""".format(TOOLS_DIR)

    helpers.TOOLS = ('optipng',)

    cmd = check.Command()
    cmd.stdout = StringIO()

    cmd.handle()
    output = cmd.stdout.getvalue()
    assert output == expected


#
# DIET_IMAGES TESTS
#
@pytest.fixture
def testfiles():
    filenames = ('png_test.png', 'stockholm.jpg')
    return [join(TEST_DIR, fname) for fname in filenames]


def test_get_files_returns_all_files_in_directory(testfiles):
    output = [f for f in diet.Command.get_files(TEST_DIR)]
    assert output == testfiles


def test_get_files_returns_all_files_from_all_specified_directories(testfiles):
    expected = testfiles * 2
    output = [f for f in diet.Command.get_files(TEST_DIR, TEST_DIR)]
    assert output == expected


def test_diet_images_output(testfiles):
    # Replace expensive diet call
    real_diet = diet.pyimagediet.diet
    diet.pyimagediet.diet = lambda x, y: False

    expected = "".join(["Processing: {0}\n".format(fname) for fname in
                        testfiles])
    cmd = diet.Command()
    cmd.stdout = StringIO()
    cmd.handle(TEST_DIR)
    output = cmd.stdout.getvalue()
    assert output == expected

    diet.pyimagediet.diet = real_diet
