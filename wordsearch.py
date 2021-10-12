#################################################################
# FILE : wordsearch.py
# WRITER : Naveh Mevorach, navehmevorach, 318284569
# EXERCISE : intro2cs2 ex5 2021
# DESCRIPTION: A simple program that finds words in a 2*2 matrix
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: None
#################################################################


import sys
import os.path


# Helpers functions
def yxzy_controller(matrix, d):
    """
    The func gets a matrix and return it with the right order for the current search direction in diagonal
    :param matrix: The given matrix
    :param d: The current search direction
    :return: sorted matrix
    """
    # For left & down the func will reverse all the lists in the matrix
    if d == "z":
        matrix = [lst[::-1] for lst in matrix]
    # For right & up the func will reverse the list it self
    if d == "w":
        matrix = matrix[::-1]
    # For left & up the func will reverse the matrix it self and the lists inside
    if d == "x":
        matrix = [lst[::-1] for lst in matrix][::-1]
    # For right & down the func will keep the list the way it is|

    # Returning the sorted matrix
    return matrix


def word_counter(lst, words):
    """
    The func counting how many time each word in a list appears init
    :param lst: a list of the words that was founded in the matrix
    :param words: a list with all the given words
    :return: a list with tuples [(word, count)]
    """
    results = []
    # iterating on all the words in the words list
    for word in words:
        # Counts how many time the current words appears in the list
        # if count > 0 it will be appended to the results list
        count = lst.count(word)
        if count > 0:
            results.append((word, count))
    return results


def find_words_in_ud_direction(words, matrix, max_length, rows, columns, direction):
    """
    The func gets a matrix and a directions that could be up or down
     and returning all the words from the words list that appears in the matrix in that direction
    :param words: list of the given words
    :param matrix: the given matrix
    :param max_length: the max length of a word in the given words list
    :param rows: the length of the rows
    :param columns: the length of the column
    :param direction: the direction to follow
    :return: list of all the words that appeared in the matrix
    """
    # Empty list to store all the matches
    matches = []
    # Set the direction
    d = -1 if direction == "u" else 1
    # Set the starting and ending points base on the direction
    first_starting_point = rows if direction == "u" else 0
    first_ending_point = 0 if direction == "u" else rows
    # The for loop runs on each row from 0 -> end, 1 ->  end and so go on
    # and checks for all the matches with max length of the max_length arg
    for c in range(columns):
        for r in range(first_starting_point, first_ending_point, d):
            # Set the starting and ending points base on the direction
            second_starting_points = r - 1 if direction == "u" else r
            second_ending_points = -1 if direction == "u" else rows
            # Set an empty string for concatenating the letters together
            word = ""
            for i in range(second_starting_points, second_ending_points, d):
                word = word + matrix[i][c]
                if word in words:
                    matches.append(word)
                # If the length of word that was concatenated is equal to max_length
                # there is no reason to keep searching for matches
                if len(word) == max_length:
                    break
    return matches


def find_words_in_rl_direction(words, matrix, max_length, rows, columns, direction):
    """
    The func gets a matrix and a directions that could be left or right
     and returning all the words from the words list that appears in the matrix in that direction
    :param words: list of the given words
    :param matrix: the given matrix
    :param max_length: the max length of a word in the given words list
    :param rows: the length of the rows
    :param columns: the length of the column
    :param direction: the direction to follow
    :return: list of all the words that appeared in the matrix
    """
    # Empty list to store all the matches
    matches = []
    # Set the direction
    d = -1 if direction == "l" else 1
    # Set the starting and ending points base on the direction
    first_starting_point = columns if direction == "l" else 0
    first_ending_point = 0 if direction == "l" else columns
    # The for loop runs on each column from 0 -> end, 1 ->  end and so go on
    # and checks for all the matches with max length of the max_length arg
    for r in range(rows):
        for c in range(first_starting_point, first_ending_point, d):
            # Set the starting and ending points base on the direction
            second_starting_points = c - 1 if direction == "l" else c
            second_ending_points = -1 if direction == "l" else columns
            # Set an empty string for concatenating the letters together
            word = ""
            for i in range(second_starting_points, second_ending_points, d):
                word = word + matrix[r][i]
                if word in words:
                    matches.append(word)
                # If the length of word that was concatenated is equal to max_length
                # there is no reason to keep searching for matches
                if len(word) == max_length:
                    break
    return matches


