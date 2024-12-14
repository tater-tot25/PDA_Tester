# PDA_Tester
A python script that can generate Initialize and simulate PDAs, as well as Hueristically test them to see if they accept every string in the alphabet

# Instructions

  * Define a dictionary of transitions, I have some demonstrated in the file, they should be of the form ("startingState", "transitionSymbol", "symbolToPop") : ("endingState", "symbolToPush")
  * Define a list of start function, a string
  * Define a list of accept states i.e. \["q1", "q2"] etc.
  * call the PDA constructor with PDA(acceptState, startState, transitions)
  * use the .testPDA(listOfTestStrings) to test multiple strings or .run(string) for one string
  * OPTIONALY: use the function acceptsAllStrings(pda, verbose = False) to Hueristically check if the PDA can accept all strings in the alphabet, you can use the function acceptsAllStringsHandler(pda, verbose = false) to have it print messages for you
