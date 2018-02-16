#!/usr/bin/env python3
import argparse
import math
import sys
import struct

# Reads input file and returns a list, each row is a block
def readFile (blocksize, input_file, transform):
    data = []

    if (transform == 0):    #forward transform
        with open(input_file) as input_file:
            while True:
                eot  = chr(3)
                temp = input_file.read(blocksize)
                block = temp + eot
                if temp == '':
                    break
                data.append(block)      

    elif (transform == 1):    #backward transform
        with open(input_file, mode = "r", encoding = "latin-1") as input_file:
            header = input_file.read(4)         # ignores first 4 bytes
            
            #converting blocksize to int
            temp = input_file.read(4)
            chars = list(temp)
            ints = [ord(c) for c in chars]      # ???
            arr_bytes = bytearray(ints)         # ??? 2d array
            blocksize = struct.unpack("I",arr_bytes)    #??? what??
            blocksize = blocksize[0]

            while True:
                eot  = chr(3)
                temp = input_file.read(blocksize+1)
                block = temp + eot
                if temp == '':
                    break

                data.append(block)
            data.append(blocksize)
    return data

def backwardTrans (data, backwardResult):
    step1 = []
    step2 = []
    holder = data[:-1]

    #attaching data to step1
    step1 = [ind for ind in data[:-1]]

    while ( len(step1[0]) < len(step1) ):
        step2 = sorted(step1)
        new_col = [item[-1] for item in step2] 
        step1 = ["".join(item) for item in list(zip(step1,new_col))]

    backwardResult.append(testLastChar(step1))
    return backwardResult

# Backward transform helper method- Finds string that has EOT char at the end of the string
def testLastChar (block):
    s = [i for i in range (len(block)) if block[i][-1] == chr(3)]
    
    return block[s[0]][:-1]

def forwardTrans (data, forwardResult):   
    # rotates block
    data_len = len(data)
    rotation = []
    for i in range (0, data_len ):
        temp = ""
        for j in range (0, data_len ):
            temp += data [(i+j)%data_len]
        rotation.append(temp)

    rotation.sort()

    # Gets last char from rotation list
    temp = ""
    for i in range (0, data_len):
        temp = temp +rotation[i][-1]
    forwardResult.append(temp)
    
    return forwardResult

#Writes resulting array for forward and backward transform in outfile
def writeOut (result, output_file, blocksize, transform):
    with open(output_file, mode = "w", encoding = "latin-1") as out_file:

        if (transform == 0):    #forward transform
            out_file.write("\xab\xba\xbe\xef") 

            #writting block size
            wakabytes = struct.pack("I", blocksize)
            chars = [chr(c) for c in wakabytes] # ??? EXPLAIN FOR LOOP????
            s = "".join(chars)
            out_file.write(s)

        for item in result:
            out_file.write(item)

def main():
    data = []
    transform_result = []

    # Parsing command line arguments
    parser = argparse.ArgumentParser(description= 'Phase 1 transform')
    parser.add_argument('--forward', action='store_true')
    parser.add_argument('--backward', action='store_true')
    parser.add_argument('--infile', help='Location of input file')
    parser.add_argument('--outfile', help='Location of output file')
    parser.add_argument('--blocksize', type = int, help='Size of each block to be read from input')
    args = parser.parse_args() # ?????????

    #forward transform
    if (args.forward == True):
        print("\nProcessing forward transform...");

        transform = 0
        print("Opening file:", args.infile);
        data = readFile(args.blocksize, args.infile, transform)

        print("Applying transform...");
        for i in range (0, len(data)):
            transform_result = forwardTrans(data[i], transform_result)

        print("Writting out result on file: %s" % args.outfile);
        writeOut(transform_result, args.outfile, args.blocksize, transform)
        print("Process completed succesfully.");

    #backward transform
    elif (args.backward == True):
        print("\nProcessing backward transform...");
        transform = 1
        print("Opening file:", args.infile);
        data = readFile(0, args.infile, transform) # 0 is a temp holder for blocksize updated in method

        print("Applying transform...");
        for i in range (0, len(data)-1):        # -1, ignores the last block which is the blocksize
            transform_result = backwardTrans(data[i], transform_result)

        print("Writting out result on file: %s"% args.outfile);
        writeOut(transform_result, args.outfile, args.blocksize, transform)
        print("Process completed succesfully.");
        
if __name__ == "__main__":
    main()