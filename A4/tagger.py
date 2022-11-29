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
    initial_table = np.full(len(unique_pos), 0.0001)
    for i in range(len(words)-1):
        if pos[i] == 'PUN': 
            initial_table[unique_pos[pos[i+1]]] += 1
    return initial_table/sum(initial_table)

def build_transition_probabilities(pos, unique_pos):
    transition_table = np.full((len(unique_pos), len(unique_pos)), 0.001)
    for i in range(len(pos)-1):
        transition_table[unique_pos[pos[i]], unique_pos[pos[i+1]]] += 1
    row_sum = transition_table.sum(axis=1)
    norm_transition_table = transition_table/row_sum[:,np.newaxis]

    return norm_transition_table

def build_emission_probabilities(pos, unique_pos, words, unique_words):
    emission_table = np.full((len(unique_pos), len(unique_words)), 0.0001)

    for word in range(len(words)):
        emission_table[unique_pos[pos[word]], unique_words[words[word]]] += 1

    row_sum = emission_table.sum(axis=1)
    norm_emission_table = emission_table/row_sum[:,np.newaxis]
    return norm_emission_table

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
    for i, pos_tag in enumerate(set(pos)):
        unique_pos[pos_tag] = i

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

    words, pos, unique_words, unique_pos = train_preprocessing(training_list)
    test_words = test_preprocessing(test_file)

    initial_table = build_initial_probabilities(pos, unique_pos, words)
    emission_table = build_emission_probabilities(pos, unique_pos, words, unique_words)
    transition_table = build_transition_probabilities(pos, unique_pos)

    commonly_appearing_word = np.argmax(initial_table)
    prob_trellis = np.zeros((len(unique_pos), len(test_words)))
    path = {}

    for i in range(len(unique_pos)):
        path[i] = np.array(i)

    if test_words[0] not in unique_words:
        prob_trellis[:,0] = initial_table*emission_table[:, commonly_appearing_word]/sum(initial_table*emission_table[:, commonly_appearing_word])
    else:
        prob_trellis[:,0] = initial_table*emission_table[:, unique_words[test_words[0]]]/sum(initial_table*emission_table[:, unique_words[test_words[0]]])

    #for x2 to xt find each state's most likely prior state x
    for o in range(1, len(test_words)):
        new_path = {}
        for s in range(len(unique_pos)):
            if test_words[o] in unique_words:
                prior_tag = np.argmax(prob_trellis[:,o-1]*transition_table[:,s]*emission_table[s, unique_words[test_words[o]]])
                prob_trellis[s, o] = prob_trellis[prior_tag, o-1]*transition_table[prior_tag, s]*emission_table[s, unique_words[test_words[o]]]
            else:
                prior_tag = np.argmax(prob_trellis[:,o-1]*transition_table[:,s]*emission_table[s, commonly_appearing_word])
                prob_trellis[s, o] = prob_trellis[prior_tag, o-1]*transition_table[prior_tag, s]*emission_table[s, commonly_appearing_word]
            new_path[s] = np.append(path[prior_tag], s)
        path = new_path
        #normalize columns
        prob_trellis[:, o] = prob_trellis[:, o]/sum(prob_trellis[:, o])

    solution  = []
    reversed_unique_tags = {value : key for (key, value) in unique_pos.items()}

    for stage in path[np.argmax(prob_trellis[:,-1])]:
        solution.append(reversed_unique_tags[stage])

    # Output the file
    output = open(output_file, "w")
    for i in range(len(solution)):
        output.write(test_words[i] + " : " + solution[i])
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