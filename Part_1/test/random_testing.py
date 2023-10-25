import unittest
import random


def randomize_test(suite):
    test_list = list(suite)
    random.shuffle(test_list)
    return unittest.TestSuite(test_list)


def testing():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='', pattern='test_*.py')

    random_suite = randomize_test(suite)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(random_suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':
    exit_code = testing()
    exit(exit_code)
