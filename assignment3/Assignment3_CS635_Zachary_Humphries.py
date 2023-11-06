# Zachary Humphries
# Assignment 3
# CS 635
# November 5, 2023

from abc import ABC, abstractmethod, ABCMeta

# Creating a Student class object to store the firstName, lastName, redId, gpa
class Student:
    def __init__(self, firstName,lastName,redId,gpa):
        self.firstName = firstName
        self.lastName = lastName
        self.redId = int(redId)
        self.gpa = gpa

#Creating NullStudent to go along with NullNode
class NullStudent:
    def __init__(self):
        self.firstName = " "
        self.lastName = " "
        self.redId = 0
        self.gpa = 0.0

# Abstract Class (DependencyBase) for Null Object Pattern
class AbstractNode(ABC):
    def __init__(self, student):
        self.student = student
        self.left = None
        self.right = None
        self.isRoot = False

        super().__init__()

    @abstractmethod
    def accept(self, visitor) -> bool:
        pass



# Null Object for Abstract Class: Creates NullTreeNode
class NullTreeNode(AbstractNode):
    def __init__(self):
        self.student = NullStudent()
        self.left = None
        self.right = None
        self.isRoot = False

    # Accept Function for Visitor Design Pattern
    def accept(self, visitor) -> bool:
        return visitor.VisitNode(self)

    # Function Used By Both Visitors
    def isTreeNode(self) -> bool:
        return False


# Dependency for Abstract Class: Creates TreeNode
class TreeNode(AbstractNode):
    def __init__(self, studentInput):
        self.student = studentInput
        self.left =  None
        self.right = None
        self.isRoot = False

    # Accept Function for Visitor Design Pattern
    def accept(self, visitor) -> bool:
        return visitor.VisitNode(self)

    # Function Used By Both Visitors
    def isTreeNode(self) -> bool:
        return True



# Abstract Visitor Class
class AbstractVisitor(ABC):

    @abstractmethod
    def VisitNode(self, element) -> bool:
        pass

# Visitor Class Used to Calculate Number of NullTreeNodes in Tree
class Visitor1(AbstractVisitor):
    def __init__(self):
        self.nullNodeCount = 0

    def VisitNode(self, element) -> bool:
        return element.isTreeNode()

    def increaseNullTreeNodeCount(self) -> None:
        self.nullNodeCount += 1
        
# Visitor Class Used to Calculate Longest Branch Length and Average Branch Length
class Visitor2(AbstractVisitor):
    def __init__(self):
        self.totalNodesTraversed = 0
        self.longestBranchLength = 0
        self.branchesTraversed = 0
        self.averageBranchLength = 0.0

    def VisitNode(self, element) -> bool:
        return element.isTreeNode()
    
    def calculateAverageBranchLength(self) -> float:
        self.averageBranchLength = self.totalNodesTraversed/self.branchesTraversed
        return self.averageBranchLength




