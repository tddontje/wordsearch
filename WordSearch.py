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
            words_dictionary = [word for word in dictionary]
        # check for no entries in dictionary
        if len(words_dictionary) == 0:
            message = "No words in dictionary, need to specify a dictionary with at least 1 word."
            raise ValueError(message)
        else:
            print("{} words in dictionary".format(len(words_dictionary)))

        # return sorted dictionary from shortest words to longest
        return sorted(words_dictionary, key=len)

    def _generate_grid(self):
        """
        Generate a random grid of letters to be searched based on object's xsize and ysize

        :return:            2d list of lists containing the grid of letters
        """
        letter_grid = [[random.choice(string.ascii_lowercase) for i in range(self.xsize)] for j in range(self.ysize)]
        return letter_grid

    def find_words(self) -> list:
        """
        Find words in grid

        :return:    list of words found in grid
        """
        found = list()
        print("finding words...")
        for y_pos in range(self.ysize):
            for x_pos in range(self.xsize):
                found.append(self._search_forward(x_pos, y_pos))
                found.append(self._search_backward(x_pos, y_pos))
                found.append(self._search_up(x_pos, y_pos))
                found.append(self._search_down(x_pos, y_pos))
                found.append(self._search_diagonal(x_pos, y_pos))
        return found

    # Search methods.
    # The following might be able to be collapsed to one method taking a direction parameter
    def _search_forward(self, x_pos: int, y_pos) -> list:
        """
        Search for words in dictionary from X,Y position on forward

        :param x_pos:   Position of start character in the X axis
        :param y_pos:   Position of start character in the Y axis
        :return:        list of words found
        """
        found = list()
        return found

    def _search_backward(self, x_pos: int, y_pos) -> list:
        """
        Search for words in dictionary from X,Y position on backward

        :param x_pos:   Position of start character in the X axis
        :param y_pos:   Position of start character in the Y axis
        :return:        list of words found
        """
        found = list()
        return found

    def _search_up(self, x_pos: int, y_pos) -> list:
        """
        Search for words in diction from X,Y position on up

        :param x_pos:   Position of start character in the X axis
        :param y_pos:   Position of start character in the Y axis
        :return:        list of words found
        """
        found = list()
        return found

    def _search_down(self, x_pos: int, y_pos) -> list:
        """
        Search for words in diction from X,Y position on down

        :param x_pos:   Position of start character in the X axis
        :param y_pos:   Position of start character in the Y axis
        :return:        list of words found
        """
        found = list()
        return found

    def _search_diagonal(self, x_pos: int, y_pos) -> list:
        """
        Search for words in diction from X,Y position diagonal

        :param x_pos:   Position of start character in the X axis
        :param y_pos:   Position of start character in the Y axis
        :return:        list of words found
        """
        found = list()
        return found


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
    grid.find_words()

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

    def test_search_forward(self):
        """
        Test searching grid forward (duplicate for other searches

        We'll want to loop over test with a set single word dictionary and grid with and without word
        Checking the following conditions:
           1.  word at start
           2.  word in middle
           3.  word at end
           4.  word non-existant
        """