from unittest import TestCase
import string
import numpy
from puzzle_solver import PuzzleSolver


class TestNumbers(TestCase):
    """
    Unit test suite for Puzzle solver
    """

    def setUp(self):
        """
        set up test data and expected results
        """
        self.puzzle_solution = PuzzleSolver()

        self.test_char_array = numpy.array(
            [['C', 'A', 'T', 'X'], ['X', 'C', 'A', 'R'], ['C', 'A', 'R', 'P'], ['X', 'G', 'O', 'D']])
        self.file = "dict1.txt"
        self.expected_trie = {'T': {'A': {'R': {'_end_': 'TAR'}}}, 'D': {'O': {'G': {'_end_': 'DOG'}}},
                              'G': {'O': {'D': {'_end_': 'GOD'}, '_end_': 'GO'}},
                              'C': {'A': {'T': {'_end_': 'CAT'}, 'R': {'P': {'_end_': 'CARP'}, '_end_': 'CAR'}}},
                              'R': {'A': {'T': {'_end_': 'RAT'}}}}

    def test_make_grid(self):
        """
        check an array of appropriate size is created
        """

        number_of_lines = 4
        expected = (number_of_lines, number_of_lines)
        result = self.puzzle_solution.make_game_grid()
        self.assertEqual(result.shape, expected)
        for element in numpy.nditer(result):
            # convert element to string from numpy element for comparison
            self.assertTrue(str(element) in string.ascii_uppercase)

    def test_create_trie(self):
        """
        test if a trie is created from an external file
        """
        trie = self.puzzle_solution.read_in_file(self.file)

        self.assertEqual(trie, self.expected_trie)

    def test_search_columns_and_rows(self):
        """
        test that we find the rows from in the appropriate directions
        """
        result_left_to_right = self.puzzle_solution.search_columns_and_rows(self.test_char_array)
        result_right_to_left = self.puzzle_solution.search_columns_and_rows(self.test_char_array, reverse=True)
        result_top_to_bottom = self.puzzle_solution.search_columns_and_rows(self.test_char_array, transpose=True)
        result_bottom_to_top = self.puzzle_solution.search_columns_and_rows(self.test_char_array, reverse=True,
                                                                            transpose=True)

        expected_result_left_to_right = ['CATX', 'XCAR', 'CARP', 'XGOD']
        expected_result_right_to_left = ['XTAC', 'RACX', 'PRAC', 'DOGX']
        expected_result_top_to_bottom = ['CXCX', 'ACAG', 'TARO', 'XRPD']
        expected_result_bottom_to_top = ['XCXC', 'GACA', 'ORAT', 'DPRX']

        self.assertEqual(result_left_to_right, expected_result_left_to_right)
        self.assertEqual(result_right_to_left, expected_result_right_to_left)
        self.assertEqual(result_top_to_bottom, expected_result_top_to_bottom)
        self.assertEqual(result_bottom_to_top, expected_result_bottom_to_top)

    def test_all_words(self):
        """
        test turning rows and columns in two words of length two or greater
        """
        test_list = ['CATX', 'XCAR', 'CARP', 'XGOD',
                     'XTAC', 'RACX', 'PRAC', 'DOGX',
                     'CXCX', 'ACAG', 'TARO', 'XRPD',
                     'XCXC', 'GACA', 'ORAT', 'DPRX']

        result = self.puzzle_solution.all_words(test_list)
        expected_result = ['CA', 'CAT', 'CATX', 'AT', 'ATX', 'TX', 'XC', 'XCA', 'XCAR', 'CA', 'CAR', 'AR',
                           'CA', 'CAR', 'CARP', 'AR', 'ARP', 'RP', 'XG', 'XGO', 'XGOD', 'GO', 'GOD', 'OD',
                           'XT', 'XTA', 'XTAC', 'TA', 'TAC', 'AC', 'RA', 'RAC', 'RACX', 'AC', 'ACX', 'CX',
                           'PR', 'PRA', 'PRAC', 'RA', 'RAC', 'AC', 'DO', 'DOG', 'DOGX', 'OG', 'OGX', 'GX',
                           'CX', 'CXC', 'CXCX', 'XC', 'XCX', 'CX', 'AC', 'ACA', 'ACAG', 'CA', 'CAG', 'AG',
                           'TA', 'TAR', 'TARO', 'AR', 'ARO', 'RO', 'XR', 'XRP', 'XRPD', 'RP', 'RPD', 'PD',
                           'XC', 'XCX', 'XCXC', 'CX', 'CXC', 'XC', 'GA', 'GAC', 'GACA', 'AC', 'ACA', 'CA',
                           'OR', 'ORA', 'ORAT', 'RA', 'RAT', 'AT', 'DP', 'DPR', 'DPRX', 'PR', 'PRX', 'RX']
        self.assertEqual(result, expected_result)

    def test_get_diagonal(self):
        """
        test diagonal array from array
        """
        results = self.puzzle_solution.get_diagonal(self.test_char_array)
        expected_results = [numpy.array(['C']),
                            numpy.array(['X', 'A']),
                            numpy.array(['C', 'C', 'T']),
                            numpy.array(['X', 'A', 'A', 'X']),
                            numpy.array(['G', 'R', 'R']),
                            numpy.array(['O', 'P']),
                            numpy.array(['D']),
                            numpy.array(['X']),
                            numpy.array(['T', 'R']),
                            numpy.array(['A', 'A', 'P']),
                            numpy.array(['C', 'C', 'R', 'D']),
                            numpy.array(['X', 'A', 'O']),
                            numpy.array(['C', 'G']),
                            numpy.array(['X'])]
        results = [result.tolist() for result in results]
        expected_results = [result.tolist() for result in expected_results]
        self.assertEqual(results, expected_results)

    def test_get_diagonal_words(self):
        """
        test the words from diagonals of the grid are provided
        """
        result_top = self.puzzle_solution.get_diagonal_words(self.test_char_array)
        result_bottom = self.puzzle_solution.get_diagonal_words(self.test_char_array, reverse=True)

        expected_result_top = ['XA', 'CCT', 'XAAX', 'GRR', 'OP', 'TR', 'AAP', 'CCRD', 'XAO', 'CG']
        expected_result_bottom = ['RT', 'PAA', 'DRCC', 'OAX', 'GC', 'AX', 'TCC', 'XAAX', 'RRG', 'PO']

        self.assertEqual(result_top, expected_result_top)
        self.assertEqual(result_bottom, expected_result_bottom)

    def test_check_in_trie(self):
        """
        test that we can search the trie for a word
        """
        words = ['CAT',
                 'DOG',
                 'CAR',
                 'CARP',
                 'TAR',
                 'GOD',
                 'RAT', 'GO']

        for word in words:
            result = self.puzzle_solution.in_trie(self.expected_trie, word)
            self.assertEqual(word, result)
