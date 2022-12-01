# The tagger.py starter code for CSC384 A4.
# Currently readu in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy

def list_to_tuple(train_list):
    train_dict = []
    for i in train_list:
        if i[0] != ":":
            my_list = i.split(':')
            train_dict.append([my_list[0], my_list[1]])
        else:
            train_dict.append([':', 'PUN'])
    return train_dict

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
    
    pos_with_begin = {'begin': 0}
    pos_without_begin = {}
    for i in training_list:
        with open(i, "r") as file:
            for l in file.readlines():
                if l.split()[2] in pos_without_begin:
                    pos_without_begin[l.split()[2]] = pos_without_begin[l.split()[2]] + 1
                else:
                    pos_without_begin[l.split()[2]] = 1

                if l.split()[2] not in pos_with_begin:
                    pos_with_begin[l.split()[2]] = 1
                elif l.split()[0] == '.' or l.split()[0] == '!' or l.split()[0] == '?' or l.split()[0] == '"':
                    pos_with_begin['begin'] = pos_with_begin['begin'] + 1
                else:
                    pos_with_begin[l.split()[2]] = pos_with_begin[l.split()[2]] + 1

    return tuple_of_training_lines, pos_with_begin, pos_without_begin

def test_preprocessing(test_lines):
    # Process the input test file
    with open(test_file, 'r') as f:
        list_of_test_lines = f.readlines()

    list_of_test_lines = [x.rstrip() for x in list_of_test_lines]

    return list_of_test_lines

def build_transition_matrix(tuple_of_training_lines, pos_with_begin):
    transitionMatrix = {'begin': {}}
    i = 0
    while i != len(tuple_of_training_lines):
        num_pos_with_begin = 1/pos_with_begin['begin']
        num_pos_with_begin2 = 1/pos_with_begin[tuple_of_training_lines[i-1][1]]
        if i == 0:
            if tuple_of_training_lines[i][1] in transitionMatrix["begin"]:
                transitionMatrix['begin'][tuple_of_training_lines[i][1]] = num_pos_with_begin + transitionMatrix['begin'][tuple_of_training_lines[i][1]]
            else:
                transitionMatrix['begin'][tuple_of_training_lines[i][1]] = num_pos_with_begin
        elif tuple_of_training_lines[i-1][0] == '"' or tuple_of_training_lines[i-1][0] == '?' or tuple_of_training_lines[i-1][0] == '.' or tuple_of_training_lines[i-1][0] == '!':
            if tuple_of_training_lines[i][1] in transitionMatrix['begin']:
                transitionMatrix['begin'][tuple_of_training_lines[i][1]] = num_pos_with_begin + transitionMatrix['begin'][tuple_of_training_lines[i][1]]
            else:
                transitionMatrix['begin'][tuple_of_training_lines[i][1]] = num_pos_with_begin
        else:
            if tuple_of_training_lines[i-1][1] not in transitionMatrix:
                transitionMatrix[tuple_of_training_lines[i-1][1]] = {}
            if tuple_of_training_lines[i][1] not in transitionMatrix[tuple_of_training_lines[i-1][1]]:
                transitionMatrix[tuple_of_training_lines[i-1][1]][tuple_of_training_lines[i][1]] = num_pos_with_begin2
            else:
                transitionMatrix[tuple_of_training_lines[i-1][1]][tuple_of_training_lines[i][1]] = num_pos_with_begin2 + transitionMatrix[tuple_of_training_lines[i-1][1]][tuple_of_training_lines[i][1]]
        i = i+1

    return transitionMatrix