class BinarySearchTree:
    def __init__(self, orderingStrategy):
        self.root = NullTreeNode()
        self.root.isRoot = True

        # orderingStrategy (1: order by redID, 2: order by lastName then firstName, 3: order by rounded gpa then redID)
        self.orderingStrategy = orderingStrategy

    # returns true if the relevant ordering strategy is met
    # will continue down left side of tree so if true, will be places beforehand/down left side of tree
    def matchesOrderingStrategy(self, currTreeNode, student):
        if (self.orderingStrategy == 1):
            # order by redID: 
            # True if "to be inserted" node's redID is smaller than "compared" node's redID
            return student.redId < currTreeNode.student.redId
        elif (self.orderingStrategy == 2):
            # order by firstName then lastName: 
            # True if "to be inserted" node's lastName (then firstName) is alphabetically smaller 
            # than "compared" node's lastName (then firstName if lastName is same)
            return (student.lastName.lower() + student.firstName.lower()) < \
                (currTreeNode.student.lastName.lower() + currTreeNode.student.firstName.lower())
        elif (self.orderingStrategy == 3):
            # order by "rounded to closest integer" gpa then redID:
            # TRUE if "to be inserted" node's gpa (rounded to the closest integer) is smaller than "compared" node's gpa
            # if rounded gpa's are the same, then redID is used
            if (((int)(student.gpa + 0.5)) == ((int)((currTreeNode.student.gpa) + 0.5))):
                return (student.redId < (currTreeNode.student.redId))
            else:
                return (((int)(student.gpa + 0.5)) > ((int)((currTreeNode.student.gpa) + 0.5)))
        else:
            return None
        

    # inserts a new TreeNode into BinarySearchTree
    def insert(self, currTreeNode, student):
        # creates new TreeNode if referenced node does not exist AND student is of class Student
        if (((currTreeNode is None)) and isinstance(student, Student)):
            return TreeNode(student)
        # creates new TreeNode if referenced node does not exist AND student is of class NullStudent
        elif ((currTreeNode is None) and isinstance(student, NullStudent)):
            return NullTreeNode()
        # continues left down the tree if ifMatchesOrderingStrategy is met and right if not met
        else:
            if (self.matchesOrderingStrategy(currTreeNode, student)):
                currTreeNode.left = self.insert(currTreeNode.left, student)
            else:
                currTreeNode.right = self.insert(currTreeNode.right, student)
            return currTreeNode
        
    # internal iterator that accepts any lambda/function and evaluates on all TreeNodes from left-most to right-most
    def forEach(self, currTreeNode, fn, *argv):
        if (not(currTreeNode == None)):
            self.forEach(currTreeNode.left, fn, *argv)
            fn(currTreeNode, *argv)
            self.forEach(currTreeNode.right, fn, *argv)

    # counts NullNodes by Using Visitor1
    def countNullNodes(self, currTreeNode):
        visitor = Visitor1()
        def evaluateNullNode(currTreeNode, visitor):
            isTreeNode = currTreeNode.accept(visitor)
        
            if(not(isTreeNode)):
                visitor.increaseNullTreeNodeCount()

        self.forEach(currTreeNode, evaluateNullNode, visitor)

        return visitor.nullNodeCount
    
    # recursive function that writes all branches into a double array
    def writeAllBranches(self, currTreeNode, tempArray, allBranches):
        if (currTreeNode is None):
            return
        
        # appends node's student data
        tempArray.append(currTreeNode.student)

        # if at leaf node in tree, then a copy of the tempArray is appended to allBranches
        if ((currTreeNode.left is None) and (currTreeNode.right is None)):
            allBranches.append(tempArray.copy())
            # last node's data in tempArray is deleted
            del tempArray[-1]
            return
        
        # recursively goes down tree to the left and then more to the right
        self.writeAllBranches(currTreeNode.left, tempArray, allBranches)
        self.writeAllBranches(currTreeNode.right, tempArray, allBranches)
        del tempArray[-1]
    
    # Uses Visitor2 to provide longest and average branch lengths
    def calculateLongestAndAverageBranch(self, currTreeNode):    
        visitor = Visitor2()    
        allBranches = []
        tempArray = []

        self.writeAllBranches(currTreeNode, tempArray, allBranches)

        # returns array of lengths of each branch
        def lengthOfEachBranch(allBranches):
            allBranchesLength = [len(branch) for branch in allBranches]
            return allBranchesLength
        
        visitor.branchesTraversed = len(allBranches)

        branchLengthArray = lengthOfEachBranch(allBranches)

        visitor.totalNodesTraversed = sum(branchLengthArray)
        visitor.longestBranchLength = max(branchLengthArray)
        visitor.averageBranchLength = visitor.calculateAverageBranchLength()

        return [visitor.longestBranchLength, visitor.averageBranchLength]



if __name__ == "__main__":
    students = [                                         #Creating a list of students to add to the tree 
        Student("Juanita","Hernandez", 1234567, 3.8),
        Student("Zachary","Humphries", 9018338, 3.9),
        Student("Donte","Robertson", 2374019, 3.4),
        Student("Abbas","Mazloumi", 123422937, 2.2),
        Student("Robert","Smith", 2038622, 2.5),
        Student("Xavier", "Smith", 1923863, 2.5),
        NullStudent(),
        NullStudent(),
        NullStudent()
    ]

    # Function to Print Node's Data
    def printNode(currTreeNode):
        student = currTreeNode.student
        print(f"Red Id: {student.redId}, FirstName: {student.firstName}, LastName: {student.lastName}, GPA: {student.gpa}")


    # ------------------ Strategy 1 ------------------
    print("Strategy 1")
    strategy1 = BinarySearchTree(1)

    # inserts all students into Binary Search Tree
    for student in students:
        strategy1.insert(strategy1.root, student)

    # prints sorted students
    print("Sorted by RedId:")
    strategy1.forEach(strategy1.root, printNode)

    # prints number of NullTreeNodes
    print("Number of NullTreeNodes (Including Root): " + str(strategy1.countNullNodes(strategy1.root)))

    # prints longest and average branch length
    [longestBranchLength, averageBranchLength] = strategy1.calculateLongestAndAverageBranch(strategy1.root)
    print("Longest Branch Length: " + str(longestBranchLength))
    print("Average Branch Length: " + str(averageBranchLength))


    # ------------------ Strategy 2 ------------------
    print("\nStrategy 2")
    strategy2 = BinarySearchTree(2)

    for student in students:
        strategy2.insert(strategy2.root, student)

    print("Sorted by lastName then firstName:")
    strategy2.forEach(strategy2.root, printNode)

    print("Number of NullTreeNodes (Including Root): " + str(strategy2.countNullNodes(strategy2.root)))

    [longestBranchLength, averageBranchLength] = strategy2.calculateLongestAndAverageBranch(strategy2.root)
    print("Longest Branch Length: " + str(longestBranchLength))
    print("Average Branch Length: " + str(averageBranchLength))



    # ------------------ Strategy 3 ------------------
    print("\nStrategy 3")
    strategy3 = BinarySearchTree(3)

    for student in students:
        strategy3.insert(strategy3.root, student)

    print("Sorted by rounded gpa then redID:")
    strategy3.forEach(strategy3.root, printNode)

    print("Number of NullTreeNodes (Including Root): " + str(strategy3.countNullNodes(strategy3.root)))

    [longestBranchLength, averageBranchLength] = strategy3.calculateLongestAndAverageBranch(strategy3.root)
    print("Longest Branch Length: " + str(longestBranchLength))
    print("Average Branch Length: " + str(averageBranchLength))





    




