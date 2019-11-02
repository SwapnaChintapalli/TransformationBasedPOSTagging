def computeProb():
    unigramList = {}
    unigramTags = {}
    word_given_tag = {}
    bigramTagsList = {}
    tagi_given_tagi1 = {}
    file_name = "./NLP6320_POSTaggedTrainingSet-Windows.txt"
    file = open(file_name, "r")

    for line in file.readlines():
        data = []
        words = line.lower().split()
        for i in range(0, len(words)):
            words_split = words[i].split('_')
            data.append((words_split[0],words_split[1]))


        for tag in data:
            if tag[1] in unigramTags:
                unigramTags[tag[1]] += 1
            else:
                unigramTags[tag[1]] = 1

            if tag not in unigramList:
                unigramList[tag] = 1
            else:
                unigramList[tag] += 1

        for i in range(1,len(data)):
            pair = (data[i][1], data[i-1][1])
            if pair in bigramTagsList:
                bigramTagsList[pair] += 1
            else:
                bigramTagsList[pair] = 1

    output1 = open('word_given_tag.txt', 'w')
    output1.write('Word' + '\t\t' + 'Tag' + '\t\t' + 'Probability' + '\n')

    for unigram in unigramList:
        word_given_tag[unigram] = unigramList.get(unigram) / unigramTags.get(unigram[1])
        output1.write(str(unigram[0])+"\t"+str(unigram[1])+"\t\t"+str(word_given_tag[unigram])+"\n")

    output2 = open('tagi_given_tagi1.txt','w')
    output2.write('Tag(i)'+'\t\t'+'Tag(i-1)'+'\t\t'+'Probability'+'\n')

    for tag in bigramTagsList:
        tagi_given_tagi1[tag] = bigramTagsList.get(tag) / unigramTags.get(tag[1])
        output2.write(str(tag[0])+'\t\t'+str(tag[1])+'\t\t'+str(tagi_given_tagi1[tag])+'\n')

    output1.close()
    output2.close()
    return word_given_tag, tagi_given_tagi1


def NaiveBayesianFunc():
    word_given_tag, tagi_given_tagi1 = computeProb()