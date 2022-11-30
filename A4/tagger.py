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

def build_initial_probabilities(pos, distinctive_pos, words):
    num_total_words = len(words)
    initial_table = np.full(len(distinctive_pos), 0.00001)
    for i in range(num_total_words - 1):
        next_pos = pos[i + 1]
        if pos[i] == 'PUN': 
            next_pos_in_table = distinctive_pos[next_pos]
            initial_table[next_pos_in_table] = initial_table[next_pos_in_table] + 1
    initial_table_sum = sum(initial_table)
    initial_table_probabilities = initial_table/initial_table_sum
    return initial_table_probabilities

def build_transition_probabilities(pos, distinctive_pos):
    num_total_pos = len(pos)
    transition_table = np.full((len(distinctive_pos), len(distinctive_pos)), 0.00001)
    for i in range(num_total_pos - 1):
        curr_pos = pos[i]
        next_pos = pos[i + 1]
        current_pos_in_table = distinctive_pos[curr_pos]
        next_pos_in_table = distinctive_pos[next_pos]
        transition_table[current_pos_in_table, next_pos_in_table] = transition_table[current_pos_in_table, next_pos_in_table] + 1
    normalize = transition_table/(transition_table.sum(axis=1)[:,np.newaxis])
    return normalize

def build_emission_probabilities(pos, distinctive_pos, words, distinctive_words):
    num_total_words = len(words)
    emission_table = np.full((len(distinctive_pos), len(distinctive_words)), 0.00001)
    for word in range(num_total_words):
        curr_word = pos[word]
        curr_word_in_words = words[word]
        pos_given_word = distinctive_pos[curr_word]
        words_given_word = distinctive_words[curr_word_in_words]
        emission_table[pos_given_word, words_given_word] = emission_table[pos_given_word, words_given_word] + 1
    normalize = emission_table/(emission_table.sum(axis=1)[:,np.newaxis])
    return normalize

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
    
    distinctive_words = {}
    for i, word in enumerate(set(words)):
        distinctive_words[word] = i
    distinctive_pos = {}
    for i, pos_tag in enumerate(set(pos)):
        distinctive_pos[pos_tag] = i

    return words, pos, distinctive_words, distinctive_pos

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

    words, pos, distinctive_words, distinctive_pos = train_preprocessing(training_list)
    test_file_words = test_preprocessing(test_file)

    # Find the number of distinctive parts of speech and total number of test file words
    num_distinctive_pos = len(distinctive_pos)
    num_total_test_words = len(test_file_words)

    viterbi = np.zeros((num_distinctive_pos, num_total_test_words))

    configuration = {}
    for i in range(num_distinctive_pos):
        configuration[i] = np.array(i)

    # Find the initial table, emission matrix and transition matrix probabilities
    initial_table = build_initial_probabilities(pos, distinctive_pos, words)
    emission_table = build_emission_probabilities(pos, distinctive_pos, words, distinctive_words)
    transition_table = build_transition_probabilities(pos, distinctive_pos)

    commonly_appearing_word = np.argmax(initial_table)

    emission_table_most_common_word = emission_table[:, commonly_appearing_word]
    emission_table_first_test_word = emission_table[:, distinctive_words[test_file_words[0]]]
    emission_table_sum = sum(emission_table_most_common_word * initial_table)
    emission_table_sum_first_word = sum(initial_table*emission_table[:, distinctive_words[test_file_words[0]]])

    # Determine value for time step 0
    if test_file_words[0] not in distinctive_words:
        viterbi[:,0] = (emission_table_most_common_word * initial_table) / emission_table_sum
    else:
        viterbi[:,0] = (emission_table_first_test_word * initial_table) / emission_table_sum_first_word

    # Recursive step from time step 1 to the number of test words
    for t in range(1, num_total_test_words):
        updated_configuration = {}

        for i in range(num_distinctive_pos):

            all_viterbi_until_last_pos = viterbi[:, t - 1]
            transition_table_up_to_i = transition_table[:,i]
            test_word_in_train = distinctive_words[test_file_words[t]]
            emission_table_from_i_to_test_word = emission_table[i, test_word_in_train]
            emission_table_from_i_to_most_common_word = emission_table[i, commonly_appearing_word]

            if test_file_words[t] in distinctive_words:
                old_pos = np.argmax(emission_table_from_i_to_test_word * transition_table_up_to_i * all_viterbi_until_last_pos)
                viterbi[i, t] = emission_table_from_i_to_test_word * transition_table[old_pos, i] * viterbi[old_pos, t-1]
            else:
                old_pos = np.argmax(emission_table_from_i_to_most_common_word * transition_table_up_to_i * all_viterbi_until_last_pos)
                viterbi[i, t] = emission_table_from_i_to_most_common_word * transition_table[old_pos, i] * viterbi[old_pos, t-1]
            updated_configuration[i] = np.append(configuration[old_pos], i)

        viterbi_sum = sum(viterbi[:, t])
        viterbi[:, t] /= viterbi_sum
        configuration = updated_configuration


    backward_pos = {value:key for (key, value) in distinctive_pos.items()}
    solution = []
    for i in configuration[np.argmax(viterbi[:, -1])]:
        solution.append(backward_pos[i])

    # Output the file
    output = open(output_file, "w")
    for i in range(len(solution)):
        output.write(test_file_words[i] + " : " + solution[i])
        output.write('\n')

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]

    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag(training_list, test_file, output_file)