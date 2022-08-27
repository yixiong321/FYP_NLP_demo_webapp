import spacy
import stanza
from nltk.tokenize import word_tokenize
import spacy_stanza
from os.path import exists
import os
from spacy.tokens import Doc
import nltk
import benepar
import ssl
from nltk.parse import CoreNLPParser
from parse_tree import parse_tree
import random
## download the benepar model is required
#ssl._create_default_https_context = ssl._create_unverified_context
#benepar.download('benepar_en3')
nlp_spacy = spacy.load("en_core_web_sm")
nlp_spacy.add_pipe("benepar", config={"model": "benepar_en3"})

#stanza.download("en",model_dir='stanza_resources')
file_exists = exists('stanza_resources/resources.json')
if file_exists:
    #nlp_stanza = spacy_stanza.load_pipeline("en",download_method=None)
    nlp_stanza = stanza.Pipeline(lang='en',dir='stanza_resources',download_method=None,verbose=False)
    #print('No download')
else:
    print('Downloading Stanza models')
    os.mkdir('stanza_resources')
    nlp_stanza = stanza.Pipeline(lang='en',dir='stanza_resources')

# Tokenization
def get_nltk_tokens(text):
    nltk_tokens = word_tokenize(text)
    return nltk_tokens
def get_nltk_tokens_corenlp(text):
    parser = CoreNLPParser(url='http://localhost:9000')
    tokens=[]
    tokens=list(parser.tokenize(text))
    return tokens
def get_spacy_tokens(text):
    spacy_doc = nlp_spacy(text)
    spacy_tokens = []
    for token in spacy_doc:
        spacy_tokens.append(token.text)
    return spacy_tokens
def get_stanza_tokens(text):
    stanza_doc = nlp_stanza(text)
    stanza_tokens = []
    for sent in stanza_doc.sentences:
        for token in sent.tokens:
            stanza_tokens.append(token.text)
    return stanza_tokens

#POS-tagging
def get_nltk_pos_tags(text):
    nltk_doc = word_tokenize(text)
    #nltk_tokens=[]
    nltk_pos_tags=[]
    for token in nltk_doc:
        #nltk_tokens.append(nltk.pos_tag([token])[0][0])
        #using the universal tagset
        nltk_pos_tags.append((nltk.pos_tag([token])[0][0],nltk.pos_tag([token], tagset='universal')[0][1]))
    return {
        #'NLTK_tokens':nltk_tokens,
        'NLTK_POS':nltk_pos_tags}
def get_nltk_pos_tags_corenlp(text):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    #tokens=get_nltk_pos_tags_corenlp(text)
    nltk_pos_tags=[]
    pos = list(pos_tagger.tag(text.split()))
    for x in pos:
        nltk_pos_tags.append(x)
    return {
        #'nltk_corenlp_tokens':tokens,
        'nltk_corenlp_POS':nltk_pos_tags}
def get_spacy_pos_tags(text):
    spacy_doc = nlp_spacy(text)
    #spacy_tokens=[]
    spacy_pos_tags=[]
    for token in spacy_doc:
        #spacy_tokens.append(token.text)
        spacy_pos_tags.append((token.text,token.pos_))
    return {
        #'SpaCy_tokens':spacy_tokens,
        'SpaCy_POS':spacy_pos_tags}

def get_stanza_pos_tags(text):
    stanza_doc =nlp_stanza(text)
    #stanza_tokens=[]
    stanza_pos_tags=[]
    for i,sentence in enumerate(stanza_doc.sentences):
        for token in sentence.words:
            #stanza_tokens.append(token.text)
            stanza_pos_tags.append((token.text,token.upos))
    return {
        #'Stanza_tokens':stanza_tokens,
        'Stanza_POS':stanza_pos_tags}

def get_stanza_doc(text):
    doc = nlp_stanza(text) 
    data=[]
    for sent in doc.sentences:
        words=[]
        arcs=[]
        for token in sent.words:
            words.append({'text':token.text,'tag':token.upos,'id':token.id-1})
        #dependencies format List[(Word,str,Word)
        for rel in sent.dependencies:
            if rel[1] == 'root':
                continue
            token=rel[0]
            dep = rel[1]
            head=rel[-1]

            if token.id<head.id:
                dir = 'left'
            if token.id>head.id:
                dir = 'right'
            if token.id!=head.id:
                arcs.append({'start': token.id-1, 'end': head.id-1, 'label': dep, 'dir': dir})
        data.append({'words':words,'arcs':arcs})
    return data
    
def get_spacy_doc(text):
    doc= nlp_spacy(text)
    data=[]
    sent_end=0 # this is to mark the end of the sentence so that the arcs can be drawn starting from index 0
    for sent in doc.sents:
        words=[]
        arcs=[]
        
        for x in sent:
            #print(x.text,x.pos_,x.tag_,x.dep_,x.head,x.head.i,x.i)
            adr= x.i
            head=x.head.i
            words.append({'text':x.text,'tag':x.pos_,'id':x.i-sent_end})
            if adr<head:
                dir='left'
            if adr>head:
                dir='right'
            if x.dep_!='ROOT':
                arcs.append({'start':x.i-sent_end,'end':x.head.i-sent_end,'label':x.dep_,'dir':dir})
            if x.is_sent_end:
                sent_end=x.i+1
        data.append({'words':words,'arcs':arcs})
    
    return data



def recursiveStanza(layer):
    #stopping condition
    if len(layer.children)==0:
        return {'name':layer.label}
    else:
        lol={'name':layer.label,'children':[]}
        for x in range(len(layer.children)):
                lol['children'].append(recursiveStanza(layer.children[x]))
        return lol

def stanzaConverter(text):
    doc=nlp_stanza(text)
    for i,sentence in enumerate(doc.sentences):
        tree = sentence.constituency
        #print(sentence.constituency)
        res=recursiveStanza(tree)
        #print(res)
        key=str(random.randint(0, 100))+str(random.randint(0, 100))
        parse_tree(res,style={ 'width': '100em', 'height': '20em','background':'white'},key=key)
        

def recursiveBenepar(layer):
    #stopping condition
    #print(layer,layer._.labels,list(layer._.children),layer._.parse_string)
    if list(layer._.children)==[]:
        if len(layer._.labels)==0:
            strs=layer._.parse_string.replace('(','').replace(')','')
            strslist=strs.split()
            return {'name':strslist[0],'children':[{'name':strslist[1]}]}
        else:
            strs=layer._.parse_string.replace('(','').replace(')','')
            strslist=strs.split()
            return {'name':strslist[0],'children':[{'name':strslist[1],'children':[{'name':strslist[-1]}]}]}
    else:
        lol={'name':layer._.labels,'children':[]}
        for x in range(len(list(layer._.children))):
            lol['children'].append(recursiveBenepar(list(layer._.children)[x]))
        return lol

def spacy_benepar(text):
    doc=nlp_spacy(text)
    for sentence in list(doc.sents):
        res=recursiveBenepar(sentence)
        #print(res)
        key=str(random.randint(0, 100))+str(random.randint(0, 100))
        parse_tree(res,style={ 'width': '100em', 'height': '20em','font-size':'large','background':'white'},key=key)
        #print(sentence.constituents)




        

