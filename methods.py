import gensim
import nltk
from gensim.models import Word2Vec
from nltk.corpus import gutenberg
from nltk.corpus import brown
from scipy import spatial


#gutenberg2 = Word2Vec(gutenberg.sents(), iter=10, min_count=25, size=500, workers=4, sg=1)
brown1 = Word2Vec(brown.sents(), iter=10, min_count=5, size=500, workers=4, sg=0)

def Vanilla1Blank(pairVector1, pairVector2, blankVector1, choiceArray):
    best_vector = pairVector1 - pairVector2 + blankVector1
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1, best_vector)
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def OnlyBlank1Blank(pairVector1, pairVector2, blankVector1, choiceArray):
    best_vector = blankVector1
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1, best_vector)
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def Ignore1Blank(pairVector1, pairVector2, blankVector1, choiceArray):
    best_vector = pairVector2 + blankVector1
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1, best_vector)
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def AddOpposite1Blank(pairVector1, pairVector2, blankVector1, choiceArray):
    best_vector = blankVector1 - pairVector1 + pairVector2
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1, best_vector)
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

print(Vanilla1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(OnlyBlank1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(Ignore1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(AddOpposite1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
