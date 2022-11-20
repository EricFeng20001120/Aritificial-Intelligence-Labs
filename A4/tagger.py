# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys

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

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

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
    print(len(list_of_training_lines))
    list_of_training_lines = list_to_tuple(list_of_training_lines)
    #list_of_training_lines = list_to_dict(list_of_training_lines)
    
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Output file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)

    # Output the file
    output = open(output_file, "w")
    for i in list_of_test_lines:
        output.write(i)
        output.write('\n')

    print(len(list_of_training_lines))