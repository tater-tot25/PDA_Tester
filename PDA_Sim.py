import random

class PDA:
    def __init__(self, acceptStates, startState, transitions):
        turnOffInfinteChecker = True #Just here for challenge activity 11
        self.acceptStates = acceptStates
        self.startState = startState
        self.transitions = transitions
        if not turnOffInfinteChecker: self.checkForInfinateLoop()
        
    def checkForInfinateLoop(self, returnValues = False): #function for preventing PDAs that have infinite loops
        allKeys = self.transitions.keys()
        for key in allKeys:
            if (key[1] == "ε" and key[2] == "ε"):
                tempVal = self.transitions[key]
                if(tempVal[1] == "ε" and key[0] == tempVal[0]): #we have a transition: ε, ε -> ε qN -> qN, which would cause an infinite loop
                    if not returnValues: 
                        raise ValueError("Transition Function has the form ε, ε -> ε, where qN transitions to qN. This is an infinite loop")
                    else:
                        return True #There was an infinite loop
        
    def run(self, inputString): #our main function to call our pda on an input string
        stack = []
        return self.recursive_helper(inputString, stack, self.startState)
        
    def recursive_helper(self, inputString, stack, currentState): #the main logic of the program
        # Base case where it accepts
        if (len(inputString) == 0 and currentState in self.acceptStates):
            return True
        
        topOfStack = stack[-1] if len(stack) > 0 else "ε"
        inputSymbol = inputString[0] if len(inputString) > 0 else "ε"
            
        keys = self.getPossibleKeys(currentState, topOfStack, inputSymbol) #get all transtition functions we can take
        
        for key in keys:  #run each transition function as a recursive call and pop/push change input string as needed
            newInputString = inputString
            newStack = stack[:]  # Create a copy of the stack
            todo = self.transitions[key]
            newCurrentState = todo[0]

            if key[2] != "ε" and len(newStack) != 0:  # Pop
                newStack = newStack[:-1]
            if todo[1] != "ε":  # Push the new symbol, if we want
                newStack.append(todo[1])  # Correctly append to newStack
            if key[1] != "ε" and len(newInputString) != 0:
                newInputString = newInputString[1:]
                
            # Run recursive call
            if self.recursive_helper(newInputString, newStack, newCurrentState):  # Ensure this is correctly checked
                return True  

        #This path is not in the language
        return False
        
        
    # Function that fetches all of the transition functions based on the state, input symbol, and stack
    def getPossibleKeys(self, currentState, topOfStack, inputSymbol):
        listOfPossibleKeys = []
        keyOne = (currentState, inputSymbol, "ε")  # (state, consume symbol, no pop)
        listOfPossibleKeys.append(keyOne)
        keyTwo = (currentState, "ε", topOfStack)  # (state, epsilon transition, pop)
        listOfPossibleKeys.append(keyTwo)
        keyThree = (currentState, "ε", "ε")  # (state, epsilon transition, no pop)
        listOfPossibleKeys.append(keyThree)
        keyFour = (currentState, inputSymbol, topOfStack)  # (state, consume symbol, pop)
        listOfPossibleKeys.append(keyFour)
        #after creating a list of all possible transition functions, check to see if it exists
        returnVal = []
        for key in listOfPossibleKeys:
            if key in self.transitions:
                returnVal.append(key)
        return returnVal
    
def testPDA(pda, testStrings):
    for string in testStrings:
        if pda.run(string):
            print(string, "is in the language")
        else:
            print(string, "is not in the language")

def acceptsAllStrings(pda,  verbose = False):
    """
    Attempts various heuristic methods to determine if the PDA accepts all strings
    numOfRandomStrings: How many random strings to test in the alphabet
    stringDepth: The longest length of strings to test with Brute Force string generation
    """
    numOfRandomStrings = 500
    stringDepth = 5

    if not pda.acceptStates: #There are no accepts states, obviously it can't accept all strings
        return False
    if pda.checkForInfinateLoop(True): #There is an infinite loop, and we cannot conclude that this machine halts
        return None
    if not pda.run(""): #Does it accept the empty string
        return False
    if not pda.transitions: #If it doesn't have a transition, even if the start state is the accept state it won't accept strings > empty
        return False

    alphabet = [] #right now the function only checks the alphabet provided, we could also check all unicode characters or something
    for key in pda.transitions.keys():  #This should collect the alphabet of the pda
        for symbol in key[1]: 
            if symbol != "ε" and alphabet.count(symbol) == 0:  # Ignore epsilon transitions.
                alphabet.append(symbol)
    if verbose: print(alphabet)

    for x in range(0, stringDepth + 1):  # Generate every possible combination of strings up to length `stringDepth`
        for i in range(len(alphabet) ** x):
            stringToTest = ""
            index = i 
            for n in range(x): 
                char_index = index % len(alphabet)  # Get the index of the current character.
                stringToTest = alphabet[char_index] + stringToTest  # Prepend the character
                index //= len(alphabet)  # Move to the next position in the string.
            if verbose: print(stringToTest)
            if not pda.run(stringToTest): return False # Test the generated string

    for i in range(numOfRandomStrings): # Extra Safety Net to check random strings
        length = random.randint(0, 200)
        random_string = ''.join(random.choice(alphabet) for _ in range(length))
        if verbose: print(random_string)
        if not (pda.run(random_string)):
            return False
    return True

