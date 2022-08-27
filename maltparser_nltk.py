from spacy.tokens import Doc
import nltk
import warnings
from nltk.parse import malt
mp = malt.MaltParser(parser_dirname='maltparser-1.9.2',model_filename='engmalt.poly-1.7.mco') 
from nltk.tokenize import sent_tokenize, word_tokenize


def get_maltparser_res(text):
    em=[]
    sentences=[]
    for x in sent_tokenize(text):
        em.append(x)
        sentences.append(word_tokenize(x))
    sentences_list=[]

    for index,sentence in enumerate(sentences):
        node_list=[]
        words_input=[]
        arcs_input=[]
        depTree=mp.parse_one(sentence)
        max=len(depTree.nodes)
        node_list.append(depTree.nodes)

        for nodes in node_list:
            for x in range(1,max):
                token = nodes[x]
                words_input.append(
                    {"text":token['word'],
                    "tag":token['tag'],
                    'id':token['address']-1})
                if token['rel']=='null':
                    continue
                if token['address']<token['head']:       
                    arcs_input.append(
                        {"start":token['address']-1,
                        "end":token['head']-1 ,
                        "label":token['rel'] ,
                        "dir":"left"})
                elif token['address']>token['head']:
                    arcs_input.append({"start":token['head']-1,"end":token['address']-1 , "label":token['rel'] ,"dir":"right"})
        sentences_list.append({'words':words_input,'arcs':arcs_input})
    return sentences_list


