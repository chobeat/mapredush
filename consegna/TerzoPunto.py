import main.py

__author__ = 'Francesco'

def timelineSimilarity(timeline1, timeline2, threshold):

    listatweet1 = main.timeline2tweets(timeline1)
    listatweet2 = main.timeline2tweets(timeline2)

    if len(listatweet1) <= len(listatweet2):
        result = computeDice(listatweet1, listatweet2, threshold)
    else:
        result = computeDice(listatweet2, listatweet1, threshold)


def computeDice(listatweet1, listatweet2, threshold):
    counter = 0
    for tweet1 in listatweet1:
        for tweet2 in listatweet2:
            if main.cosineSimilarity(tweet1, tweet2) >= threshold:
                counter += 1

    return (float(2 * counter))/(len(listatweet1) + len(listatweet2))





