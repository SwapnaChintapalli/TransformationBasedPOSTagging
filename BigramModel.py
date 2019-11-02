def BigramModel():
    bigramsList = []
    bigramCounts = {}
    unigramCounts = {}
    unigramsList = []
    file_name = "./NLP6320_POSTaggedTrainingSet-Windows.txt"
    file = open(file_name, "r")

    for line in file.readlines():
        data = []
        for word in line.split():
            word_split = word.lower().split('_')
            data.append(word_split[0])

        for i in range(len(data)-1):
            bigramsList.append((data[i],data[i+1]))
            unigramsList.append(data[i])
            if i== len(data) -2:
                unigramsList.append(data[i+1])
            if (data[i],data[i+1]) in bigramCounts:
                bigramCounts[(data[i],data[i+1])] += 1
            else:
                bigramCounts[(data[i],data[i+1])] = 1

            if data[i] in unigramCounts:
                unigramCounts[data[i]] += 1
            else:
                unigramCounts[data[i]] = 1

            if i==len(data) -2:
                if data[i+1] in unigramCounts:
                    unigramCounts[data[i+1]] += 1
                else:
                    unigramCounts[data[i+1]] = 1
    file.close()

    return bigramsList,bigramCounts,unigramCounts,unigramsList

def bigramProbabilities(bigramsList,bigramCounts,unigramCounts):
    bigramProb = {}

    for bigram in bigramsList:
        data1 = bigram[0]
        data2 = bigram[1]

        bigramProb[bigram] = (bigramCounts.get(bigram,0) / unigramCounts.get(data1))

    file = open('BigramProbability.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Probability' + '\n')

    for bigrams in set(bigramsList):
        file.write(str(bigrams) + ' : ' + str(bigramProb[bigrams]) + '\n')

    file.close()
    return bigramProb

def addOneSmoothing(bigramsList,bigramCounts,unigramCounts):
    bigramProb = {}
    cstar = {}

    for bigram in bigramsList:
        data1 = bigram[0]
        data2 = bigram[1]

        cstar[bigram] = (bigramCounts[bigram] + 1) * unigramCounts[data1] / (unigramCounts[data1] + len(unigramCounts))
        bigramProb[bigram] = (bigramCounts.get(bigram) + 1) / (unigramCounts.get(data1) + len(unigramCounts))

    BProb = {}
    cstar1 = {}
    file = open('AddOneSmoothing.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Cstar'+ '\t\t' +'Probability' + '\n')

    for data1, v1 in unigramCounts.items():
        for data2, v2 in unigramCounts.items():
            bigram = (data1,data2)

            BProb[bigram] = (bigramCounts.get(bigram, 0) + 1) / (unigramCounts.get(data1) + len(unigramCounts))
            cstar1[bigram] = (bigramCounts.get(bigram, 0) + 1) * unigramCounts[data1] / (unigramCounts[data1] + len(unigramCounts))
            file.write(str(bigram) + ' : ' + str(cstar1[bigram]) + ' : ' + str(BProb[bigram]) + '\n')
    file.close()
    return bigramProb, cstar


def goodTuring( bigramCounts, unigramCounts):
    bucket = {}
    cstar = {}
    pstar = {}
    goodTuring1 = {}
    total_bigramSum = 0
    for i in bigramCounts:
        total_bigramSum += bigramCounts[i]

    file = open('goodTuringDiscounting.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Cstar' + '\t\t' + 'Probability' + '\n')

    for bigram in bigramCounts.items():
        key = bigram[0]
        value = bigram[1]

        if not value in bucket:
            bucket[value] = 1
        else:
            bucket[value] += 1

    for data1 in unigramCounts:
        for data2 in unigramCounts:
            bigram1 = (data1, data2)

            count = bigramCounts.get(bigram1,0)
            if count == 0:
                pstar[bigram1] = bucket[1] / total_bigramSum
                cstar[bigram1] = bucket[1]
            else:
                cstar[bigram1] = (count + 1)*bucket.get(count+1,0)/bucket[count]
                pstar[bigram1] = count/total_bigramSum
            goodTuring1[bigram1] = (cstar[bigram1],pstar[bigram1])

    for k,v in goodTuring1.items():
        file.write(k+'\t\t\t'+v[0]+'\t\t'+v[1]+'\n')

    file.close()



def bigramModelFunc():
    bigramsList, bigramCounts, unigramCounts,unigramsList = BigramModel()
    bigramProbability = bigramProbabilities(bigramsList, bigramCounts, unigramCounts)
    bigramAddOne, cstar = addOneSmoothing(bigramsList, bigramCounts, unigramCounts)
    goodTuring(bigramCounts, unigramCounts)


