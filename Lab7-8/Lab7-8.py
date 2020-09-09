"""
Name: Jinghong Xiao
Student number: 20035787
Lab 7-8; Assignment 3
Program: Huffman Coding
This program have two parts
Part 1: Implement the three modules and using a file to build the code-string dictionary,
then encode and decode some specified file
Part 2: Using different Canonical Collection file to encode and decode some specified file in Data directory
then analyze the encode file to compare the origin one
"""
import sys
import os


# class node use for build tree
class Node:
    def __init__(self, frequency):
        self.left = self.right = self.parents = None
        self.frequency = frequency

    def is_right(self):
        return self.parents.left == self


def readfile(filename):
    try:
        file = open(filename, "r", encoding="utf-8")
        return file.read()
    except OSError as error:
        print(error), sys.exit()
    except ValueError as error:
        print(error), sys.exit()


# set the printable characters
def printable_code():
    ascii_ = "\n !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    return ascii_


# function use to make a frequency dictionary and return the frequency
def make_frequency(data):
    frequency = {}
    printable = printable_code()
    for i in printable:
        frequency[i] = 0
    for k in data:
        frequency[k] += 1
    return frequency


# Recursive to make node (due to the frequency)
def create_nodes(frequency_list):
    return [Node(frequency) for frequency in frequency_list]


# Function use to create a Huffman tree, use queue to help create a Huffman tree
def create_tree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item: item.frequency)
        node_left, node_right = queue.pop(0), queue.pop(0)
        node_parents = Node(node_left.frequency + node_right.frequency)
        node_parents.left, node_parents.right = node_left, node_right
        node_left.parents, node_right.parents = node_parents, node_parents
        queue.append(node_parents)
    queue[0].parents = None
    return queue[0]


# Function use to encode the file data
def huff_encoding(nodes, root):
    huff_code = [''] * len(nodes)
    for i in range(len(nodes)):
        node = nodes[i]
        while node != root:
            if node.is_right():
                huff_code[i] = '0' + huff_code[i]  # if is right set 0
            else:
                huff_code[i] = '1' + huff_code[i]
            node = node.parents
    return huff_code  # get bac 0 or 1


# Function use to encode the file data, and get back all the huffman code
def encode(text, char_frequency, codes):
    result = ""
    for char in text:
        i = 0
        for item in char_frequency:
            if char == item[0]:
                result += codes[i]
            i += 1
    return result  # get back the code


# Function use to decode the huffman code, use frequency dictionary to decode that
def decode(huff_code, new_dict):
    result = ""
    current = ""
    for i in huff_code:
        current += i
        if current in new_dict:
            result += new_dict[current]
            current = ""
    return result


# Function use to write code string to a file
def write_code_string(frequency_dict, codes, code_string_file_name, current_dir):
    code_string_file_name = code_string_file_name.replace(".txt", "")
    code_string_file_name = code_string_file_name.replace("Data 20191031/", "")
    if "/" in code_string_file_name:
        code_string_file_name = code_string_file_name[code_string_file_name.index("/") + 1:]
    newfile = open(current_dir + "/" + code_string_file_name + "_code_string_dictionary.txt", 'w')
    index = 0
    newdict = {}
    for i in frequency_dict:
        newdict[codes[index]] = i
        newfile.write("%s %s" % (ord(i), codes[index]) + "\n")  # ord use to get ascii code
        index += 1
    newfile.close()
    return newdict


# Function use to write encode(huffman code) to a file
def write_encode(huff_code, encode_file, encode_dir):
    encode_file = encode_file.replace(".txt", "")
    encode_file = encode_file.replace("Data 20191031/", "")
    if encode_dir != "":
        encode_file = encode_dir + encode_file
    newfile = open(encode_file + "_encode.txt", 'w')
    newfile.write(huff_code)
    newfile.close()
    return encode_file + "_encode.txt"  # get back the directory


