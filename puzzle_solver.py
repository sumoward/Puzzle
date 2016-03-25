"""
Test:

Using Ruby/Java/Python, generate an N x N grid, where N can be any number, and randomly populate the grid with letters (A-Z).

Using the provided dictionary file find all:

Horizontal words from left to right in your grid

Horizontal words from right to left in your grid

Vertical words from top to bottom in your grid

Vertical words from bottom to top in your grid

Diagonal words from left to right in your grid

Diagonal words from right to left in your grid
"""
import pickle
import string
import random
import numpy
import time


def timing(f):
    """
    Wrapper to time a function
    :param f: function we wish to time
    """

    def wrap(*args, **kwargs):
        print('Timing....')
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print(f.__name__, 'function took %0.3f ms' % ((time2 - time1) * 1000.0))
        print('....end Timimg')
        return ret

    return wrap


class PuzzleSolver:
    def __init__(self, grid_size=4, file='dict1.txt', persist="save_default.p"):
        """
        Constructor
        :param grid_size: default 4
        :param file: default dict.txt
        :return:
        """
        self.grid_size = grid_size
        self.file = file
        self.persist = persist
        self.sorted_words = []
        self.main()

    def make_game_grid(self):
        """
        Create an n by n array using numpy
        :param n: dimensions of array default is 4
        :return: a numpy array
        """
        return numpy.array([[random.choice(string.ascii_uppercase) for breath in range(self.grid_size)] for depth in
                            range(self.grid_size)])

    @timing
    def read_in_file(self, file):
        """
        read in a file and store it as a trie
        :param file: file we read in to build trie
        :return: trie
        """
        with open(self.file) as doc:
            trie = dict()
            for line in doc:
                line = line.split(' ')[0]
                self.make_trie(trie, line.rstrip())
            return trie

    def make_trie(self, root, *words):
        """ make a trie from input

        :param root:
        :param words:
        :return: root
        """
        _end = '_end_'
        for word in words:
            current_dict = root
            for letter in word:
                current_dict = current_dict.setdefault(letter, {})
            current_dict[_end] = word

            return root

    def search_columns_and_rows(self, array, reverse=False, transpose=False):
        """
        get the four letters combination left to right and top to bottom and their opposites
        :param array: the n by n grid for the puzzle
        :param reverse: reverse the rows
        :param transpose: transpose the array
        :return:
        """
        # to get the columns transpose them and now they are the rows
        if transpose:
            array = array.T
        # reverse the rows to get right to left
        if reverse:
            array = numpy.fliplr(array)
        words = []
        for x, row in enumerate(array):
            word = ''.join(row)
            if len(word) > 1:
                words.append(word)
        return words

    def get_diagonal_words(self, array, reverse=False):
        """
        search the diagonals of the array and return all diagonals combinations of two or greater
        :param array:
        :param reverse: reverse the direction of the search
        :return:
        """
        if reverse:
            array = numpy.fliplr(array)
        diagonal_array = self.get_diagonal(array)
        words = []
        for row in diagonal_array:
            word = ''.join(row)
            if len(word) > 1:
                words.append(word)
        return words

    def get_diagonal(self, array):
        """
        gets lower-left-to-upper-right and upper-left-to-lower-right diagonals.
        :param array:array to search
        :return:
        """
        diags = [array[::-1, :].diagonal(i) for i in range(-array.shape[0] + 1, array.shape[1])]

        # Now back to the original array to get the upper-left-to-lower-right diagonals,
        # starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
        diags.extend(array.diagonal(i) for i in range(array.shape[1] - 1, -array.shape[0], -1))
        return diags

    def check_words_in_trie(self, trie, words):
        """
        check list against a trie
        :param trie:
        :param words:
        :return:
        """
        result = []
        # get the unique combinations for our search
        word_set = set(words)
        print('The Number of possible combinations is:', len(words), '.\n The Number of unique combinations is:',
              len(word_set), '.')
        for word in word_set:
            checked = self.in_trie(trie, word)
            if checked:
                result.append(checked)
        return result

    def in_trie(self, trie, word):
        """
        check the tre for the existence of a word
        :param trie: the rie we wish to search
        :param word:
        :return: boolean or word if present
        """
        current_dict = trie
        for letter in word:
            if letter in current_dict:
                current_dict = current_dict[letter]
            else:
                return False
        else:
            if '_end_' in current_dict:
                return current_dict['_end_']
            else:
                return False
        return False

    def all_words(self, all_possible_words):
        """
        Takes all four letter combinations and get all two and greater combinations
        :param all_possible_words: list of lists of 4 letter combination from grid
        :return: all possible two letter combinations
        """
        result = []
        for word in all_possible_words:
            result = result + [word[i:j]
                               for i in range(len(word)) for j in range(i + 2, len(word) + 1)]

        return result

    def persist_trie(self, trie):
        """
        Persist the trie so we do not have to rebuild it each time
        :param trie:
        :return:
        """
        pickle.dump(trie, open(self.persist, "wb"))

    def retrieve_trie(self):
        """
        We retrieve the trie from pickle
        :return:
        """
        trie = pickle.load(open(self.persist, "rb"))
        return trie

    @timing
    def main(self):
        """
        function to sole an N by N grid
        :param n:
        :return:
        """
        grid = self.make_game_grid()
        print(self.grid_size, ' by ', self.grid_size, 'grid')
        trie = self.retrieve_trie()
        if not trie:
            trie = self.read_in_file(self.file)
            self.persist_trie(trie)

        all_possible_words = []
        # left to right rows
        all_possible_words = all_possible_words + self.search_columns_and_rows(grid)
        # right to left rows
        all_possible_words = all_possible_words + self.search_columns_and_rows(grid, reverse=True, transpose=False)
        # left to right columns
        all_possible_words = all_possible_words + self.search_columns_and_rows(grid, reverse=False, transpose=True)
        # right to left columns
        all_possible_words = all_possible_words + self.search_columns_and_rows(grid, reverse=True, transpose=True)

        # handle all possible sun sets of the array row
        all_possible_words = self.all_words(all_possible_words)
        # get diagonal letters top to bottom
        all_possible_words = all_possible_words + self.get_diagonal_words(grid)
        # get diagonal letters  bottom to top
        all_possible_words = all_possible_words + self.get_diagonal_words(grid, reverse=True)
        ans = self.check_words_in_trie(trie, all_possible_words)
        self.sorted_words = sorted(ans, key=len)
        if self.sorted_words:
            print("The number of words in the solution is: %s." % (len(ans),))
            print("The shortest word in the solution is: %s." % (self.sorted_words[0],))
            print("The longest word in the solution is: %s." % (self.sorted_words[-1],))
        print('the possible words in this grid are ', self.sorted_words)
        return self.sorted_words


if __name__ == '__main__':
    print('Start...')
    file = "dict.txt"
    persist = "save.p"
    puzzle_solution = PuzzleSolver(8, file, persist)
    # puzzle_solution
    print('...Complete')
