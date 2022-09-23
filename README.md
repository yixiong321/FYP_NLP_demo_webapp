# FYP_NLP_demo_webapp
NLP demo web app that demostrates the differences and similarities between NLTK,spaCy and Stanza packages in tokenization, POS-tagging, constituency parsing and dependency parsing. 

# Requirements :
1) installed Python
2) installed Java

# Installation Guide:
1. Create a new project folder
2. Create a virtual environment for project in cmd via <code>python -m venv venv</code> and activate it
3. Git clone the repository
4. Download <a href="http://maltparser.org/dist/maltparser-1.9.2.zip">maltparser-1.9.2.zip</a> and unzip
5. Download pre-trained English model via <a href="https://www.maltparser.org/mco/english_parser/engmalt.poly-1.7.mco">engmalt.poly-1.7.mco</a>
6. Download <a href="http://nlp.stanford.edu/software/stanford-corenlp-4.4.0.zip">StanfordCoreNLP</a> (project uses version 4.4.0)
7. Move all downloaded files into FYP_NLP_demo_webapp folder and unzip all compressed files.
6. set a environment variable to overwrite default stanza download location via <code>set STANZA_RESOURCES_DIR={project directory}</code>
7. open a new cmd and run the StanfordCoreNLP server from the within the stanford-corenlp-4.4.0 folder via <code>java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer</code>
8. install dependencies via <code>pip install -r requirements.txt</code>
9. run the NLP demostration web application via <code>streamlit run nlp_demo_app.py</code>. (click submit to download stanza models for the first time,might take a while for the first time)