# Function use to write decode string to a file
def write_decode(decode_file, decode_str, decode_dir):
    decode_file = decode_file.replace(".txt", "")
    decode_file = decode_file.replace("Data 20191031/", "")
    if decode_dir != "":
        decode_file = decode_dir + decode_file
    newfile = open(decode_file + "_decode.txt", 'w')
    newfile.write(decode_str)
    newfile.close()


# code building module, use to read all the files, set frequency dictionary and apply huffman algorithm
def code_building(file_data, code_string_file_name, current_dir):
    frequency_dict = make_frequency(file_data)
    nodes = create_nodes([frequency_dict[i] for i in frequency_dict])
    root = create_tree(nodes)
    codes = huff_encoding(nodes, root)
    new_dict = write_code_string(frequency_dict, codes, code_string_file_name, current_dir)
    return frequency_dict, codes, new_dict


# encoding module, use to encoding all the data(call encode function)
def encoding(code_string_file_name, encode_file, encode_dir, decode_dir, current_dir):
    file_data_code_string = readfile(code_string_file_name)
    frequency_dict, codes, new_dict = code_building(file_data_code_string, code_string_file_name, current_dir)
    file_data_encode_data = readfile(encode_file)
    huff_code = encode(file_data_encode_data, frequency_dict, codes)
    encode_file_huffman_name = write_encode(huff_code, encode_file, encode_dir)  # write encode to a file
    decoding(encode_file_huffman_name, encode_file, new_dict, decode_dir)  # call decoding function


# decoding module, load code-string dictionary and encode file(huffman string) then encode the file
def decoding(encode_file_huffman_name, decode_file, new_dict, decode_dir):
    filedata = readfile(encode_file_huffman_name)
    decode_str = decode(filedata, new_dict)
    write_decode(decode_file, decode_str, decode_dir)  # encode the string to a file


# help function to analysis Canonical Collection 2.zip to get code-string dictionary
def write_c2(canonical_Collection2_list):
    result = ""
    for file in canonical_Collection2_list:
        result += readfile("Canonical Collection 2 20191031/" + file)
    newfile = open("Canonical Collection 2 20191031/Canonical Collection 2 20191031.txt", 'w')
    newfile.write(result)
    newfile.close()


# help function to analysis Canonical Collection 3.zip to get code-string dictionary
def write_c3(canonical_Collection3_list):
    result = ""
    for file in canonical_Collection3_list:
        result += readfile("Canonical Collection 3 20191031/" + file)
    newfile = open("Canonical Collection 3 20191031/Canonical Collection 3 20191031.txt", 'w')
    newfile.write(result)
    newfile.close()


# main function, all below codes are test code, all encode and decode files save the
# Canonical Collection x encode or Canonical Collection x decode
# x means which Canonical Collection file
def main():
    cwd = os.getcwd()  # get current directly
    # Part 1
    print("Part 1:")
    encoding("File1ASCII.txt", "File2ASCII.txt", "", "", cwd)
    # Part 1 code-string dictionary called File1ASCII_code_string_dictionary.txt
    print("\nFinish Part 1 encoding and decoding [Code-string dictionary:File1ASCII_code_string_dictionary.txt]\n")

    # Part 2
    print("\n\nPart 2:\n")
    datafile_list = os.listdir("Data 20191031")  # get all data file's file name
    canonical_Collection2_list = os.listdir("Canonical Collection 2 20191031")
    canonical_Collection3_list = os.listdir("Canonical Collection 3 20191031")

    for file in datafile_list:
        if ".txt" in file:
            encoding("words1ASCII.txt", "Data 20191031/" + file, cwd + "/Canonical Collection 1 encode/",
                     cwd + "/Canonical Collection 1 decode/", cwd)  # encoding and decoding use Canonical Collection 1
    print("Finish use [Canonical Collection 1] encoding and decoding all the documents in Data file\n")

    write_c2(canonical_Collection2_list)
    for file in datafile_list:
        if ".txt" in file:
            encoding("Canonical Collection 2 20191031/Canonical Collection 2 20191031.txt", "Data 20191031/" + file,
                     "Canonical Collection 2 encode/", "Canonical Collection 2 decode/", cwd)
            # encoding and decoding use Canonical Collection 2
    os.remove("Canonical Collection 2 20191031/Canonical Collection 2 20191031.txt")
    print("Finish use [Canonical Collection 2] encoding and decoding all the documents in Data file\n")

    write_c3(canonical_Collection3_list)
    for file in datafile_list:
        if ".txt" in file:
            encoding("Canonical Collection 3 20191031/Canonical Collection 3 20191031.txt", "Data 20191031/" + file,
                     "Canonical Collection 3 encode/", "Canonical Collection 3 decode/", cwd)
            # encoding and decoding use Canonical Collection 3
    os.remove("Canonical Collection 3 20191031/Canonical Collection 3 20191031.txt")
    print("Finish use [Canonical Collection 3] encoding and decoding all the documents in Data file\n\n")
    print("-" * 50)
    print("All part 2 encoding and decoding files in the [Canonical Collection x encode or Canonical Collection x "
          "decode]\nx is mean use which Canonical Collection file")
    print("-" * 50)

