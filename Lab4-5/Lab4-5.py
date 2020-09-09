"""
Lab 4-5; Assignment 2
Program: This program have three parts
Part 1: Implement and test both the BFI_Subset_Sum and HS_Subset_Sum algorithms.
Part 2: Conduct experiments to explore the relative efficiency of the two algorithms.
Part 3: Observations support the theoretical predictions that BFS_Subset_Sum is in O(2^n)
and HS_Subset_Sum is in O(n*2^(n/2)).

From my BFI_Subset_Sum and HS_Subset_Sum, both algorithms from Dr. Robin Dawes assignment 2
instructions, there have pseudo codes about both algorithms, and I follow the pseudo codes
processes to finish both algorithms(my codes).
"""

import math
import random


"-----------------------------Part 1-------------------------------------"
class Set:  # creat class for make a set
    def __init__(self, elements, sums):
        self.elements = elements
        self.sums = sum(elements)


# BFI algorithm follow the pseudo codes process finish it
def BFI_Subset_Sum(S, k):
    empty_set = Set([], 0)
    subsets = [empty_set]
    for i in range(len(S)):
        new_subsets = []
        for old_u in subsets:
            new_u = Set([*old_u.elements], old_u.sums)
            new_u.elements.append(S[i])
            new_u.sums += S[i]
            if new_u.sums == k:
                return new_u.elements  # find target return elements
            else:
                new_subsets.append(old_u), new_subsets.append(new_u)
        subsets = new_subsets
    return "no subset sums to the target value"  # not find


# BFI algorithm modify, only return subsets
def BFI_Subset_Sum_Modify(S):
    empty_set = Set([], 0)
    subsets = [empty_set]
    for i in range(len(S)):
        new_subsets = []
        for old_u in subsets:
            new_u = Set([*old_u.elements], old_u.sums)
            new_u.elements.append(S[i])
            new_u.sums += S[i]
            new_subsets.append(old_u), new_subsets.append(new_u)
        subsets = new_subsets
    return subsets


# Pair_Sum function, the function from Dr. Robin assignment 2 instructions
def Pair_Sum(Values_1, Values_2, k):
    p1 = 0
    p2 = len(Values_2) - 1
    while (p1 < len(Values_1)) and (p2 > 0):
        t = Values_1[p1].sums + Values_2[p2].sums
        if t == k:
            return Values_1[p1].elements + Values_2[p2].elements
        elif t < k:
            p1 = p1 + 1
        else:
            p2 = p2 - 1
    return -1, -1


# HS algorithm follow the pseudo codes process finish it
def HS_Subset_Sum(S, k):
    half = len(S) // 2
    S_Left = BFI_Subset_Sum_Modify(S[:half])
    S_Right = BFI_Subset_Sum_Modify(S[half:])
    for i in S_Left:
        if i.sums == k:
            return i.elements
    for i in S_Right:
        if i.sums == k:
            return i.elements

    S_Left = sorted(S_Left, key=lambda x: x.sums)  # use built-in method to sort the set
    S_Right = sorted(S_Right, key=lambda x: x.sums)  # use built-in method to sort the set
    new_susbet = Pair_Sum(S_Left, S_Right, k)

    if new_susbet != (-1, -1):
        return new_susbet
    else:
        return "no subset sums to the target value"
"---------------------------End Part 1-----------------------------------"




"-----------------------------Part 2-------------------------------------"
"""
My part 2 codes all from my part 1, the only change is I'm not return the results
(the target elements) I change to return the operations(counts)
"""

def BFI_Subset_Sum_Count(S, k):
    count = 0
    empty_set = Set([], 0)
    subsets = [empty_set]
    count += 2
    for i in range(len(S)):
        new_subsets = []
        count += 1
        for old_u in subsets:
            new_u = Set([*old_u.elements], old_u.sums)
            new_u.elements.append(S[i])
            new_u.sums += S[i]
            count += 3
            if new_u.sums == k:
                count += 1
                return count
            else:
                new_subsets.append(old_u), new_subsets.append(new_u)
                count += 2
        subsets = new_subsets
        count += 1
    return count


def HS_Subset_Sum_Count(S, k):
    count = 0
    half = len(S) // 2
    count += 1
    S_Left, left_count = BFI_Subset_Sum_Modify_Count(S[:half])  # left half operations from modify BFI
    S_Right, light_count = BFI_Subset_Sum_Modify_Count(S[half:])  # right half operations from modify BFI
    count += left_count
    count += light_count
    for i in S_Left:
        if i.sums == k:
            count += 1
            return count
    for i in S_Right:
        if i.sums == k:
            count += 1
            return count
    S_Left = sorted(S_Left, key=lambda x: x.sums)
    count += 3 * len(S_Left) * math.log2(len(S_Left))  # follow the instruction 3*t*(log t) operations
    S_Right = sorted(S_Right, key=lambda x: x.sums)
    count += 3 * len(S_Right) * math.log2(len(S_Right))  # follow the instruction 3*t*(log t) operations

    new_susbet_count = Pair_Sum_Count(S_Left, S_Right, k)  # get back pair sum function total operations
    count += new_susbet_count
    return count


