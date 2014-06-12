import civimain
import math
__author__ = 'Francesco'


def cosineSimilarity(tweetID1, tweetID2):
    civimain.initIDFCollection()
    words1 = civimain.tfidf(tweetID1)
    words2 = civimain.tfidf(tweetID2)

    keys1 = words1.keys()
    keys2 = words2.keys()

    commonWords = set(keys1) & set(keys2)
    num = sum([words1[value] * words2[value] for value in commonWords])

    #somme al quadrato
    sumDoc1 = sum([math.pow(words1[value], 2) for value in keys1])
    sumDoc2 = sum([math.pow(words2[value], 2) for value in keys2])
    den = math.sqrt(sumDoc1) * math.sqrt(sumDoc2)
    result = 0

    try:
        return float(num) / den
    except Exception:
        return 0.0

