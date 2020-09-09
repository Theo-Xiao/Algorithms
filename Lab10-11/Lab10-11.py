"""
Name: Jinghong Xiao
Student number: 20035787
Lab 10-11; Assignment 4
Program: Dynamic Programming LCS algorithm (Settling Our Differences)
This program use to Dynamic Programming find longest common subsequence and
use the result to trace back and find the difference between the file's each line
"""
import sys


# Function use read file then return file data
def readfile(filename):
    try:
        file = open(filename, "r", encoding="utf-8")
        return file.readlines()
    except OSError as error:
        print(error), sys.exit()
    except ValueError as error:
        print(error), sys.exit()


# Function from Lab 9 Experiment 1 method
def f1(s):
    sums = 0
    for c in s:
        sums += ord(c)
    return sums
    # return integer result based on ASii number


# Function from Lab 9 Experiment 3 method
def f2mod(s):
    results = 0
    for c in s:
        results = (7 * results + ord(c)) % 100000
    return results
    # return integer result based on (ASii number and mod it)


# Function from Lab 9 Experiment 4 method
def check(s1, s2):
    if f1(s1) != f1(s2) or f2mod(s1) != f2mod(s2):
        return False
    else:
        if s1 == s2: # check two strings are actually same
            return True
        return False


# Function use to get longest common subsequence
def Longest_Common_Subsequence(file1, file2, file1_length, file2_length):
    match_list, length_1, length_2 = [], file1_length, file2_length
    matrix = [[0 for i in range(file2_length + 1)] for i in range(file1_length + 1)]
    for length_1 in range(file1_length + 1):
        for length_2 in range(file2_length + 1):
            if length_1 == 0 or length_2 == 0:
                matrix[length_1][length_2] = 0
            elif check(file1[length_1 - 1], file2[length_2 - 1]):
                # compare the string use to make them become integer and then to compare them
                # if check function return True which two lines are equal
                matrix[length_1][length_2] = matrix[length_1 - 1][length_2 - 1] + 1
            else:
                matrix[length_1][length_2] = max(matrix[length_1 - 1][length_2], matrix[length_1][length_2 - 1])

    while length_1 > 0 and length_2 > 0:
        if check(file1[length_1 - 1], file2[length_2 - 1]):
            # compare the string use to make them become integer to compare them
            # if check function return True which two lines are equal
            match_list.append((0, length_1, length_2))
            # if is equal append the (0, file1 index, file2 index) to the result
            length_1 -= 1
            length_2 -= 1
        elif matrix[length_1 - 1][length_2] > matrix[length_1][length_2 - 1]:
            match_list.append((1, length_1, length_2))
            # if is not equal append the (1, file1 index, file2 index) to the result
            length_1 -= 1
        else:
            match_list.append((1, length_1, length_2))
            length_2 -= 1
            # if is not equal append the (1, file1 index, file2 index) to the result
    match_list.reverse()  # reverse the results since is based on trace back
    return match_list