# BFI modify count to help HS operations
def BFI_Subset_Sum_Modify_Count(S):
    count = 0
    empty_set = Set([], 0)
    subsets = [empty_set]
    count += 2
    for i in range(len(S)):
        new_subsets = []
        count += 1
        for old_u in subsets:
            new_u = Set([*old_u.elements], old_u.sums)
            new_u.elements.append(S[i])
            new_u.sums += S[i]
            new_subsets.append(old_u), new_subsets.append(new_u)
            count += 5
        subsets = new_subsets
        count += 1
    return subsets, count


# Pair sum to help HS operations
def Pair_Sum_Count(Values_1, Values_2, k):
    count = 0
    p1 = 0
    p2 = len(Values_2) - 1
    while (p1 < len(Values_1)) and (p2 > 0):
        t = Values_1[p1].sums + Values_2[p2].sums
        count += 1
        if t == k:
            count += 1
            return count
        elif t < k:
            p1 = p1 + 1
            count += 1
        else:
            p2 = p2 - 1
            count += 1
    return count


"""My part 2 experiments results, some test codes from assignment 2 instructions"""
def test_experiment():
    average_B = []
    average_H = []
    B_Count = 0
    H_Count = 0
    for n in range(4, 16):
        for i in range(0, 20):
            newset = [random.randint(1, 100) for i in range(n)]
            target = [random.randint(1, 100) for i in range(10)]
            for k in target:
                B_Count += BFI_Subset_Sum_Count(newset, k)
                H_Count += HS_Subset_Sum_Count(newset, k)
            average_B_Count = B_Count / 10
            average_H_Count = H_Count / 10
        average_B_Count_1 = average_B_Count / 20
        average_H_Count_2 = average_H_Count / 20
        average_B.append(round(average_B_Count_1, 3))
        average_H.append(round(average_H_Count_2, 3))
    print("Set size of N from 4 to 15:")
    print("BFI_Subset_Sum:", average_B)
    print("HS_Subset_Sum:", average_H)
    print()


    # Below parts for my experiments plotted on a chart, please install matplot library
    try:
        print("My plotted on a chart:")
        import matplotlib.pyplot as plt
        x = [i for i in range(4, 16)]
        plt.plot(x, average_B, linewidth=2, label="BFI_Subset_Sum")
        plt.plot(x, average_H, linewidth=2, label="HS_Subset_Sum")
        plt.title("BFI_Subset_Sum/HS_Subset_Sum Experiment", fontsize=15)
        plt.xlabel("Set size of N", fontsize=12)
        plt.ylabel("Average number of Operations", fontsize=12)
        plt.tick_params(axis='both', labelsize=9)
        plt.legend()
        plt.show()
    except ModuleNotFoundError:  # matplot module do not install
        print("Sorry, my plotted on a chart cannot show it because you do not install matplot library!")
"---------------------------End Part 2-----------------------------------"




"-----------------------------Part 3-------------------------------------"
""" 
My conclusion is I support the theoretical predictions that BFS_Subset_Sum is in 
O(2^n) and HS_Subset_Sum is in O(n*2^(n/2)). 
From my second part experiments(see my plotted on a chart), when the set size is increasing, 
the average of operations also is increasing. Compare both of BFS_Subset_Sum and HS_Subset_Sum growing speed, 
BFS_Subset_Sum is growing much faster than HS_Subset_Sum.

In addition, compare the increase speed between (complexity) 2^n and n*2^(n/2), 
that's obvious 2^n grow faster than n*2^(n/2).

So we can conclude that BFS_Subset_Sum is in O(2^n) and HS_Subset_Sum is in 
O(n*2^(n/2))
"""
"---------------------------End Part 3-----------------------------------"




"""
This is my main function, use to test my Part 1 and Part 2
"""
if __name__ == '__main__':
    print("Test for Part 1:")
    S = [3, 5, 3, 9, 18, 4, 5, 6]
    k, k1, k2 = 28, 53, 88
    print("Set S = {" + str(S)[1:-1] + "}")
    print("\nWhen k is 28:")
    print("BFI_Subset_Sum:", "{" + str(BFI_Subset_Sum(S, k))[1:-1] + "}")
    print("HS_Subset_Sum:", "{" + str(HS_Subset_Sum(S, k))[1:-1] + "}")

    print("\nWhen k is 53(sum of the entire set):")
    print("BFI_Subset_Sum:", "{" + str(BFI_Subset_Sum(S, k1))[1:-1] + "}")
    print("HS_Subset_Sum:", "{" + str(HS_Subset_Sum(S, k1))[1:-1] + "}")

    print("\nWhen k is 88:")
    print("BFI_Subset_Sum:", (BFI_Subset_Sum(S, k2)))
    print("HS_Subset_Sum:", (HS_Subset_Sum(S, k2)))

    print("\n")
    print("Test for Part 2:")
    test_experiment()
