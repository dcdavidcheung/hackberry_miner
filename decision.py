import sys
import math

# Structure to store final tree
class Node:
    def __init__(self, label, depth, split_attribute, node_attribute):
        self.left = None
        self.right = None
        self.val = label
        self.depth = depth
        self.splitAttr = split_attribute
        self.attrVal = node_attribute

# Conduct a majority vote at a given node
def conductMajVote(node):
    dataPoints = node.val
    listOfData = []
    for key in dataPoints:
        listOfData = dataPoints[key]
    
    counts = {}
    for dataP in listOfData:
        label = dataP[-1]
        if (not label in counts):
            counts[label] = 1
        else:
            counts[label] += 1
    
    majority = ["", 0]
    for entry in counts:
        if (counts[entry] > majority[1]):
            majority[0] = entry
            majority[1] = counts[entry]

    return majority[0]

# Get the entropy at a given node
def getEntropy(node):
    counts = {}
    totalCount = 0

    listofData = []
    for key in node:
        listofData = node[key]
    
    for dataList in listofData:
        label = dataList[-1]
        if (not label in counts):
            counts[label] = 1
        else:
            counts[label] += 1
        totalCount += 1

    entropy = 0
    for count in counts:
        prob = counts[count] / totalCount
        entropy += -1 * prob * math.log2(prob)
    return entropy

# Get the conditional entropy at a given node after a split
def getConditionalEntropy(node):
    totalCondEntropy = 0
    values = []
    totalNum = 0
    for split in node:
        counts = {}
        totalCount = 0

        listofData = node[split]
        for dataList in listofData:
            label = dataList[-1]
            if (not label in counts):
                counts[label] = 1
            else:
                counts[label] += 1
            totalCount += 1
        
        partialCondEntropy = 0
        for count in counts:
            prob = counts[count] / totalCount
            partialCondEntropy += -1 * prob * math.log2(prob)
        values.append((partialCondEntropy, totalCount))
    for value in values:
        totalNum += value[1]
    for tup in values:
        totalCondEntropy += tup[0] * (tup[1] / totalNum)
    return totalCondEntropy

# Get the mutual information of a split
def getMutualInfo(beforeSplit, afterSplit):
    return getEntropy(beforeSplit) - getConditionalEntropy(afterSplit)

# Split data along a specific attribute
def split(beforeSplit, attrNum):
    afterSplit = {}
    for i in beforeSplit.values():
        for dataPoint in i:
            key = dataPoint[attrNum]
            if (not key in afterSplit):
                afterSplit[key] = []
            afterSplit[key].append(dataPoint)
    return afterSplit

# Take in all the data from training
# Configure get_data.py to give .csv file with known format
# Assume data format will be comma separated (csv)
def processData(trainIn):
    # Open file to get data from
    trainData = open(trainIn, "r")
    
    dictOfData = {'root' : []}
    currLine = trainData.readline()
    currData = currLine.split(",")
    numAttr = len(currData[:-1])

    while (currLine != ''):
        currLine = trainData.readline()
        if (currLine == ''):
            break
        currData = currLine.strip().split(",")
        dictOfData['root'].append(currData)

    # Start the tree at its root
    finalTree = Node(dictOfData, 0, None, None)

    # Close files that were opened
    trainData.close()
    return (finalTree, numAttr)

# Recursive function, build tree
def decisionTree(tree, maxDepth, numAttr):
    if (tree.depth == maxDepth):
        return tree
    else:
        mutualInfoList = []

        # Split on each attribute to find the one with most mutual information
        for i in range(numAttr):
            splitData = split(tree.val, i)
            mutualInfo = getMutualInfo(tree.val, splitData)
            mutualInfoList.append(mutualInfo)
        # Determine which attribute leads to most mutual information
        mostPositive = [0, -1]
        for index in range(len(mutualInfoList)):
            if (0 < mutualInfoList[index] and mostPositive[0] < mutualInfoList[index]):
                mostPositive[0] = mutualInfoList[index]
                mostPositive[1] = index
        
        # Mutual informations were all negative
        if (mostPositive[1] == -1):
            return tree
        else:
            # Split on attribute that gives most mutual information
            splitData = split(tree.val, mostPositive[1])
            attrBranches = []
            for branch in splitData:
                attrBranches.append(branch)
            
            # Set up for recursion
            leftVal = {}
            rightVal = {}
            leftVal[attrBranches[0]] = splitData[attrBranches[0]]
            rightVal[attrBranches[1]] = splitData[attrBranches[1]]
            leftNode = Node(leftVal, tree.depth + 1, mostPositive[1], attrBranches[0])
            rightNode = Node(rightVal, tree.depth + 1, mostPositive[1], attrBranches[1])
            tree.left = decisionTree(leftNode, maxDepth, numAttr)
            tree.right = decisionTree(rightNode, maxDepth, numAttr)
            return tree

# Follow the tree
def followTree(tree, datapoint, maxDepth):
    currDepth = 0
    while (currDepth < maxDepth):
        leftTree = tree.left
        rightTree = tree.right
        if (leftTree != None):
            leftAttrVal = leftTree.attrVal
        else:
            leftAttrVal = None
        if (rightTree != None):
            rightAttrVal = rightTree.attrVal
        else:
            rightAttrVal = None
        if (leftTree != None):
            splitAttr = leftTree.splitAttr
        elif (rightTree != None):
            splitAttr = rightTree.splitAttr
        else:
            break
        
        dataVal = datapoint[splitAttr]
        if (leftTree == rightTree == None):
            break
        elif (leftTree == None):
            if (rightAttrVal == dataVal):
                tree = rightTree
                currDepth += 1
            else:
                break
        elif (rightTree == None):
            if (leftAttrVal == dataVal):
                tree = leftTree
                currDepth += 1
            else:
                break
        else:
            if (leftAttrVal == dataVal):
                tree = leftTree
                currDepth += 1
            elif (rightAttrVal == dataVal):
                tree = rightTree
                currDepth += 1
            else:
                break

    return conductMajVote(tree)

# python3 decision.py train_data_fake.csv
if __name__ == '__main__':
    # Training Data
    trainIn = sys.argv[1]

    # Hyperparameter
    maxDepth = 2

    (trainTree, numAttr) = processData(trainIn)
    finalTree = decisionTree(trainTree, maxDepth, numAttr)
    test_inf = ["up", "up", "btc"]
    print(followTree(finalTree, test_inf, maxDepth))
    test_inf = ["up", "down", "btc"]
    print(followTree(finalTree, test_inf, maxDepth))
    test_inf = ["down", "up", "eth"]
    print(followTree(finalTree, test_inf, maxDepth))
    test_inf = ["down", "down", "btc"]
    print(followTree(finalTree, test_inf, maxDepth))