def find_words_in_yxzy_direction(words, matrix, max_length, rows, columns, direction):
    """
    The func will handle all the diagonals direction by sorting them all to the same direction
    and using the same iteration to find all the words in the matrix that were given in the words list
    :param words: list of the given words
    :param matrix: the given matrix
    :param max_length: the max length of a word in the given words list
    :param rows: the length of the rows
    :param columns: the length of the column
    :param direction: the direction to follow
    :return: list of all the words that appeared in the matrix
    """
    # Empty list to store all the matches
    matches = []
    # Re edit the Matrix depending on the searching direction
    matrix = yxzy_controller(matrix, direction)
    # The first for loop runs from 0 to rows in order to push the following count variable up each iteration.
    for i in range(rows):
        for r in range(columns, 0, -1):
            # Save the last word from the previous iteration
            word = ""
            # That variable help to get the next letter in diagonal
            count = 0
            for c in range(r, columns + 1):
                word += matrix[i + count][c - 1]
                count += 1
                # Checks if the word that was concatenated so far is in words
                if word in words:
                    matches.append(word)
                # Checks if the word length is higher than the max length
                # Or if the counter is equal to the rows which mean the next iteration will cause an error
                if count + i == rows or len(word) == max_length:
                    break
    return matches


def check_input_args(args):
    """
    The func checks all the Parameters are valid and if not return a msg with the error
    :param args: paths for 4 files
    :return: String with the error message or None in case the was no errors
    """
    if not (len(args) == 4):
        return "Invalid amount of args"
    [word_file, matrix_file, output_file, directions] = args
    msg = ""
    isfile = os.path.isfile
    # Check if word_wile exist
    if not isfile(word_file):
        msg = "The word file not exist"
    # Check if the matrix_file exist
    elif not isfile(matrix_file):
        msg = "The matrix file not exist"
    # Check if directions has valid input
    else:
        for char in directions:
            if char not in "udrlwxyz":
                msg = "The directions were invalid"
                break
    return msg if msg else None


def read_wordlist(filename):
    """
    The func convert the given file into a list of words
    :param filename: a path for a file in the current directory
    :return: list with words in it
    """
    with open(filename, "r") as words_file:
        text = words_file.read()
    words = text.split("\n")
    # Returning the list without the last item because its an empty string
    return words[:-1]


def read_matrix(filename):
    """
    The func convert the given file into a matrix (list with lists in it)
    :param filename: a path for a file in the current directory
    :return: list with lists in it
    """
    with open(filename, "r") as matrix_file:
        text = matrix_file.read()
    matrix_draft = text.split("\n")
    matrix = [row.split(",") for row in matrix_draft]
    # Returning the matrix without the last item because its an empty list
    return matrix[:-1]


def find_words(word_list, matrix, directions):
    """
    The func finds the words from the word list that appears in the matrix by the given direction
    :param word_list: list of whole the words to look for
    :param matrix: where the func looks for words in
    :param directions: The direction the func need to look by
    :return: a list with tuples init which state all the words that was found and how many times
    """
    if not matrix:
        return []
    # Convert the string into a set in order to remove duplicates and then join in back into a one string
    direction = "".join(set(directions))
    # Empty list to store all the matches
    matches = []
    num_of_columns = len(matrix[0])
    num_of_rows = len(matrix)
    max_word_length = 0
    # Get the longest word in the words list
    for word in word_list:
        if len(word) > max_word_length:
            max_word_length = len(word)
    # Looking for all the words in each direction
    for d in direction:
        f = {
            "u": find_words_in_ud_direction,
            "d": find_words_in_ud_direction,
            "r": find_words_in_rl_direction,
            "l": find_words_in_rl_direction,
            "w": find_words_in_yxzy_direction,
            "x": find_words_in_yxzy_direction,
            "y": find_words_in_yxzy_direction,
            "z": find_words_in_yxzy_direction,
        }
        results = f[d](
            word_list, matrix, max_word_length, num_of_rows, num_of_columns, d
        )
        matches += results
    # From results list in to a list with tuples in the format: [(word, count), (word, count)]
    list_of_tuples = word_counter(matches, word_list)
    return list_of_tuples


def write_output(results, filename):
    """
    Convert a list tuples into a txt file.
    :param results: List of tuples
    :param filename: a path for a file in the current directory
    """
    with open(filename, "w") as output_file:
        if results:
            for word, count in results:
                output_file.write(f"{word},{count}\n")
        else:
            output_file.write("")


def main(words_file, matrix_file, output_file, directions):
    words_list = read_wordlist(words_file)
    matrix = read_matrix(matrix_file)
    matches = find_words(words_list, matrix, directions)
    write_output(matches, output_file)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        WORD_FILE, MATRIX_FILE, OUTPUT_FILE, DIRECTIONS = sys.argv[1:5]
        msg = check_input_args([WORD_FILE, MATRIX_FILE, OUTPUT_FILE, DIRECTIONS])
        if not msg:
            main(WORD_FILE, MATRIX_FILE, OUTPUT_FILE, DIRECTIONS)
        else:
            print(msg)
    else:
        print("Too many parameters were given. Please provide only 4 Parameters")
