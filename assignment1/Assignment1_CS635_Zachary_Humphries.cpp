// Zachary Humphries
// Assignment 1
// CS 635
// September 13, 2023


// C++ code that inserts words into a Trie and allows for a substring search
#include <bits/stdc++.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstring>

using namespace std;

// alphabet is a through z
const int ALPHABET_LENGTH = 26;

// trie node
struct Node
{
	struct Node *children[ALPHABET_LENGTH];

	// endNode is true if the node is the last node of trie (end of word)
	bool endNode;
};

// Returns new trie node (initialized to NULLs)
struct Node *getNode(void)
{
	struct Node *newNode = new Node;

	newNode->endNode = false;

	for (int i = 0; i < ALPHABET_LENGTH; i++)
		newNode->children[i] = NULL;

	return newNode;
}

// Returns index of letter in alphabet
// Also used to determine if character is not in alphabet
int letterIndex(char letter){
	return (letter - 'a');
}

// Returns true if letters in word are all in alphabet
bool lettersAreInAlphabet(string word)
{
	int index;
	for (int i = 0; i< word.length(); i++)
	{
		index = letterIndex(word[i]);

		if(index < 0 || index > 25)
			return false;
	}

	return true;
}

// Returns word as lowercase
string toLowerCase(string word)
{
	int index;

	for (int i = 0; i< word.length(); i++) {
		index = letterIndex(word[i]);

		if(index < 0 || index > 25)
			word[i] = word[i] + 32;
	}

	return word;

}



// Inserts word into trie
void insert(struct Node *root, string word)
{
	struct Node *childNode = root;

	for (int i = 0; i < word.length(); i++)
	{
		int index = letterIndex(word[i]);

		// if letter is not present in trie, makes a new node
		if (!childNode->children[index])
			childNode->children[index] = getNode();

		childNode = childNode->children[index];
	}

	// mark last node/letter as end node
	childNode->endNode = true;
}

// returns true if substring is within string (does not return npos value of -1)
bool containsSubstring(std::string prefix, std::string substring)
{
    return (prefix.find(substring) != std::string::npos);
}

// searches through each word inputted into trie
void searchSubstring(std::string& substring, std::string& prefix, Node const& node) 
{
	// prints if at last node/letter and the word contains the specified substring
	if (node.endNode && containsSubstring(prefix, substring))
    cout << prefix << endl;

	// iterates through each index (letter) and sees if that index is in trie
	for (char index = 0; index < ALPHABET_LENGTH; ++index) 
	{
    	char next = 'a'+index;
    	Node const* childNode = node.children[index];

		// if index is in trie, appends letter to prefix
    	if (childNode) 
		{
      		prefix.push_back(next);
      		searchSubstring(substring, prefix, *childNode);
      		prefix.pop_back();
    	}
  	}
}


int main()
{

	struct Node *root = getNode();

	// Input words (alphabet letters only, case insensitive)
	string words[] = {"hello", "mister", "hardware",
					"batters", "are", "a",
					"plenty", "here!" };
	
	int n = sizeof(words)/sizeof(words[0]);

	// Changes words to all lowercase and checks each word to see if in alphabet
	for (int i = 0; i < n; i++){
		string word;
		word = toLowerCase(words[i]);
		if(lettersAreInAlphabet(word)){
			insert(root, word);
		} else {
			cout << "\"" << words[i] << "\" contains a letter outside of the standard alphabet. Skippping word..."<<endl;
		}
	}

    std::string allWords;
    std::string substring = "ar";
    cout<<"printing all containing \"" << substring << "\"... " <<endl;

    searchSubstring(substring, allWords, *root);

	return 0;
}
