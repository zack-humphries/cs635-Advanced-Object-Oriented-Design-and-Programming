// Zachary Humphries
// Assignment 2
// CS 635
// October 13, 2023

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstring>
#include <bits/stdc++.h>
#include <string>

using namespace std;

class BinarySearchTree
{
    // orderingStrategy (1: order by redID, 2: order by lastName then firstName, 3: order by rounded gpa then redID)
    public:
        int orderingStrategy;

    // set orderingStrategy in main through setOrderingStrategy
    void setOrderingStrategy(int order){
        orderingStrategy = order;
    }

    // Binary Search Tree Node
    struct TreeNode {
        // set a unqiue key for each node based on orderingStrategy
        std::string key;

        // student information
        int redID;
        std::string firstName;
        std::string lastName;
        float gpa;

        // define nodes to the left and right of current tree node
        TreeNode *left; 
        TreeNode *right;
    };

    // returns new TreeNode
    struct TreeNode *getTreeNode(void)
    {
        struct TreeNode *newNode = new TreeNode;
        return newNode;
    }

    // returns TRUE if TreeNode has not been initialized
    static bool isEmpty(const TreeNode *t) {
        return t == nullptr;
    }

    // Returns index of letter in alphabet
    // Used to determine if character is uppercase or lowercase in toLowerCase
    int letterIndex(char letter){
	    return (letter - 'a');
    }

    // Returns word as lowercase if uppercase
    string toLowerCase(string word)
    {
        int index;
        for (int i = 0; i < (int) word.length(); i++) {
            index = letterIndex(word[i]);

            if (index < 0 || index > 25)
                // uses ASCII property where a lowercase letter is 32 more than respecive uppercase letter
                word[i] = word[i] + 32;
        }

        return word;

    }

    // returns a unique key based on orderingStrategy
    string makeKey(int redID, std::string firstName, std::string lastName, float gpa){

        if (orderingStrategy == 1){
            return (std::to_string(redID));
        } else if(orderingStrategy == 2){
            return (toLowerCase(lastName + firstName));
        } else if(orderingStrategy == 3){
            return (std::to_string((int)(gpa + 0.5f)) + std::to_string(redID));
        }

        return "";

    }

    // returns true if the relevant ordering strategy is met
    // will continue down left side of tree so if true, will be places beforehand/down left side of tree
    bool ifMatchesOrderingStrategy(TreeNode *t, int redID, std::string firstName, std::string lastName, float gpa){

        if (orderingStrategy == 1){
            // order by redID: 
            // TRUE if "to be inserted" node's redID is smaller than "compared" node's redID
            return (redID < t -> redID); 
        } else if(orderingStrategy == 2){
            // order by firstName then lastName: 
            // TRUE if "to be inserted" node's lastName (then firstName) is alphabetically smaller 
            // than "compared" node's lastName (then firstName if lastName is same)
            return (toLowerCase(lastName + firstName) < toLowerCase((t -> lastName) + (t -> firstName)));
        } else if(orderingStrategy == 3){
            // order by "rounded to closest integer" gpa then redID:
            // TRUE if "to be inserted" node's gpa (rounded to the closest integer) is smaller than "compared" node's gpa
            // if rounded gpa's are the same, then redID is used
            if (((int)(gpa + 0.5f)) == ((int)((t -> gpa) + 0.5f)) )
                return (redID < (t -> redID));
            else
                return (((int)(gpa + 0.5f)) > ((int)((t -> gpa) + 0.5f)));
        }

        return NULL;

    }

    // inserts a new TreeNode into BinarySearchTree
    TreeNode * insert(TreeNode *t, int redID, std::string firstName, std::string lastName, float gpa){
        
        // makes a unique key for each TreeNade
        std::string key = makeKey(redID, firstName, lastName, gpa);

        // creates new TreeNode if referenced node does not exist
        if (isEmpty(t)){
            return new TreeNode{key, redID, firstName, lastName, gpa, nullptr, nullptr};
        } else {
            // continues left down the tree if ifMatchesOrderingStrategy is met and right if not met
            if (ifMatchesOrderingStrategy(t, redID, firstName, lastName, gpa)){
                t -> left = insert(t->left, redID, firstName, lastName, gpa);
                }
            else {
                t -> right = insert(t->right, redID, firstName, lastName, gpa);
                }
            return t;
        }
    }

    // internal iterator that accepts any lambda/function and evaluates on all TreeNodes from left-most to right-most
    template< typename Function >
    static void forEach(TreeNode *t , Function fn ) {
        if( !isEmpty(t)){
            forEach(t->left, fn );
            fn(t);
            forEach( t->right, fn );
        }
    }

};




int main()
{

    // Sets up example case with 7 students
    int n = 7;
    int redIdList[] = {1234, 321, 865369, 5492194, 204850182, 481394, 574629};
    string firstNameList[] = {"Juana", "Zachary", "Donte", "Alexandria", "Abbas", "Xavier", "Rondel"};
    string lastNameList[] = {"Hernandez", "Humphries", "Robertson", "Bilbao", "Mazloumi", "Smith", "Smith"};
    float gpaList[] = {3.5, 3.9, 3.8, 3.1, 2.4, 2.8};

    // --------------- Strategy 1 ---------------
    // creates new instance of class
	BinarySearchTree strategy1; 

    // sets orderingStrategy in class
    strategy1.setOrderingStrategy(1);

    // creates root TreeNode
    struct BinarySearchTree::TreeNode *root1 = strategy1.getTreeNode();
    
    // inserts example case's student information
    for (int i = 0; i < n; i++){
        strategy1.insert(root1, redIdList[i], firstNameList[i], lastNameList[i], gpaList[i]);
    }

    // calls forEach function to print student information in order with following lambda expression
    strategy1.forEach(root1, [](BinarySearchTree::TreeNode *root){
        std::cout << root -> redID << " " << root -> firstName << " " << root -> lastName << " " << root -> gpa << std::endl;
    });
    std::cout << std::endl << std::endl; 



    // --------------- Strategy 2 ---------------
    BinarySearchTree strategy2;
    strategy2.setOrderingStrategy(2);

    struct BinarySearchTree::TreeNode *root2 = strategy2.getTreeNode();
    for (int i = 0; i < n; i++){
        strategy2.insert(root2, redIdList[i], firstNameList[i], lastNameList[i], gpaList[i]);
    }
    strategy2.forEach(root2, [](BinarySearchTree::TreeNode *root){
        std::cout << root -> redID << " " << root -> firstName << " " << root -> lastName << " " << root -> gpa << std::endl;
    });
    std::cout << std::endl << std::endl;


    // --------------- Strategy 3 ---------------
    BinarySearchTree strategy3;
    strategy3.setOrderingStrategy(3);

    struct BinarySearchTree::TreeNode *root3 = strategy3.getTreeNode();
    for (int i = 0; i < n; i++){
        strategy3.insert(root3, redIdList[i], firstNameList[i], lastNameList[i], gpaList[i]);
    }
    strategy3.forEach(root3, [](BinarySearchTree::TreeNode *root){
        std::cout << root -> redID << " " << root -> firstName << " " << root -> lastName << " " << root -> gpa << std::endl;
    });
    std::cout << std::endl << std::endl << "Done";



	return 0;
}

