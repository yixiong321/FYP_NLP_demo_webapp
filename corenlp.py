from nltk.parse import CoreNLPParser
import nltk
from nltk.tree import Tree
import parse_tree
from parse_tree import parse_tree
import random
def recursive_nltk_tree_traversal(tree):
    if(type(tree)==str):
        return {'name':tree}
    format={'name':tree.label(),'children':[]}
    for x in range(len(tree)):
        #print(tree[x])
        format['children'].append(recursive_nltk_tree_traversal(tree[x]))
    return format

def constituency_corenlp(text):
    parser = CoreNLPParser(url='http://localhost:9000')
    sents=parser.parse_text(text) # returns iter(Trees)
    for sent in sents:
        result=recursive_nltk_tree_traversal(sent)
        key=str(random.randint(0, 100))+str(random.randint(0, 100))
        parse_tree(result,style={ 'width': '100em', 'height': '20em','background':'white'},key=key)
    
        
#print(constituency_corenlp('i like this tree.'))


        

#example=Tree.fromstring('(ROOT(NP (NP (PRP i)) (PP (IN like) (NP (DT this) (NN tree))) (. .)))')
#ok=recursive_nltk_tree_traversal(example)
#ok=traverse_tree(example)
#print(ok)
