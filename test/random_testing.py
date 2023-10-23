import unittest
import random


def shuffle_tests(suite):
    test_list = list(suite)
    random.shuffle(test_list)
    return unittest.TestSuite(test_list)


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')

    shuffled_suite = shuffle_tests(suite)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(shuffled_suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    exit(exit_code)