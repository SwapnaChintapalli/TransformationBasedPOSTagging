class Token:
    word = None
    correctTag = None
    currentTag = None
    lineNum = None

    def __init__(self, word, correctTag, lineNum):
        self.word = word
        self.correctTag = correctTag
        self.lineNum = lineNum
    

def unigramProb(tokens):
    token_count = {}
    pos_count = {}
    
    for token in tokens:
        token_count[token.word] = token_count.get(token.word, 0) + 1
        if token.word not in pos_count:
            pos_count[token.word] = {}
            
        pos_count[token.word][token.correctTag] = pos_count[token.word].get(token.correctTag, 0) + 1
    
    pos_prob = {}
    
    for word, wordPosCounts in pos_count.items():
        for pos, posCount in wordPosCounts.items():
            
            if word not in pos_prob:
                pos_prob[word] = {}
                
            pos_prob[word][pos] = posCount/token_count[word]
            
    return pos_prob


def get_best_instance(tokens):
    fromtags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT",
                "POS", "PRP",
                "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT",
                "WP", "WP$", "WRB",
                "$", "#", "(", ")", ",", ".", ":", """, """]
    totags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT",
              "POS", "PRP",
              "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP",
              "WP$", "WRB",
              "$", "#", "(", ")", ",", ".", ":", """, """]
    bestRule = None
    for fromTag in fromtags:
        for toTag in totags:
            if fromTag == toTag:
                continue
            counts = {}
            max_tag = None
            max_count = 0
            for index, token in enumerate(tokens):
                
                if index == 0:
                    continue
                if tokens[index-1].lineNum != tokens[index].lineNum:
                    continue
                if (token.currentTag == fromTag and token.correctTag == toTag):
                    counts[tokens[index-1].currentTag] = counts.get(tokens[index-1].currentTag, 0) + 1
                elif (token.currentTag == fromTag and token.correctTag == fromTag):
                    counts[tokens[index-1].currentTag] = counts.get(tokens[index-1].currentTag, 0) - 1
                    
                if counts.get(tokens[index-1].currentTag) and (max_tag == None or counts[tokens[index-1].currentTag] > max_count):
                    max_tag = tokens[index-1].currentTag
                    max_count = counts.get(tokens[index-1].currentTag)
                    
            if bestRule == None or bestRule['count'] < max_count:
                bestRule = {
                "fromTag" : fromTag, 
                "toTag" : toTag, 
                "context" : max_tag,
                "count" :max_count}
    
    return bestRule


def readFromFile():
    tokens = []
    with open('./NLP6320_POSTaggedTrainingSet-Windows.txt', 'r') as myfile:
        data = myfile.read()

    lines = data.split("\n")
    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            root, pos = word.split("_")
            token = Token(root.lower(), pos, i)
            tokens.append(token)
    return tokens


def maxPosProb(pos_prob):
    max_prob_pos = {}
    for word, wordPOSProb in pos_prob.items():
        maxProb = 0
        maxPos = None
        for pos, prob in wordPOSProb.items():
            if (prob > maxProb):
                maxProb = prob
                maxPos = pos

        max_prob_pos[word] = maxPos
    return max_prob_pos


def BrillsPOSTagging():
    tokens = readFromFile()
    pos_prob = unigramProb(tokens)
    max_prob_pos = maxPosProb(pos_prob)

    for token in tokens:
        token.currentTag = max_prob_pos[token.word]

    topRules = []
    while len(topRules) <= 10:
        rule = get_best_instance(tokens)
        for index, token in enumerate(tokens):
            if index == 0:
                continue

            if token.currentTag == rule['fromTag'] and tokens[index - 1].currentTag == rule['context']:
                token.currentTag = rule['toTag']
	topRules.append(rule)
    file1 = open("brillsRules.txt", "w")
    file1.write("FromTag" + "\t\t\t" + "ToTag" + "\t\t\t" + "Condition" + "\t\t\t" + "Score" + "\n")
    for rule in topRules:
        file1.write(
            str(rule['fromTag']) + "\t\t\t" + str(rule['toTag']) + "\t\t\t" + str(rule['context']) + "\t\t\t" + str(
                rule['count']) + "\n")
