import os
import timeit
import pprint

if __name__ == '__main__':

    # TODO: PASTE IN YOUR FILEPATHS
    training_list = ["data/training1.txt", "data/training2.txt", "data/training3.txt", "data/training4.txt", "data/training5.txt"]
    test_files = ["data/test1.txt", "data/test2.txt", "data/test3.txt", "data/test4.txt", "data/test5.txt"]
    solution_files = training_list
    # NOTE: Solution files are the same as training files since the respective test files are the same as the training files

    # make every combination of training files
    training_files_combos = []
    for i in range(1, len(training_list)+1):
        training_files_combos.append([training_list[i-1]])
        for j in range(i+1, len(training_list)+1):
            training_files_combos.append([training_list[i-1], training_list[j-1]])
            for k in range(j+1, len(training_list)+1):
                training_files_combos.append([training_list[i-1], training_list[j-1], training_list[k-1]])
                for l in range(k+1, len(training_list)+1):
                    training_files_combos.append([training_list[i-1], training_list[j-1], training_list[k-1], training_list[l-1]])

    accuracy_dict = {}

    # run the tagger on each combination of training files and test files
    for training_files in training_files_combos:
      for i in range(len(test_files)):
        if f"data/training{test_files[i][-5]}.txt" in training_files:
            continue # don't overfit, skip
        
        # make the string for the tagger
        training_files_string = ""
        for training_file in training_files:
            training_files_string += training_file + " "
        training_files_string = training_files_string.strip()

        print(f"\n\nTraining on {training_files_string}, testing on {test_files[i]}")

        # run the tagger and time it.
        start_time = timeit.default_timer()
        os.system(f"python tagger.py -d {training_files_string} -t {test_files[i]} -o output1.txt")
        end_time = timeit.default_timer()

        # Compare the contents of the HMM tagger output with the reference solution.
        # Store the missed cases and overall stats in results.txt
        with open("output1.txt", "r") as output_file, \
            open(str(solution_files[i]), "r") as solution_file:
            output = output_file.readlines()
            solution = solution_file.readlines()
            total_matches = 0

            # Count the number of matches.
            for index in range(len(output)):
                if output[index] == solution[index]:
                    total_matches = total_matches + 1

            # Calculate the accuracy.
            print (f"Total time: {end_time - start_time} seconds")
            if len(output)>0:
              print (f"Accuracy: %{100 * total_matches / len(output)}")
              accuracy_dict[f"Training Files: {training_files_string} -- Test File {test_files[i]} -- Time Taken {end_time - start_time}"] = 100 * total_matches / len(output)

    pprint.pprint(accuracy_dict)