# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

def list_to_tuple(train_list):
    train_dict = []
    for i in train_list:
        if i[0] != ":":
            my_list = i.split(':')
            train_dict.append([my_list[0], my_list[1]])
        else:
            train_dict.append([':', 'PUN'])
    return train_dict

def build_initial_probabilities(pos, unique_pos, words):
    initial_table = np.full(len(unique_pos), 0.0001, dtype='float')
    for i in range(len(words)-1):
        if pos[i] == 'PUN': #end of sentence
            initial_table[unique_pos[pos[i+1]]] += 1
    return initial_table/sum(initial_table)

def build_transition_probabilities(pos, unique_pos):
    #creating t x t transition matrix of tags
    transition_matrix = np.full((len(unique_pos), len(unique_pos)), 0.001, dtype='float')
    for i in range(len(pos)-1):
        transition_matrix[unique_pos[pos[i]], unique_pos[pos[i+1]]] += 1
    row_sum = transition_matrix.sum(axis=1)
    norm_transition_matrix = transition_matrix/row_sum[:,np.newaxis]

    return norm_transition_matrix

def build_emission_probabilities(pos, unique_pos, words, unique_words):
    emission_matrix = np.full((len(unique_pos), len(unique_words)), 0.0001, dtype='float')
    for word in range(len(words)):
        emission_matrix[unique_pos[pos[word]], unique_words[words[word]]] += 1

    row_sum = emission_matrix.sum(axis=1)
    norm_emission_matrix = emission_matrix/row_sum[:,np.newaxis]
    return norm_emission_matrix

def train_preprocessing(training_list):
    list_of_training_lines = []
    tmp = []

    # Process the input training files
    for i in training_list:
        tmp += list_of_training_lines
        with open(i, 'r') as f:
            list_of_training_lines = f.readlines()

    list_of_training_lines += tmp
    list_of_training_lines = [x.rstrip() for x in list_of_training_lines]
    list_of_training_lines = [x.replace(' ', '') for x in list_of_training_lines]
    tuple_of_training_lines = list_to_tuple(list_of_training_lines)

    words = [x[0] for x in tuple_of_training_lines]
    pos = [x[1] for x in tuple_of_training_lines]
    
    unique_words = {}
    for i, word in enumerate(set(words)):
        unique_words[word] = i
    unique_pos = {}
    for i, tag in enumerate(set(pos)):
        unique_pos[tag] = i

    return words, pos, unique_words, unique_pos

def test_preprocessing(test_lines):
    # Process the input test file
    with open(test_file, 'r') as f:
        list_of_test_lines = f.readlines()

    list_of_test_lines = [x.rstrip() for x in list_of_test_lines]

    return list_of_test_lines

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    # Find the unique number of words and parts of speech from training files

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]

    words, pos, unique_words, unique_pos = train_preprocessing(training_list)
    test_words = test_preprocessing(test_file)

    print(build_initial_probabilities(pos, unique_pos, words))
    print(build_emission_probabilities(pos, unique_pos, words, unique_words))
    print(build_transition_probabilities(pos, unique_pos))

    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Output file: " + output_file)

    # Start the training and tagging operation.
    #tag(training_list, test_file, output_file)

    # Output the file
    output = open(output_file, "w")
    for i in test_words:
        output.write(i)
        output.write('\n')