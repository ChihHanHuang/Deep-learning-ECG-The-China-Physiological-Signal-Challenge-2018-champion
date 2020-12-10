If the operating environment is python2.7, use score.py as the scoring script.
If the operating environment is python3.5 or python3.6, use score2018.py as the scoring script.

The challenge committee selected 300 recoding files randomly as validation data(including the corresponding REFERENCE.csv ), storing in the validation_set folder, the validation dataset is only to verify every challenger's code running successfully.

The challenger should write the inference code into script cpsc2018.py, and encapsulate the code into function def challenge2018(record_base_path). The result corresponding to each recording file is an integer in range 1-9.
Input:
record_base_path:		the path saving the dataset
The function cpsc2018() will eventually generate a csv file named answers.csv, saving the inference results of the validation dataset, the storage format is as follows:
Recoding    Result
B0001       1
.           .
.           .
.           .
the first column is recording name and the second column is prediction label

Take recognizing the data under path ./validation_set as an example:
cpsc2018(record_base_path='./validation_set/')
the challenge team should run the script cpsc2018.py before running score.py to generate answers.csv file, and verify whether the encapsulation of the function is correct at the same time.
If under Linux/Unix environment, run command: $python cpsc2018.py -p ./validation_set/
If under Windows environment, run command: >python cpsc2018.py -p .\\validation_set\\
If the function generates the file answers.csv successfully, the recording and file format are in compliance with the requirements, the encapsulation is correct.

The frame of cpsc2018.py is provided, challengers can write the inference part of their algorithms in to INFERENCE PART of function challenge2018().
After generating the file answers.csv, each team can run the script score.py(or score_py3.py for python3) to verify their algorithm:
If under Linux/Unix environment, run command: $python score.py -r ./validation_set/REFERENCE.csv
If under Windows environment, run command: >python score.py -r .\\validation_set\\REFERENCE.csv
The file score.txt storing the final scores should be produced in the local path.

It is hoped that each team can optimize the time complexity of their algorithm while running code under validation dataset, and submit the algorithm run time on classifying 300 recording files of the validation dataset as a txt file named time_validation.txt based on the local platform. We will predict the execution time of the algorithm on the test dataset based on the submission and schedule the follow-up evaluation cycle:
If the algorithm runtime on the test dataset is less than 30 mins, we will give scoring feedback in 3 days;
If the algorithm runtime is between 30 and 120 mins, we will give scoring feedback in 1 week;
If the algorithm runtime is over 120 mins, we will not guarantee the feedback in time, please understand!
