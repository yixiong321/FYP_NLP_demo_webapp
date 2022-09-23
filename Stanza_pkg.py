from os.path import exists
import random
from parse_tree import parse_tree
from dep_parsing_component import dep_parsing_component
import streamlit as st
class Stanza_pkg():
    def __init__(self,model):
        self.nlp_stanza = model

    def set_doc(self,text):
        self.doc = self.nlp_stanza(text)

    def get_stanza_tokens(self):
        stanza_doc = self.doc
        stanza_tokens = {}
        
        for i,sent in enumerate(stanza_doc.sentences):
            stanza_tokens[str(i+1)]= []
            for token in sent.tokens:
                stanza_tokens[str(i+1)].append(token.text)
        return stanza_tokens, len(stanza_doc.sentences)

    def get_stanza_pos_tags(self):
        stanza_doc =self.doc
        #stanza_tokens=[]
        stanza_pos_tags={}
        for i,sentence in enumerate(stanza_doc.sentences):
            stanza_pos_tags[str(i+1)]= []
            for token in sentence.words:
                #stanza_tokens.append(token.text)
                stanza_pos_tags[str(i+1)].append((token.text,token.upos))
            
        return stanza_pos_tags
    # convert dep tree in standardised format
    def convert_for_stanza_dep_parsing(self):
        doc = self.doc
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

    
    # to convert the consti tree to standard format
    def recursiveStanza(self,layer):
        #stopping condition
        if len(layer.children)==0:
            return {'name':layer.label}
        else:
            lvl={'name':layer.label,'children':[]}
            for x in range(len(layer.children)):
                    lvl['children'].append(self.recursiveStanza(layer.children[x]))
            return lvl
    
    # feed data to visualisation comp for constituency parsing
    def visualise_stanza_consti_parsing (self):
        doc=self.doc
        for i,sentence in enumerate(doc.sentences):
            tree = sentence.constituency
            #print(sentence.constituency)
            res=self.recursiveStanza(tree)
            #print(res)
            key=str(random.randint(0, 100))+str(random.randint(0, 100))
            parse_tree(res,style={ 'width': '100em', 'height': '20em','background':'white'},key=key)