import spacy
import random
from parse_tree import parse_tree
import benepar
import ssl
import streamlit as st
from spacy.tokens import Doc
## download the benepar model is required
#ssl._create_default_https_context = ssl._create_unverified_context
#benepar.download('benepar_en3')
#nlp_spacy = spacy.load("en_core_web_sm")
#nlp_spacy.add_pipe("benepar", config={"model": "benepar_en3"})

class Spacy_pkg:
    def __init__(self,model):
        self.nlp_spacy = model
    def set_doc(self,text):
        self.doc = self.nlp_spacy(text)
    def get_spacy_tokens(self):
        spacy_tokens = {}
        sents = list(self.doc.sents)
        for i in range(len(sents)):
            spacy_tokens[str(i+1)]=[]
            for token in sents[i]:
                spacy_tokens[str(i+1)].append(token.text)
        return spacy_tokens,len(sents)
    def get_spacy_pos_tags(self):
        spacy_pos_tags={}
        sents = list(self.doc.sents)
        for i in range(len(sents)):
            spacy_pos_tags[str(i+1)] = []
            print(sents[i])
            for token in sents[i]:
                spacy_pos_tags[str(i+1)].append((token.text,token.pos_))
        return spacy_pos_tags
    
    def convert_for_dep_parsing(self):
        data=[]
        sent_end=0 # this is to mark the end of the sentence so that the arcs can be drawn starting from index 0
        for sent in self.doc.sents:
            words=[]
            arcs=[]
            for x in sent:
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
    def recursiveBenepar(self,layer):
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
                lol['children'].append(self.recursiveBenepar(list(layer._.children)[x]))
            return lol
    
    def visualise_spacy_benepar_const_parsing(self):
        for sentence in list(self.doc.sents):
            res=self.recursiveBenepar(sentence)
            #print(res)
            key=str(random.randint(0, 100))+str(random.randint(0, 100))
            parse_tree(res,style={ 'width': '100em', 'height': '20em','font-size':'large','background':'white'},key=key)
            #print(sentence.constituents)

