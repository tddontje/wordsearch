"""
WordSearch - This program searches a given grid of letters for words contained
in a given dictionary file.

* The grid of letters will be randomly generated.
* The search for words have the following constraints:
  * Words will be search forwards, backwards, up, down and diaganol
  * Words will not be tested for wrapping of the edge of grid
* Dictionary will be given as a file (defaulting to words.txt)
"""
import unittest
import os.path
import argparse
import string
import random

class WordSearch():
    """
    WordSearch:
        __init__    :   setup object with defined grid
        find_words  :   find words in grid that matches dictionary
    """
    def __init__(self, dict_file: str, xsize: int = 15, ysize: int = 15):
        """
        Setup WordSearch object
            * initialize random grid using xsize and ysize values
            * load dictionary file to be used in word search

        :param dict_file:   Filename of dictionary to load
        :param xsize:       X-axis size of word grid
        :param ysize:       Y-axis size of word grid
        """
        print("initializing WordSearch")
        self.xsize = xsize
        self.ysize = ysize
        self.words_dictionary = self._load_dictionary(dict_file)
        self.letter_grid = self._generate_grid()
        self.found_words = set()

    def _load_dictionary(self, dict_file: str) -> list:
        """
        Load dictionary from file and order by length

        :param dict_file:   Filename of dictionary to load
        :return:            list of dictionary words in size order
        :exceptions:        if dictionary contains no words
        """
        words_dictionary = list()
        # load dictionary from file
        with open(dict_file, 'rt') as dictionary:
            words_dictionary = [word.split('\n')[0] for word in dictionary]
        # check for no entries in dictionary
        if len(words_dictionary) == 0:
            message = "No words in dictionary, need to specify a dictionary with at least 1 word."
            raise ValueError(message)
        else:
            print("loaded {} words in dictionary".format(len(words_dictionary)))

        # return sorted dictionary from shortest words to longest
        return sorted(words_dictionary, key=len)

    def _generate_grid(self):
        """
        Generate a random grid of letters to be searched based on object's xsize and ysize

        :return:            2d list of lists containing the grid of letters
        """
        letter_grid = [[random.choice(string.ascii_lowercase) for i in range(self.xsize)] for j in range(self.ysize)]
        return letter_grid

    def find_words(self) -> set:
        """
        Find words in grid.
        Using the grid of letter we will search the grid horizontally and diagonally forwards
        and backwards.  Since we are not worried about finding the exact location we can search
        for words based on a full slice instead of trying to searching through each position.

        :return:
        """
        # generate comparison string lists from grid
        print('generating grid comparision string list')
        comp_strings = list()
        comp_strings.extend(self._get_horizontal_str())
        comp_strings.extend(self._get_vertical_str())
        comp_strings.extend(self._get_diagonal_str())


        # find all dictionary words that occur in the comp_strings
        print('searching for words in comparison string list')
        for word_to_cmp in self.words_dictionary:
            if any(word_to_cmp in curr_string for curr_string in comp_strings):
                self.found_words.add(word_to_cmp)

        return self.found_words

    # Search methods.
    def _get_horizontal_str(self)->list:
        """
        get strings for horizontal comparisons

        :return: string_list of all horizontal strings forward and backward
        """
        string_list = list()
        for char_list in self.letter_grid:
            curr_string = ''.join(char_list)
            string_list.append(curr_string)
            bwd_string = ''.join(reversed(curr_string))
            string_list.append(bwd_string)

        return string_list

    def _get_vertical_str(self)->list:
        """
        get strings for vertical comparisons

        Currently

        :return: string_list of all vertical strings forward and backward
        """
        string_list = list()
        for curr_x in range(self.xsize):
            char_list = [self.letter_grid[y][curr_x] for y in range(self.ysize)]
            curr_string = ''.join(char_list)
            string_list.append(curr_string)
            bwd_string = ''.join(reversed(curr_string))
            string_list.append(bwd_string)

        return string_list

    def _get_diagonal_str(self)->list:
        """
        get strings for diagonal comparisons
        - Currently only getting diagonals that start at the top row

        :return: string_list of all diagonal strings to the right and left, forward and backward
        """
        string_list = list()
        # get diagonal from top row going to the right and then left
        for curr_x in range(self.xsize):
            d_upper_right = [self.letter_grid[inc][curr_x + inc] for inc in range(self.xsize - curr_x)]
            curr_string = ''.join(d_upper_right)
            string_list.append(curr_string)
            bwd_string = ''.join(reversed(curr_string))
            string_list.append(bwd_string)
            d_upper_left = [self.letter_grid[inc][(self.xsize - 1 - curr_x) - inc] for inc in range(self.xsize - curr_x)]
            curr_string = ''.join(d_upper_left)
            string_list.append(curr_string)
            bwd_string = ''.join(reversed(curr_string))
            string_list.append(bwd_string)

        return string_list

