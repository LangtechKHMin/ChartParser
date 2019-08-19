from SentParser import SentParser

S = ["The university sent me a letter of apology.",
    "The box was so heavy that she could not carry it.",
    "Her mother didn't permit her to go out late at night.",
    "Those dolls looks as if they were alive.",
    "The house looks nicer than the one next to it.",
    "If I had not fooled around,I could have graduated sooner.",
    "The palace is one of the oldest buildings in Korea.",
    "There is a man who is very energetic.",
    "It is dangerous for children to play soccer in the street.",
    "What a big bag it is!",
    "Study hard and you will pass the next bar exam.",
    "What would you like to choose?",
    "Could you show me the way to City Hall?",
    "I don't know whether to take an exam.",
    "That is the reason that I tried to reach you."]

parser = SentParser(S[0], ".\\grammar.cfg")
parser.tokenize()

parser.cfgReader()

parser.ChartInit()
parser.ChartFeed()
parser.ChartFinal()

for n in parser.finals:
    print(n)
#print(parser.tokens)
#print(parser.TMR)
#print(parser.NTR)
#parser.ChartShow()