if __name__ == '__main__':
    main()
    # Continue Part2
    list_c1 = os.listdir("Canonical Collection 1 encode")  # get all the encode files directory
    list_c2 = os.listdir("Canonical Collection 2 encode")
    list_c3 = os.listdir("Canonical Collection 3 encode")
    # the origin file size, use encode ending is convenience for me calculate
    origin_size = {'WodehouseASCII_encode.txt': 403294, 'SimakASCII_encode.txt': 310126,
                   'MythsASCII_encode.txt': 740678, 'MysteryASCII_encode.txt': 444611, 'EarthASCII_encode.txt': 438284}
    size_dict1 = {}
    size_dict2 = {}
    size_dict3 = {}
    for file in list_c1:
        if ".txt" in file:
            size = len(readfile("Canonical Collection 1 encode/" + file)) / 8  # 8 bit = 1 byte
            size_dict1[file] = size
    for file in list_c2:
        if ".txt" in file:
            size = len(readfile("Canonical Collection 2 encode/" + file)) / 8  # 8 bit = 1 byte
            size_dict2[file] = size
    for file in list_c3:
        if ".txt" in file:
            size = len(readfile("Canonical Collection 3 encode/" + file)) / 8  # 8 bit = 1 byte
            size_dict3[file] = size

    print("\n\nPart 2 experiments results:")
    # Part 2 experiments results
    print("\nUse Canonical Collection 1:\n")
    for i in size_dict1:
        if i in origin_size:
            print(i, "      Compress origin size file:" + str(round((size_dict1[i] / origin_size[i]) * 100)) + "%")

    print("\nUse Canonical Collection 2:\n")
    for i in size_dict2:
        if i in origin_size:
            print(i, "      Compress origin size file:" + str(round((size_dict2[i] / origin_size[i]) * 100)) + "%")

    print("\nUse Canonical Collection 3:\n")
    for i in size_dict3:
        if i in origin_size:
            print(i, "      Compress origin size file:" + str(round((size_dict3[i] / origin_size[i]) * 100)) + "%")


"""
Part 3 results and conclusions:
According to my Part 2 results of experiments, the Canonical Collection 3 gives the best results, and
Canonical Collection 2 almost tie the Canonical Collection 3, the different between Canonical Collection 2 and
Canonical Collection 3 is WodehouseASCII.txt and MysteryASCII.txt in Canonical Collection 3 compress one more percent
than Canonical Collection 2. The Canonical Collection 1 is the worst, some encode file even bigger than origin file.

Why they difference? Because each Canonical Collection file gives different frequencies, thus some printable letters give
high frequency in the code-string dictionary but they actually in origin file is not that high frequency, and some have a high
frequency in origin file, however, in the code-string dictionary they do not have that high.
So that's why they have a big difference like Canonical Collection 3 have better results and Canonical Collection 1 not.
"""
