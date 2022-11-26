# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np

def list_to_dict(train_list):
    train_dict = dict()
    for i in train_list:
        if i[0] != ":":
            my_list = i.split(':')
            train_dict[my_list[0]] = my_list[1]
        else:
            train_dict[":"] = "PUN"
    return train_dict

def list_to_tuple(train_list):
    train_dict = []
    for i in train_list:
        if i[0] != ":":
            my_list = i.split(':')
            train_dict.append([my_list[0], my_list[1]])
        else:
            train_dict.append([':', 'PUN'])
    return train_dict

# Emission Probability
def word_given_tag(word, tag, train_list):
    tag_list = [pair for pair in train_list if pair[1]==tag]
    count_tag = len(tag_list)
    w_given_tag_list = [pair[0] for pair in tag_list if pair[0]==word]
    count_w_given_tag = len(w_given_tag_list)
    
    return (count_w_given_tag, count_tag)

# Transition Probability
def t2_given_t1(t2, t1, train_list):
    tags = [pair[1] for pair in train_list]
    count_t1 = len([t for t in tags if t==t1])
    count_t2_t1 = 0
    for index in range(len(tags)-1):
        if tags[index]==t1 and tags[index+1] == t2:
            count_t2_t1 += 1
    return (count_t2_t1, count_t1)

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    # Find the unique number of words and parts of speech from training files
    words = [x[0] for x in training_list]
    unique_words = set(words)
    pos = [x[1] for x in training_list]
    unique_pos = set(pos)
    num_unique_pos = len(unique_pos)
    num_unique_words = len(unique_words)

    # Emission probabilities
    # Calculate probability of a word given tag
    w_given_t = np.zeros((num_unique_pos, num_unique_words))
    
    # Transition  probabilities
    tags_matrix = np.zeros((num_unique_pos, num_unique_pos))

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]

    list_of_training_lines = []
    tmp = []

    # Process the input training files
    for i in training_list:
        tmp += list_of_training_lines
        with open(i, 'r') as f:
            list_of_training_lines = f.readlines()

    list_of_training_lines += tmp
    list_of_training_lines = [x.rstrip() for x in list_of_training_lines]

    # Process the input test file
    with open(test_file, 'r') as f:
        list_of_test_lines = f.readlines()

    list_of_test_lines = [x.rstrip() for x in list_of_test_lines]
    list_of_training_lines = [x.replace(' ', '') for x in list_of_training_lines]
    tuple_of_training_lines = list_to_tuple(list_of_training_lines)
    #list_of_training_lines = list_to_dict(list_of_training_lines)

    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag (tuple_of_training_lines, test_file, output_file)

    # Output the file
    output = open(output_file, "w")
    for i in list_of_test_lines:
        output.write(i)
        output.write('\n')