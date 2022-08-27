# streamlit_app.py
from turtle import onclick
from spacy_streamlit import visualize_parser
import streamlit as st
from spacy_streamlit import visualize_tokens
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import api
import spacy
import maltparser_nltk as mp
from spacy import displacy
from spacy_streamlit.util import get_svg
import corenlp as cn
from dep_parsing_component import dep_parsing_component

st.set_page_config(layout="wide")
inputs=st.container()
graph=st.container()

def handle_token_multiselects(packages_options,process_options,text):
    df=None
    if 'Tokenization' in process_options:
        nltk_dict=[]
        spacy_dict=[]
        stanza_dict=[]
        if 'NLTK' in packages_options:
            nltk_dict={'NLTK':api.get_nltk_tokens(text)}
            nltk_corenlp_dict={'NLTK_corenlp':api.get_nltk_tokens_corenlp(text)}
        if 'SpaCy' in packages_options:
            spacy_dict={'SpaCy':api.get_spacy_tokens(text)}
        if 'Stanza' in packages_options:
            stanza_dict={'Stanza':api.get_stanza_tokens(text)}

        df_spacy=pd.DataFrame(spacy_dict)
        df_nltk=pd.DataFrame(nltk_dict)
        df_nltk_corenlp=pd.DataFrame(nltk_corenlp_dict)
        df_stanza=pd.DataFrame(stanza_dict)
        df=pd.concat([df_spacy,df_nltk,df_nltk_corenlp,df_stanza], axis=1)
        df.insert(0,'id',range(1,len(df)+1))
             
    if df is not None:
        st.subheader('Tokenisation')
        AgGrid(df)
        
def handle_pos_multiselects(packages_options,process_options,text):
    df=None
   
    if 'POS-tagging' in process_options:
        nltk_pos_dict=[]
        nltk_pos_corenlp_dict=[]
        spacy_pos_dict=[]
        stanza_pos_dict=[]
        if 'NLTK' in packages_options:
            nltk_pos_dict=api.get_nltk_pos_tags(text)
            #nltk_pos_corenlp_dict=api.get_nltk_pos_tags_corenlp(text)
        if 'SpaCy' in packages_options:
            spacy_pos_dict=api.get_spacy_pos_tags(text)
            df=pd.DataFrame(spacy_pos_dict)
        if 'Stanza' in packages_options:
            stanza_pos_dict=api.get_stanza_pos_tags(text)
        df_spacy_pos=pd.DataFrame(spacy_pos_dict)
        df_stanza_pos=pd.DataFrame(stanza_pos_dict)
        df_nltk_pos=pd.DataFrame(nltk_pos_dict)
        #df_nltk_pos_corenlp=pd.DataFrame(nltk_pos_corenlp_dict)
        df=pd.concat([df_spacy_pos,df_nltk_pos,
       # nltk_pos_corenlp_dict,
        df_stanza_pos],axis=1)
        df.insert(0,'id',range(1,len(df)+1))
        
    if df is not None:
        st.subheader('POS-Tagging')
        AgGrid(df)


def handle_dep_parsing_multiselect(packages_options,process_options,text):
    
    if 'Dependency Parsing' in process_options:
        if 'NLTK' in packages_options:
            docs=mp.get_maltparser_res(text)
            st.subheader('Dependency Parsing (NLTK-maltparser)')
            for index,doc in enumerate(docs):
                dep_parsing_component(doc,'dp_nltk_'+str(index))
  
        if 'SpaCy' in packages_options:
            docs=api.get_spacy_doc(text)
            st.subheader('Dependency Parsing (SpaCy)')
            for index,doc in enumerate(docs):
                dep_parsing_component(doc,'dp_spacy_'+str(index))
                
        if 'Stanza' in packages_options:
            docs=api.get_stanza_doc(text)
            st.subheader('Dependency Parsing (Stanza)')
            for index,doc in enumerate(docs):
                dep_parsing_component(doc,'dp_stanza_'+str(index))

            


def handle_const_parsing_multiselect(packages_options,process_options,text):
    if 'Constituency Parsing' in process_options:
        if 'SpaCy' in packages_options:
            st.subheader('Spacy Benepar (Berkeley Neural Parser)')
            docs=api.spacy_benepar(text)

        if 'NLTK' in packages_options:
            st.subheader('NLTK Stanford Corenlp')
            docs=cn.constituency_corenlp(text)
            
        if 'Stanza' in packages_options:
            st.subheader('Stanza Constituency Parsing')
            docs=api.stanzaConverter(text)
            
            
                

# Containers
with inputs:
    st.title('NLP Demo app')    
    with st.form(key='my-form'):
        #might want to do input checking
        user_text=st.text_area('Text to test')
        packages_options = st.multiselect(
        'Pick the libraries to use (One or more):',
        ['NLTK', 'SpaCy', 'Stanza'] 
        )
        process_options=st.multiselect(
            'Pick the process(es) desired:',
            ['Tokenization','POS-tagging','Constituency Parsing','Dependency Parsing']
        )
        submitted = st.form_submit_button("Submit")


with graph:
    if submitted:   
        st.header('Results:')
        handle_token_multiselects(packages_options,process_options,user_text)
        handle_pos_multiselects(packages_options,process_options,user_text)
        
        handle_const_parsing_multiselect(packages_options,process_options,user_text)
        handle_dep_parsing_multiselect(packages_options,process_options,user_text)
    