# Function use to simplify the results and show the results
def result(match_info, file1, file2):
    list1, list2, final_list = [], [], []
    for i in match_info:
        if i[0] == 0:
            if list2:
                final_list.append(["mis", list2[0][0], list2[-1][0], list2[0][1], list2[-1][1]])
                # simplify the result based on the lines, from the mismatch to match
                list2 = []
            list1.append((i[1], i[2]))
        else:
            if list1:
                final_list.append(["mat", list1[0][0], list1[-1][0], list1[0][1], list1[-1][1]])
                # simplify the result based on the lines, from the match to mismatch
                list1 = []
            list2.append((i[1], i[2]))

    # after the loop they may have some lines reaming, and still based on the mismatch to match or match to mismatch
    if list1:
        final_list.append(["mat", list1[0][0], list1[-1][0], list1[0][1], list1[-1][1]])
    if list2:
        final_list.append(["mis", list2[0][0], list2[-1][0], list2[0][1], list2[-1][1]])

    # Below loop use to remove duplicate lines, and determine the None is in the line or not
    for i in range(len(final_list)):
        try:
            if final_list[i][1] == final_list[i - 1][2]:
                final_list[i][1] = final_list[i][1] + 1
            if final_list[i][1] == final_list[i - 1][2]:
                final_list[i][1] = final_list[i][2] + 1
            if final_list[i][3] == final_list[i - 1][4]:
                final_list[i][3] = final_list[i][3] + 1
            if final_list[i][1] > final_list[i][2]:
                final_list[i][2] = None
            if final_list[i][3] > final_list[i][4]:
                final_list[i][4] = None
        except IndexError:
            pass

    # Below loop use to show the results
    for i in final_list:
        if i[0] == "mis" and i[2] is None:
            print("Mismatch:  " + file1 + ":   " + str(i[2]) + "\t\t" + file2 + ": <" + str(i[3]) +
                  " .. " + str(i[4]) + ">\n")
        elif i[0] == "mis" and i[4] is None:
            print("Mismatch:  " + file1 + ": <" + str(i[1]) + " .. " + str(i[2]) + ">\t" + file2 +
                  ":   " + str(i[4]) + "\n")
        elif i[0] == "mis":
            print("Mismatch:  " + file1 + ": <" + str(i[1]) + " .. " + str(i[2]) + ">\t" + file2 + ": <" + str(i[3]) +
                  " .. " + str(i[4]) + ">\n")
        elif i[0] == "mat":
            print("Match:\t   " + file1 + ": <" + str(i[1]) + " .. " + str(i[2]) + ">\t" + file2 + ": <" + str(i[3]) +
                  " .. " + str(i[4]) + ">\n")


# This is my main function, use to set the menu to the user to find the difference between the different files
def main():
    file_1, file_2 = readfile("Data_Files/" + "Dijkstra.py"), readfile("Data_Files/" + "Dijkstra_py3.py")
    file_3, file_4 = readfile("Data_Files/" + "Three_Bears.v1.txt"), readfile("Data_Files/" + "Three_Bears.v2.txt")
    while True:
        print('Welcome to use "diff" system!\n')
        print("1: Dijkstra.py | Dijkstra_py3.py")
        print("2: Three_Bears.v1.txt | Three_Bears.v2.txt")
        print("3: Exit the system\n")
        user_input = input("Which file difference do you want to report:")
        if user_input == "1":
            print("\n\nPatch:\n")
            match_matrix = Longest_Common_Subsequence(file_1, file_2, len(file_1), len(file_2))
            result(match_matrix, "Dijkstra.py", "Dijkstra_py3.py")
            print("\nFinish\t Dijkstra.py | Dijkstra_py3.py  report!\n\n")
        elif user_input == "2":
            print("\n\nPatch:\n")
            match_matrix = Longest_Common_Subsequence(file_3, file_4, len(file_3), len(file_4))
            result(match_matrix, "Three_Bears.v1.txt", "Three_Bears.v2.txt")
            print("\nFinish\t Three_Bears.v1.txt | Three_Bears.v2.txt  report!\n\n")
        elif user_input == "3":
            print('Thank you for used "diff" system!')
            break
        else:
            print("Please enter a valid operation!\n\n")


if __name__ == '__main__':
    main()


"""
Part 2 (An explanation and justification of the method you use to represent strings by integers):

For the method, I used to represent strings by integers is from lab 9 experiment 4. 
(Experiment 4 actually include two functions)
I assume each line have too many strings(some lines may not have too many), 
thus if I only use lab 9 experiment 1 method, they may occur overflow, so I include experiment 3 method, 
prevent that when a string represents integer actually overflows and if is happend then fix it 
(make sure it does not represent the wrong integer). 

It is really easy to determine two integers are not equal, when they are not equal, 
(the function represent each string by an integer) there is no way they can be equal
or same string. However, when they are equal, 
there is always a possibility that two different strings will be represented by the same integer, 
so when two integers are equal, we still need to check the string is actually the same or not
(to see if they really do match).
"""
