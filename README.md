# FYP_NLP_demo_webapp
NLP demo web app that demostrates the differences and similarities between NLTK,spaCy and Stanza packages in tokenization, POS-tagging, constituency parsing and dependency parsing. 

# Requirements :
1) installed Python
2) installed Java

# Installation Guide:
1. Create a new project folder
2. Create a virtual environment for project in cmd via <code>python -m venv venv</code> and activate it
3. Git clone the repository
4. Download maltparser-1.9.2 [here](http://maltparser.org/dist/maltparser-1.9.2.zip) and unzip
5. Download pre-trained English model [here](https://www.maltparser.org/mco/english_parser/engmalt.poly-1.7.mco)
6. set a environment variable to overwrite default stanza download location via <code>set STANZA_RESOURCES_DIR={project directory}</code>
6. Download StanfordCoreNLP (project uses version 4.40) and cd to downloaded folder
7. run the server from the within the directory via <code>java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer</code>
8. install dependencies via <code>pip install -r requirements.txt</code>
9. run the NLP demostration web application via <code>streamlit run nlp_demo_app.py</code>.