def check_axis(arg):
    try:
        value = int(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))

    if value <= 0:
        message = "Expected value > 0, got value = {}".format(value)
        raise argparse.ArgumentTypeError(message)
    return value

def check_file(arg):
    try:
        value = str(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))

    if not os.path.isfile(value):
        message = "Could not find dictionary file {}".format(value)
        raise argparse.ArgumentTypeError(message)
    return value

def main():
    parser = argparse.ArgumentParser('WordSearch a randomly generated grid')
    parser.add_argument('--xsize', dest='xsize', default=15, type=check_axis,
                        help='X-Axis size')
    parser.add_argument('--ysize', dest='ysize', default=15, type=check_axis,
                        help='Y-Axis size')
    parser.add_argument('--dictionary', dest='dict_file', default='words.txt', type=check_file,
                        help='dictionary filename')

    args = parser.parse_args()

    print("Xsize={}, Ysize={}, Dictionary={}".format(args.xsize, args.ysize, args.dict_file))
    grid = WordSearch(args.dict_file, args.xsize, args.ysize)
    found = grid.find_words()
    print("found following {} words:".format(len(found)))
    print(found)

if __name__ == '__main__':
    main()

class TestWordSearch(unittest.TestCase):
    def test_create_with_no_words(self):
        """
        Test for object creation with dictionary of no words.
        """
        # verify the right exception is done
        self.assertRaises(ValueError, WordSearch, "nowords.txt")

    def test_create_default_grid(self):
        """
        Test for object creation using defaults
        """
        grid = WordSearch("words.txt")
        # verify dictionary is set
        self.assertTrue(len(grid.words_dictionary) > 0)
        # verify x-axis length
        self.assertTrue(len(grid.letter_grid) == 15)
        # verify y-axis length
        self.assertTrue(len(grid.letter_grid[0]) == 15)

    def test_create_1x100_grid(self):
        """
        Test for object creation of a grid that is 1 row and 100 chars
        """
        grid = WordSearch("words.txt", 1, 100)
        # verify dictionary is set
        self.assertTrue(len(grid.words_dictionary) > 0)
        # verify x-axis length
        self.assertTrue(len(grid.letter_grid) == 100)
        # verify y-axis length
        self.assertTrue(len(grid.letter_grid[0]) == 1)

    def test_create_100x1_grid(self):
        """
        Test for object creation of a grid that is 100 rows and 1 char
        """
        grid = WordSearch("words.txt", 100, 1)
        # verify dictionary is set
        self.assertTrue(len(grid.words_dictionary) > 0)
        # verify x-axis length
        self.assertTrue(len(grid.letter_grid) == 1)
        # verify y-axis length
        self.assertTrue(len(grid.letter_grid[0]) == 100)

    def test_create_100x100_grid(self):
        """
        Test for object creation of a grid that is 100 rows and 100 chars
        """
        grid = WordSearch("words.txt", 100, 100)
        # verify dictionary is set
        self.assertTrue(len(grid.words_dictionary) > 0)
        # verify x-axis length
        self.assertTrue(len(grid.letter_grid) == 100)
        # verify y-axis length
        self.assertTrue(len(grid.letter_grid[0]) == 100)

    def test__get_horizontal_str(self):
        """
        Test that the string_list returned is of the right value.

        We force the grid to be a numeral string and then validate that the
        returned list looks correct.
        """
        input_grid = [[string.ascii_lowercase[x] for x in range(9)] for y in range(9)]
        expect_strings = ['abcdefghi',
                          'ihgfedcba',
                          'abcdefghi',
                          'ihgfedcba'
                          ]

        grid = WordSearch("words.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_strings = grid._get_horizontal_str()
        print(actual_strings)
        print("---")
        print(expect_strings)
        self.assertTrue(actual_strings[0] == expect_strings[0])
        self.assertTrue(actual_strings[1] == expect_strings[1])
        self.assertTrue(actual_strings[16] == expect_strings[2])
        self.assertTrue(actual_strings[17] == expect_strings[3])

    def test__get_vertical_str(self):
        """
        Test that the string_list returned is of the right value.

        We force the grid to be a numeral string and then validate that the
        returned list looks correct.
        """
        input_grid = [[string.ascii_lowercase[x] for x in range(9)] for y in range(9)]
        expect_strings = ['aaaaaaaaa',
                          'aaaaaaaaa',
                          'iiiiiiiii',
                          'iiiiiiiii'
                          ]

        grid = WordSearch("words.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_strings = grid._get_vertical_str()
        print(actual_strings)
        print("---")
        print(expect_strings)
        self.assertTrue(actual_strings[0] == expect_strings[0])
        self.assertTrue(actual_strings[1] == expect_strings[1])
        self.assertTrue(actual_strings[16] == expect_strings[2])
        self.assertTrue(actual_strings[17] == expect_strings[3])

    def test__get_diagonal_str(self):
        """
        Test that the string_list returned is of the right value.

        We force the grid to be a numeral string and then validate that the
        returned list looks correct.
        """
        input_grid = [[string.ascii_lowercase[x] for x in range(9)] for y in range(9)]
        expect_strings = ['abcdefghi',  # upper left to lower right
                          'ihgfedcba',  # ul2lr backwards
                          'ihgfedcba',  # upper right to lower left
                          'abcdefghi',  # ul2lr backwards
                          'bcdefghi',   # upper left to lower right (shift by one)
                          'ihgfedcb',   # ul2lr backwards
                          'hgfedcba',   # upper right to lower left (shift by one)
                          'abcdefgh',   # ul2lr backwards
                          'i',          # upper left last character
                          'i',          # upper left last character backwards
                          'a',          # upper right last character
                          'a'           # upper right last character backwards
                          ]

        grid = WordSearch("words.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_strings = grid._get_diagonal_str()
        print(actual_strings)
        print("---")
        print(expect_strings)
        self.assertTrue(actual_strings[0] == expect_strings[0])
        self.assertTrue(actual_strings[1] == expect_strings[1])
        self.assertTrue(actual_strings[2] == expect_strings[2])
        self.assertTrue(actual_strings[3] == expect_strings[3])
        self.assertTrue(actual_strings[4] == expect_strings[4])
        self.assertTrue(actual_strings[5] == expect_strings[5])
        self.assertTrue(actual_strings[6] == expect_strings[6])
        self.assertTrue(actual_strings[7] == expect_strings[7])
        self.assertTrue(actual_strings[32] == expect_strings[8])
        self.assertTrue(actual_strings[33] == expect_strings[9])
        self.assertTrue(actual_strings[34] == expect_strings[10])
        self.assertTrue(actual_strings[35] == expect_strings[11])

    def test_search_horizontal_fwd(self):
        """
        Test searching grid horizontal forward

        Checking the following conditions:
           1.  word at start
           2.  word in middle
           3.  word at end
           4.  word non-existant
        """
        input_grid = [['a','b','a','t','e','f','g','h','i'],
                      ['a', 'b', 'c', 'c', 'a', 'n', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'i', 'r', 'e', 'c', 't'],
                      ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']]

        expected_words = {'can', 'abate', 'direct'}
        grid = WordSearch("testwords.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_words = grid.find_words()
        self.assertTrue(len(expected_words) == len(actual_words))

    def test_search_vertical_fwd(self):
        """
        Test searching grid vertical forward

        Checking the following conditions:
           1.  word at top
           2.  word in middle
           3.  word at end
           4.  word non-existant
        """
        input_grid = [['c','b','a','t','e','f','g','h','i'],
                      ['o', 'b', 'c', 'c', 'a', 'n', 'g', 'h', 'i'],
                      ['m', 'b', 'c', 'p', 'e', 'f', 'g', 'h', 'i'],
                      ['p', 'b', 'c', 'y', 'e', 'f', 'g', 'a', 'i'],
                      ['u', 'b', 'c', 't', 'e', 'f', 'g', 'b', 'i'],
                      ['t', 'b', 'c', 'h', 'e', 'f', 'g', 'a', 'i'],
                      ['e', 'b', 'c', 'o', 'c', 'f', 'g', 't', 'i'],
                      ['r', 'b', 'c', 'n', 'a', 'r', 'e', 'e', 't'],
                      ['a', 'b', 'c', 'd', 'n', 'f', 'g', 'h', 'i']]

        expected_words = {'can', 'abate', 'computer', 'python'}
        grid = WordSearch("testwords.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_words = grid.find_words()
        self.assertTrue(len(expected_words) == len(actual_words))

    def test_search_diagonal_fwd(self):
        """
        Test searching grid diagonal forward

        Checking the following conditions:
           1.  word at start
           2.  word in middle
           3.  word at end
           4.  word non-existant
        """
        input_grid = [['d','b','a','t','e','f','g','h','n'],
                      ['a', 'i', 'c', 'c', 'a', 'n', 'g', 'a', 'i'],
                      ['a', 'b', 'r', 'd', 'e', 'f', 'c', 'h', 'i'],
                      ['a', 'b', 'c', 'e', 'e', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'c', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'e', 't', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'd', 'a', 'f', 'g', 'h', 'i'],
                      ['a', 'b', 'c', 'b', 'i', 'r', 'e', 'c', 't'],
                      ['a', 'b', 'a', 'd', 'e', 'f', 'g', 'h', 'i']]

        expected_words = {'can', 'direct'}
        grid = WordSearch("testwords.txt", 9, 9)
        grid.letter_grid = input_grid
        actual_words = grid.find_words()
        self.assertTrue(len(expected_words) == len(actual_words))
