from os.path import dirname, abspath, join

ROOT_DIR = join(dirname(abspath(__file__)))  # This is the path to the root
SOURCE_DIR = join(ROOT_DIR, "src")

RESOURCES_PATH = join(ROOT_DIR, "resources")
OUTPUT_PATH = join(ROOT_DIR, "output")
CLASSIFIERS_PATH = join(OUTPUT_PATH, "classifiers")
TEST_PATH = join(ROOT_DIR, "tests")
TEST_DATA_PATH = join(TEST_PATH, "test_data")
EXCEPTIONS_PATH = join(SOURCE_DIR, "exceptions")