def build_emission_matrix(tuple_of_training_lines, pos_without_begin):
    emissionMatrix = {}
    i = 0
    while i != len(tuple_of_training_lines):
        num_pos_without_begin = 1/pos_without_begin[tuple_of_training_lines[i][1]]
        if tuple_of_training_lines[i][1] not in emissionMatrix:
            emissionMatrix[tuple_of_training_lines[i][1]] = {}
        if tuple_of_training_lines[i][0] in emissionMatrix[tuple_of_training_lines[i][1]]:
            emissionMatrix[tuple_of_training_lines[i][1]][tuple_of_training_lines[i][0]] = num_pos_without_begin + emissionMatrix[tuple_of_training_lines[i][1]][tuple_of_training_lines[i][0]]
        else:
            emissionMatrix[tuple_of_training_lines[i][1]][tuple_of_training_lines[i][0]] = num_pos_without_begin
        i = i+1
    
    return emissionMatrix

def matrix_manipulate(matrix):
    return dict((i,dict((j,numpy.log(k)) for j,k in l.items())) for i,l in matrix.items())

def viterbi_probabilities(transitionMatrix, emissionMatrix, test_file_words, pos_without_begin):
    final_ans = ""
    viterbi = {}
    num_test_file_words = len(test_file_words)
    t = 0
    while t != num_test_file_words:
        updated_viterbi = {}
        if t == 0:
            for u in pos_without_begin:
                if test_file_words[t] not in emissionMatrix[u]:
                    emission = -100
                else:
                    emission = emissionMatrix[u][test_file_words[t]]
                if u not in transitionMatrix['begin']:
                    transition = -100
                else:
                    transition = transitionMatrix['begin'][u] 
                updated_viterbi[u] = emission + transition
        elif test_file_words[t-1][0] == '"' or test_file_words[t-1][0] == '!' or test_file_words[t-1][0] == '?' or test_file_words[t-1][0] == '.':
            for u in pos_without_begin:
                if test_file_words[t] not in emissionMatrix[u]:
                    emission = -100
                else:
                    emission = emissionMatrix[u][test_file_words[t]]
                if u not in transitionMatrix['begin']:
                    transition = -100
                else:
                    transition = transitionMatrix['begin'][u]
                updated_viterbi[u] = emission + transition

            if test_file_words[t-1][0] == '"':
                final_ans += (test_file_words[t-1] + ' : ' + 'PUQ' + '\n')
            else:
                final_ans += (test_file_words[t-1] + ' : ' + 'PUN' + '\n')

        else:
            prev = {}
            for u in pos_without_begin:
                updated_viterbi[u] = -10000000000
                for x in viterbi:
                    if x in transitionMatrix:
                        if test_file_words[t] not in emissionMatrix[u]:
                            emission = -100
                        else:
                            emission = emissionMatrix[u][test_file_words[t]]
                        if u not in transitionMatrix[x]:
                            transition = -100
                        else:
                            transition = transitionMatrix[x][u]
                        updated_sum = emission + transition + viterbi[x]
                        if updated_sum > updated_viterbi[u]:
                            prev[u] = x
                            updated_viterbi[u] = updated_sum
                        
            final_ans = (test_file_words[t-1] + ' : ' + prev[max(updated_viterbi, key=lambda key: updated_viterbi[key])] + '\n') + final_ans

        if t == len(test_file_words) - 1:
            final_ans = (test_file_words[t] + ' : ' + max(updated_viterbi, key=lambda key: updated_viterbi[key]) + '\n') + final_ans
        
        viterbi = updated_viterbi

        t+=1

    return final_ans


def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #

    tuple_of_training_lines, pos_with_begin, pos_without_begin = train_preprocessing(training_list)
    test_file_words = test_preprocessing(test_file)

    emissionMatrix = build_emission_matrix(tuple_of_training_lines, pos_without_begin)
    transitionMatrix = build_transition_matrix(tuple_of_training_lines, pos_with_begin)

    emissionMatrix, transitionMatrix = matrix_manipulate(emissionMatrix), matrix_manipulate(transitionMatrix)

    solution = viterbi_probabilities(transitionMatrix, emissionMatrix, test_file_words, pos_without_begin)

    # Output the file
    output = open(output_file, "w")
    output.write(solution)
    

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