# coding: utf8
from sorter import Sorter
from generator import Generator
from sorter import Sorter, Statistics
import time


class SortingMachine:
    algorithm_names = Sorter.algorithm_names
    array_types = Generator.array_types

    def __init__(self):
        menu_entries = [
            {
                'name': 'Sort numbers from keyboard',
                'fn': self.keyboard_input,
            },
            {
                'name': 'Sort numbers from file',
                'fn': lambda: print('plik')
            },
            {
                'name': 'Sort generated numbers',
                'fn': lambda: print('plik')
            },
            {
                'name': 'Benchmark',
                'fn': lambda: print('benchmark')
            },
            {
                'name': 'Quit',
                'fn': exit
            },
        ]
        while True:
            print('===MENU===')
            for i in range(len(menu_entries)):
                print('[{}] {}'.format(i + 1, menu_entries[i]['name']))

            menu_entries[self.menu_input(menu_entries)]['fn']()

    # MENU ENTRIES

    def keyboard_input(self):
        available_algorithms = self.algorithm_picker()
        print('Please enter numbers:')
        user_array = self.input_array()
        for algorithm_name in available_algorithms:
            array = user_array[:]
            print('\nSorting array using {}'.format(algorithm_name))
            print('INPUT: ', user_array)
            f = getattr(Sorter, algorithm_name)

            Statistics.reset()

            start_time = time.time()
            print('OUTPUT: ', f(array, verbose=True))
            elapsed_time = round(time.time() - start_time, 3)
            statistics = Statistics.report()
            print('Elapsed time: {}s\nComparisons: {}\nSwaps: {}\n'.format(elapsed_time, statistics['comparisons'], statistics['swaps']))

    # UTILITIES

    def is_int(self, string):
        string = list(string)
        for index, char in enumerate(string):
            if not char.isdigit() and ((index != 0) or (index == 0 and char != '-')):
                    return False
        return True

    def input_array(self):
        import re
        user_input = input().replace(',', ' ').replace('\n', ' ')
        user_input = re.sub(r' {2,}', ' ', user_input)
        return list(map(int, filter(self.is_int, user_input.split())))

    def menu_input(self, entries, allow_done=False):
        while True:
            print('choice> ', end='')
            choice = input()
            if allow_done and choice == 'done':
                return -1
            if choice.isdigit() and 0 < int(choice) <= len(entries):
                return int(choice) - 1

    def select_input(self, entries):
        select_options = {}
        for name in entries:
            select_options[name] = True
        print('Select entry, choose number to (di)select or type \'done\':')

        while True:
            for i in range(len(self.algorithm_names)):
                print('[{}]\t[{}] {}'.format(i+1, 'X' if select_options[entries[i]] else ' ', entries[i]))

            choice = self.menu_input(entries, allow_done=True)
            if choice >= 0:
                select_options[entries[choice]] = not select_options[entries[choice]]
            else:
                return list(filter(lambda key: select_options[key], select_options.keys()))

    def algorithm_picker(self):
        print('Choose sorting algorithm.')
        return self.select_input(self.algorithm_names)

    def array_type_picker(self):
        print('Choose array types.')
        return self.select_input(self.array_types)

sm = SortingMachine()