def acceptsAllStringsHandler(pda, verbose = False):
    result = acceptsAllStrings(pda, verbose)
    if result:
        print ("This PDA accepts all strings")
    elif result == None:
        print ("Inconclusive")
    else:
        print ("This PDA does not accept all strings")
        
def main():
    """
    PDA ONE
    """
    print("The language where L = {a^n b^n | n >= 0}")
    transitions = { #The language where L = {a^n b^n | n >= 0}
        ("q0", "ε", "ε") : ("q1", "$"),  #(start state, input, pop) : (next state, push)
        ("q1", "a", "ε") : ("q1", "a"),
        ("q1", "ε", "ε") : ("q2", "ε"),
        ("q2", "b", "a") : ("q2", "ε"),
        ("q2", "ε", "$") : ("q3", "ε"),
        #("q0", "ε", "ε") : ("q0", "ε") #For testing if it catches an infinite loop
    }
    startState = "q0"
    acceptStates = ["q0", "q3"]
    pda = PDA(acceptStates, startState, transitions)
    # testStrings = ["", "ab", "aabb", "aaabbb", "abababab", "abcsb", "aaabb", "abbb"]
    # testPDA(pda, testStrings)
    acceptsAllStringsHandler(pda)
    """
    PDA TWO
    """
    print("The language where there are twice as many a's as b's")
    transitionsL2 = {
        ("q0", "ε", "ε") : ("q1", "$"), #ε, ε -> ε q0->q1
        ("q1", "a", "ε") : ("q1", "a"), #a, ε -> a q1->q1
        ("q1", "a", "b") : ("q1", "ε"), #a, b -> ε q1->q1
        ("q1", "b", "a") : ("q2", "ε"), #b, a -> ε q1->q2
        ("q1", "b", "ε") : ("q2", "b"), #b, ε -> b q1->q2
        ("q2", "ε", "ε") : ("q1", "b"), #ε, ε -> b q2->q1
        ("q2", "ε", "a") : ("q1", "ε"), #ε, a -> ε q2->q1
        ("q1", "ε", "$") : ("q3", "ε")  #ε, $ -> ε q1->q3
    }
    startStateL2 = "q0"
    acceptStatesL2 = ["q3"]
    pdaL2 = PDA(acceptStatesL2, startStateL2, transitionsL2)
    # testStringsL2 = ["", "ababaa", "aabbaa", "bbbaaaaaa", "bbaaa", "ab", "abba", "aaxxcccbbbb"]
    # testPDA(pdaL2, testStringsL2)
    acceptsAllStringsHandler(pdaL2)
    """
    PDA THREE
    """
    # L3 = {a^i b^j c^k | k = i+j}
    print("The language {a^i b^j c^k | k = i+j}")
    transitionsL3 = {
        ("q0", "ε", "ε") : ("q1", "$"),
        ("q1", "a", "ε") : ("q1", "a"),
        ("q1", "ε", "ε") : ("q2", "ε"),
        ("q2", "b", "ε") : ("q2", "b"),
        ("q2", "ε", "ε") : ("q3", "ε"),
        ("q3", "c", "a") : ("q4", "ε"),
        ("q3", "c", "b") : ("q4", "ε"),
        ("q4", "c", "a") : ("q4", "ε"),
        ("q4", "c", "b") : ("q4", "ε"),
        ("q4", "ε", "$") : ("q5", "ε")
    }
    startStateL3 = "q0"
    acceptStatesL3 = ["q0", "q5"]
    pdaL3 = PDA(acceptStatesL3, startStateL3, transitionsL3)
    # testStringsL3 = ["", "aaabcccc", "abcc", "aaabbc", "aaaaaa", "cccc", "abc", "abbbcccc", "bc", "ac"]
    # testPDA(pdaL3, testStringsL3)
    acceptsAllStringsHandler(pdaL3)
    """
    PDA FOUR
    """
      # L4 = {(a|b|c)*} This one should pass accept all strings
    print("The language {(a|b|c)*}")
    transitionsL4 = {
        ("q0", "ε", "ε") : ("q1", "ε"),
        ("q0", "a", "ε") : ("q1", "ε"),
        ("q0", "b", "ε") : ("q1", "ε"),
        ("q0", "c", "ε") : ("q1", "ε"),
        ("q1", "a", "ε") : ("q1", "ε"),
        ("q1", "b", "ε") : ("q1", "ε"),
        ("q1", "c", "ε") : ("q1", "ε")
    }
    startStateL4 = "q0"
    acceptStatesL4 = "q1"
    pdaL4 = PDA(acceptStatesL4, startStateL4, transitionsL4)
    acceptsAllStringsHandler(pdaL4)
    """
    PDA FIVE
    """
    print("A language with an infinite loop")
    transitionsLInfinite = {
        ("q0", "ε", "ε") : ("q1", "ε"),
        ("q0", "a", "ε") : ("q1", "ε"),
        ("q1", "ε", "ε") : ("q1", "ε"),
        ("q1", "a", "ε") : ("q2", "ε"),
        ("q2", "a", "ε") : ("q2", "ε")
    }
    startStateLInfinite = "q0"
    acceptStatesLInfinite = "q2"
    pdaInfinite = PDA(acceptStatesLInfinite, startStateLInfinite, transitionsLInfinite)
    acceptsAllStringsHandler(pdaInfinite)

main()