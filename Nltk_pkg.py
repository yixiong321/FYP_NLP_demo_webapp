import nltk
from nltk.tokenize import word_tokenize
from nltk.parse import malt
from parse_tree import parse_tree
from nltk.tokenize import sent_tokenize, word_tokenize
import random
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import WhitespaceTokenizer
import nltk.data
from nltk.tokenize import RegexpTokenizer
class NLTK_pkg():
    def __init__(self,parser,pos_tagger):
        self.parser = parser
        self.pos_tagger = pos_tagger
    def set_text(self,text):
        self.text = text

    def nltk_word_tokenize(self):
        sents = sent_tokenize(self.text)
        tokens = {}
        for i,sent in enumerate(sents):
            tokens[str(i+1)]=[]
            for token in word_tokenize(sent):
                tokens[str(i+1)].append(token)
        return tokens , len(sents)

    def nltk_wordpunct_tokenize(self):
        sents = sent_tokenize(self.text)
        tokens = {}
        for i,sent in enumerate(sents):
            tokens[str(i+1)]=[]
            for token in wordpunct_tokenize(sent):
                tokens[str(i+1)].append(token)
        return tokens
       
        
    def nltk_treeback_tokenize(self):
        sents = sent_tokenize(self.text)
        tokens = {}
        for i,sent in enumerate(sents):
            tokens[str(i+1)]=[]
            for token in TreebankWordTokenizer().tokenize(sent):
                tokens[str(i+1)].append(token)
        return tokens
        
        

    def nltk_whitespace_tokenize(self):
        sents = sent_tokenize(self.text)
        tokens = {}
        for i,sent in enumerate(sents):
            tokens[str(i+1)]=[]
            for token in WhitespaceTokenizer().tokenize(sent):
                tokens[str(i+1)].append(token)
        return tokens
        

    def nltk_regexp_tokenize(self):
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        sents = sent_tokenize(self.text)
        tokens={}
        for i,sent in enumerate(sents):
            tokens[str(i+1)]=[]
            for token in tokenizer.tokenize(sent):
                tokens[str(i+1)].append(token)
        return tokens

    def get_nltk_tokens_corenlp(self):
        tokens={}
        parsed_data = self.parser.api_call(self.text,properties={"annotators": "tokenize,ssplit"})
        for i,sentence in enumerate(parsed_data['sentences']):
            tokens[str(i+1)]=[]
            for token in sentence["tokens"]:
                tokens[str(i+1)].append(token["originalText"] or token["word"])
        return tokens ,len(parsed_data['sentences'])

    def get_nltk_pos_tags(self):
        #nltk_doc = word_tokenize(self.text)
        sents = sent_tokenize(self.text)
        nltk_pos_tags={}
        for index,sent in enumerate(sents):
            nltk_pos_tags[str(index+1)] = []
            txt = word_tokenize(sent)
            nltk_pos_tags[str(index+1)] = nltk.pos_tag(txt,tagset='universal')
        return nltk_pos_tags

    def get_nltk_pos_tags_corenlp(self):
        tagged_data = self.parser.api_call(self.text,properties={"annotators": "tokenize,ssplit,pos"})
        nltk_pos_tags_core = {}
        for sentence in tagged_data['sentences']:
            key = str(sentence['index']+1)
            nltk_pos_tags_core[key] = []
            for token in sentence['tokens']:
                nltk_pos_tags_core[key].append((token["word"],token["pos"]))
        return nltk_pos_tags_core

    def get_maltparser_res(self):
        mp = malt.MaltParser(parser_dirname='maltparser-1.9.2',model_filename='engmalt.poly-1.7.mco') 
        em=[]
        sentences=[]
        for x in sent_tokenize(self.text):
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
                            "end":token['head']-1,
                            "label":token['rel'],
                            "dir":"left"})
                    elif token['address']>token['head']:
                        arcs_input.append(
                            {"start":token['head']-1,
                            "end":token['address']-1,
                            "label":token['rel'],
                            "dir":"right"})
            sentences_list.append({'words':words_input,'arcs':arcs_input})
        return sentences_list

    def recursive_nltk_tree_traversal(self,tree):
        if(type(tree)==str):
            return {'name':tree}
        format={'name':tree.label(),'children':[]}
        for x in range(len(tree)):
            format['children'].append(self.recursive_nltk_tree_traversal(tree[x]))
        return format

    def constituency_corenlp(self):
        sents=self.parser.parse_text(self.text) # returns iter(Trees)
        for sent in sents:
            result=self.recursive_nltk_tree_traversal(sent)
            key=str(random.randint(0, 100))+str(random.randint(0, 100))
            parse_tree(result,style={ 'width': '100em', 'height': '20em','background':'white'},key=key)