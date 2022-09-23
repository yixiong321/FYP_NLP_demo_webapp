import token
import streamlit as st
from Spacy_pkg import Spacy_pkg
from Stanza_pkg import Stanza_pkg
from Nltk_pkg import NLTK_pkg
from dep_parsing_component import dep_parsing_component
from viz_tokens_component import viz_tokens_component as vz
import spacy
import os
import stanza
from os.path import exists
from nltk.parse import CoreNLPParser

@st.cache(allow_output_mutation=True)
def load_nltk_coreNLP(url):
    parser = CoreNLPParser(url=url)
    pos_tagger = CoreNLPParser(url=url, tagtype='pos')
    return parser,pos_tagger
@st.cache(allow_output_mutation=True)
def load_spacy_model(model_name):
    nlp_spacy = spacy.load(model_name)
    nlp_spacy.add_pipe("benepar", config={"model": "benepar_en3"})
    return nlp_spacy

@st.cache(allow_output_mutation=True)
def load_stanza_model(dir_name):
    file_exists = exists('stanza_resources/resources.json')
    if file_exists:
        nlp_stanza = stanza.Pipeline(lang='en',dir=dir_name,download_method=None,verbose=False)
        return nlp_stanza
    else:
        print('Downloading Stanza models for the first time...')
        os.mkdir('stanza_resources')
        nlp_stanza = stanza.Pipeline(lang='en',dir=dir_name)
        return nlp_stanza

st.set_page_config(layout="wide")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
inputs=st.container()
result=st.container()
if 'ready' not in st.session_state:
    st.session_state.ready = False
if "token" not in st.session_state:
    st.session_state.token = False
def handle_init_packages(packages_options,text):
    spacy_pkg=None
    stanza_pkg=None
    nltk_pkg=None
    if 'SpaCy' in packages_options:
        nlp_spacy = load_spacy_model("en_core_web_sm")
        spacy_pkg = Spacy_pkg(nlp_spacy)
        spacy_pkg.set_doc(text)
    if 'Stanza' in packages_options:
        nlp_stanza = load_stanza_model("stanza_resources")
        stanza_pkg = Stanza_pkg(nlp_stanza)
        stanza_pkg.set_doc(text)
    if 'NLTK' in packages_options:
        nltk_corenlp,pos_tagger = load_nltk_coreNLP('http://localhost:9000')
        nltk_pkg = NLTK_pkg(nltk_corenlp,pos_tagger)
        nltk_pkg.set_text(text)
    return nltk_pkg,spacy_pkg,stanza_pkg



#tokenizers,
def handle_tokenization(spacy_pkg,nltk_pkg,stanza_pkg):
    data = {}
    data['SpaCyTokenizer'] ,spacySentListLength = spacy_pkg.get_spacy_tokens()
    data['NLTK_word_tokenize'],nltkSentListLength=nltk_pkg.nltk_word_tokenize()
    data["StanzaTokenizer"], stanzaSentListLength = stanza_pkg.get_stanza_tokens()
    data['TreebankWordTokenizer(NLTK)'] = nltk_pkg.nltk_treeback_tokenize()
    data['wordpunct_tokenize(NLTK)'] = nltk_pkg.nltk_wordpunct_tokenize()
    data['WhitespaceTokenizer(NLTK)'] = nltk_pkg.nltk_whitespace_tokenize()
    data['RegexpTokenizer(NLTK)'] = nltk_pkg.nltk_regexp_tokenize()
    data['CoreNLP_Tokenizer(NLTK)'], corenlpLength = nltk_pkg.get_nltk_tokens_corenlp()
    common = {}
    
    maxSentences=max(spacySentListLength,nltkSentListLength,stanzaSentListLength,corenlpLength)
    
    for sentenceID in range(1,maxSentences+1):
        for tokenizer in data.keys():
            if tokenizer == 'SpaCyTokenizer':
                intersection = set(data[tokenizer][str(sentenceID)])
            else:
                if str(sentenceID) in data[tokenizer].keys():
                    intersection = intersection.intersection(set(data[tokenizer][str(sentenceID)]))
        common[str(sentenceID)] = list(intersection)
   
    # pass data to vis comp
    vz(data,True,common)
    return common
    #st.success('Tokenization results loaded!', icon="✅")
               
def handle_pos_tagging(packages_options,spacy_pkg,nltk_pkg,stanza_pkg,common):
    data={}
    if 'NLTK' in packages_options:
        data['NLTK_POS_tags']=nltk_pkg.get_nltk_pos_tags()
        data['NLTK_POS_tags (CoreNLP)']=nltk_pkg.get_nltk_pos_tags_corenlp()
    if 'SpaCy' in packages_options:
        data['SpaCy_POS_tags']=spacy_pkg.get_spacy_pos_tags()
    if 'Stanza' in packages_options:
        data['Stanza_POS_tags']=stanza_pkg.get_stanza_pos_tags()
    vz(data,False,None)
    
    #st.success('POS-Tagging results loaded!', icon="✅")

def handle_const_parsing_multiselect(packages_options,spacy_pkg,nltk_pkg,stanza_pkg):
    if 'SpaCy' in packages_options:
        st.subheader('Spacy Benepar (Berkeley Neural Parser)')
        docs=spacy_pkg.visualise_spacy_benepar_const_parsing()
    if 'NLTK' in packages_options:
        st.subheader('NLTK Stanford Corenlp')
        docs=nltk_pkg.constituency_corenlp()
    if 'Stanza' in packages_options:
        st.subheader('Stanza Constituency Parsing')
        docs=stanza_pkg.visualise_stanza_consti_parsing()
    #st.success('Constituency Parsing results loaded!', icon="✅")


