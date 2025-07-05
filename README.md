# A Compiler Built from Scratch

This repository documents my progress in building a compiler from scratch. It's purpose is to increase my understanding of compiler technology and exhibit my technical skills. The compiler implements a high level procedural programming language. It supports a minimal set programming constructs like loops, functions, conditionals, variable assignment, types and more.

## Lexer

### Regular Expressions

The design process starts by writing regular expressions which are capable of expressing the set of tokens my lexer should recognise. 


### Converting the Regular Expressions to Nondeterministic Finite Automata (NFA)

Converting these regular expressions to NFA resulted in unmanageable complexity due to the combinatorial explosion of branching as a result of using raw regular expressions. I decided to use character classes defined in regular defintions as transitions in the NFA. This choice reduces the complexity of the NFA but requires us to resolve which character belongs to which transition (you will see later that I chose to resolve this by preprocessing the state table). 


### Converting the NFA into a deterministic finite automaton (DFA) by subset construction

By finding the epsilon colsure of each transtion in the NFA we can generate a DFA. I do this recursively until all states transiton to a state thats already been defined in the DFA.


### Prototyping the Lexer 

I learned three things from prototyping the lexer 
1. keywords should be recognised as IDs and checked against hardcoded keywords
2. The state table should be processed to flatten the transition classes into individual characters
3. Use disjoint character classes on the first state of the combined NFA (this is possible because of 1.)

(1.) Simplifies subset construction at the expense of a couple of lines of extra code in the lexer. (2.) Removes the runtime logic in the lexer needed to resolve whether a character belongs to a transition class. This makes the lexer logic more readable and allows for an average case O(1) lookup. (3.) Reduces the complexity of token creation by removing the need for priority rules based on token type. The lexer can naturally take the longest token once no more transitions are possible.


### Finalised Automata
With these contraints the finalised regular defintions NFAs and DFA are below. (note the DFA is not drawn, all information required to implement the state table is present in the subset construction.)


#### Regular Definitions
```
letters_ -> [a-zA-Z_]      
digits   -> [0-9]  
ID       -> letters_(letters_|digits)* 

digits         -> [0-9]  
digits_not_0   -> [1-9]  
number_literal -> (0|digits_not_0digits)*)(.digits⁺)?

ascii          -> [\x00-\x7F]  
string_literal -> "ascii*"

op -> [+|-|*|/|=|>|<|||&|!|%]

punctuatuon -> [(|)|;|:|,|[|]|{|}]

whitespace -> [ |\t|\n|\r]
```
#### NFA
#### Subset Construction/DFA
```
S1 = {1, 10, 11}

δ(S1, letters_) = S2 = {2, 3, 4, 6, 9}
δ(S1, digits_not_0) = S3 = {12, 14, 16, 17, 18, 21}
δ(S1, 0) = S4 = {13, 17, 18, 21}
δ(S1, ") = S5 = {22, 23, 25}
δ(S1, op) = S6 = {27}
δ(S1, punctuation) = S7 = {28}
δ(S1, whitespace) = S8 = {29}

δ(S2, letters_) = S9 = {5, 8, 3, 4, 6, 9}
δ(S2, digits) = S10 = {7, 8, 3, 4, 6, 9}

δ(S3, digits) = S11 = {15, 14, 16, 17, 18, 21}
δ(S3, .) = S12 = {19}

δ(S4, .) = S13 = S12

δ(S5, ascii) = S13 = {24, 23, 25}
δ(S5, ") = S14 = {26}

δ(S9, letters_) = S9 
δ(S9, digits) = S10 

δ(S10, letters_) = S9 
δ(S10, digits) = S10 

δ(S11, digits) = S11
δ(S11, .) = S12 

δ(S12, digits) = S15 = {20, 19, 21} 

δ(S13, ascii) = S13
δ(S13, ") = S14

δ(S15, digits) = S15
```






### Lexing Logic and State Table Construction

The `raw_state_table` is implemented as a nested dictionary in `raw_state_table.py` allowing it to be accessed with meaninful names in constant time on average.  This results in a data structure that is readable and efficient. Rather than hardcoding the transition classes at each state, I use a separate dictionary, `transition_classes`, to encapsulate them. The values of of the transition classes are implemented as strings for fast iteration. An Enum is used for the transition class keys to encapsulate key definitions which increases maintainability and reduces errors from mispelled/invalid keys. The `lexer` code is designed to be as clean as possible and lives in `lexer.py`. It loops through all characters in the input following the transitions defined in the state table. I used the `.get` method to look up the next state, which returns gracefully if there is no transition in the current state matching the current character. If it transitions to another state, it tries to access the the type of token accepeted at this state. If this state is not accepting, `.get` returns None and it loops. This process continues until there are no transitions left to make. If we have encoutered an accepting state, we create and store the token and reset the state variables to process the rest of the input.
