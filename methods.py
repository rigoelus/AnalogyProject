import gensim
import nltk
from gensim.models import Word2Vec
from nltk.corpus import gutenberg
from nltk.corpus import brown
from scipy import spatial
import numpy as np


#gutenberg2 = Word2Vec(gutenberg.sents(), iter=10, min_count=25, size=500, workers=4, sg=1)
brown1 = Word2Vec(brown.sents(), iter=10, min_count=5, size=500, workers=4, sg=0)

def getVector(model, word):
    if word in model.wv.vocab:
        return model.wv[word]
    return np.zeros(model.vector_size)

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

def Vanilla2Blank(pairVector1, pairVector2, choiceArray):
    best_vector = pairVector1 - pairVector2
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1[1], best_vector + vector1[0])
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def OnlyBlank2Blank(pairVector1, pairVector2, choiceArray):
    best_vector = pairVector1 - pairVector2
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1[1], vector1[0])
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def Ignore2Blank(pairVector1, pairVector2, choiceArray):
    best_vector = pairVector2
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1[1], best_vector + vector1[0])
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

def AddOpposite2Blank(pairVector1, pairVector2, choiceArray):
    best_vector = pairVector2 - pairVector1
    def cosine_sim(vector1):
        return 1 - spatial.distance.cosine(vector1[1], best_vector + vector1[0])
    sim_list = list(map(cosine_sim, choiceArray))
    return sim_list.index(max(sim_list))

print(Vanilla1Blank(brown1.wv['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(OnlyBlank1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(Ignore1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(AddOpposite1Blank(brown1['train'], brown1['board'], brown1['horse'], [brown1['stable'], brown1['shoe'], brown1['ride'], brown1['mount']]))
print(Vanilla2Blank(brown1['medicine'], brown1['illness'], [[brown1['law'], brown1['anarchy']], [brown1['hunger'], brown1['sad']], [brown1['love'], brown1['treason']], [brown1['ride'], brown1['shoe']]]))
print(OnlyBlank2Blank(brown1['medicine'], brown1['illness'], [[brown1['law'], brown1['anarchy']], [brown1['hunger'], brown1['sad']], [brown1['love'], brown1['treason']], [brown1['ride'], brown1['shoe']]]))
print(Ignore2Blank(brown1['medicine'], brown1['illness'], [[brown1['law'], brown1['anarchy']], [brown1['hunger'], brown1['sad']], [brown1['love'], brown1['treason']], [brown1['ride'], brown1['shoe']]]))
print(AddOpposite2Blank(getVector(brown1,'medicine'), getVector(brown1,'illness'), [[getVector(brown1,'law'), getVector(brown1,'anarchy')], [getVector(brown1,'hunger'), getVector(brown1,'sad')], [getVector(brown1,'love'), getVector(brown1,'treason')], [getVector(brown1,'ride'), getVector(brown1,'shoe')]]))