def handle_dep_parsing_multiselect(packages_options,spacy_pkg,nltk_pkg,stanza_pkg):
    if 'NLTK' in packages_options:
        docs=nltk_pkg.get_maltparser_res()
        st.subheader('Dependency Parsing (NLTK-maltparser)')
        for index,doc in enumerate(docs):
            dep_parsing_component(doc,'dp_nltk_'+str(index))

    if 'SpaCy' in packages_options:
        docs=spacy_pkg.convert_for_dep_parsing()
        st.subheader('Dependency Parsing (SpaCy)')
        for index,doc in enumerate(docs):
            dep_parsing_component(doc,'dp_spacy_'+str(index))
            
    if 'Stanza' in packages_options:
        docs=stanza_pkg.convert_for_stanza_dep_parsing()
        st.subheader('Dependency Parsing (Stanza)')
        for index,doc in enumerate(docs):
            dep_parsing_component(doc,'dp_stanza_'+str(index))
    #st.success('Dependency Parsing results loaded!', icon="✅")
def form_callback():
    #st.write(st.session_state.txt + 'ok')
    txt_length = len(st.session_state.txt)
    pkgs_length = len(st.session_state.packages_ms)
    proc_length = len(st.session_state.process_ms)
    #tokenizers_length = len(st.session_state.token_ms)
    #got_tokenization = "Tokenization" in st.session_state.process_ms
    if txt_length==0:
        st.warning('Input text cannot be empty!',icon="⚠️")
    if pkgs_length==0:
        st.warning('Please choose at least 1 package!',icon="⚠️")
    if proc_length ==0:
        st.warning('Please choose at least 1 process!',icon="⚠️")
    if txt_length>0 and pkgs_length>0 and proc_length>0:
        st.session_state.ready = True
    else:
        st.session_state.ready = False
    #if got_tokenization and tokenizers_length==0:
    #    st.warning('Please choose at least 1 tokenizer for tokenization!')
    #if txt_length>0 and pkgs_length>0 and proc_length>0:
    #    if got_tokenization and tokenizers_length>0:
    #        st.session_state.ready=True
    #    elif not got_tokenization:
    #        st.session_state.ready=True
    #    else:st.session_state.ready = False

# Containers
with inputs:
    st.title('NLP Demo app')
    with st.form(key='my-form'):
        #might want to do input checking
        user_text=st.text_area('Input text to analyse:',"I can't finish this whole bottle of water.",key='txt')
        packages_options = st.multiselect(
        'Pick the libraries to use (One or more):',
        ['NLTK', 'SpaCy', 'Stanza'],default=['NLTK', 'SpaCy', 'Stanza'],key='packages_ms'
        )
        process_options=st.multiselect(
            'Pick the process(es) desired:',
            ['Tokenization','POS-Tagging','Constituency Parsing','Dependency Parsing'],
            default=['Tokenization','POS-Tagging','Constituency Parsing','Dependency Parsing'],
            key = 'process_ms')
        submitted = st.form_submit_button("Submit",on_click=form_callback())
        #tokenizers_to_use = st.multiselect('Pick tokenizers to use',[
        #    'NLTK_word_tokenize',
        #    'SpaCyTokenizer',
        #    "StanzaTokenizer",
        #    'TreebankWordTokenizer(NLTK)',
        #    'wordpunct_tokenize(NLTK)',
        #    'WhitespaceTokenizer(NLTK)',
        #    'RegexpTokenizer(NLTK)',
        #    'CoreNLP_Tokenizer(NLTK)',
        #    ],
        #    default=[
        #    'NLTK_word_tokenize',
        #    'SpaCyTokenizer',
        #    "StanzaTokenizer",
        #    'TreebankWordTokenizer(NLTK)',
        #    'wordpunct_tokenize(NLTK)',
        #    'WhitespaceTokenizer(NLTK)',
        #    'RegexpTokenizer(NLTK)',
        #    'CoreNLP_Tokenizer(NLTK)'],
        #    key="token_ms") """
        


with result:
    if st.session_state.ready==True and submitted:
        nltk_pkg,spacy_pkg,stanza_pkg = handle_init_packages(packages_options,user_text)
        st.header('Results:')
        #tokenization,pos_tagging,const_parsing,dep_parsing = st.tabs(["Tokenization", "POS-Tagging", "Constituency Parsing","Dependency Parsing"])
        #with tokenization:
        if "Tokenization" in process_options:
            #tokenizers_to_use,
            common = handle_tokenization(spacy_pkg,nltk_pkg,stanza_pkg)
    #with pos_tagging:
        if 'POS-Tagging' in process_options:
            handle_pos_tagging(packages_options,spacy_pkg,nltk_pkg,stanza_pkg,common)
    #with const_parsing:
        if 'Constituency Parsing' in process_options:
            handle_const_parsing_multiselect(packages_options,spacy_pkg,nltk_pkg,stanza_pkg)
    #with dep_parsing:
        if 'Dependency Parsing' in process_options:
            handle_dep_parsing_multiselect(packages_options,spacy_pkg,nltk_pkg,stanza_pkg)
            #else:
            #    st.warning('No results on Dependency Parsing.', icon="⚠️")