import random
import sys

from behave.__main__ import Configuration, run_behave, Runner


"""
Shuffle class that has function used to find all the feature files and randomize these files
"""
class Shuffle_Features(Runner):

    def feature_locations(self):
        locations = super().feature_locations()
        random.shuffle(locations)
        return locations


def main():
    config = Configuration()
    return run_behave(config, runner_class=Shuffle_Features)


if __name__ == '__main__':
    sys.exit(main())
