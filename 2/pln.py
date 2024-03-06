import string
import json
import os

from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from rank_bm25 import BM25Okapi
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

results = []
infos = []
documents = []
articles_list = []

def write_in_json(results):
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)


def search(query):
    infos, documents = process()
    
    tokenized_corpus = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    query = query.split(" ")
    score = bm25.get_scores(query)

    for i in range(len(score)):
        infos[i]['score'] = score[i]
    
    filtered_array = [obj for obj in infos if obj['score'] != 0.0]

    ordered_array = sorted(filtered_array, key=lambda obj: obj['score'], reverse=True)

    return ordered_array


def get_references(txt):
    i = txt.find('REFERENCES')
    if i == -1:
        i = txt.find('References')
    references = txt[i+10:].strip()
    
    return references
    
def get_abstract(txt):
    start = txt.find('Abstract')
    end = txt.find('I.')

    if start != -1 and end != -1:
        abstract = txt[start+8:end].strip()
        return abstract
    else:
        return
    
def get_introduction(txt):
    start = txt.find('I.')
    if start == -1:
        start = txt.lower().find('introduction')
    end = txt.find('II.')
    
    if start != -1 and end != -1:
        introduction = txt[start+12:end].strip()
        return introduction
    else:
        return

def get_objective(txt):
    introduction = get_introduction(txt)
    abstract = get_abstract(txt)

    corpus = (abstract + introduction)
    corpus = sent_tokenize(corpus)

    key_words = [
        "objective",
        "the purpose",
        "aim", "goal",
        "research question",
        "intention", "motivation",
        "mission", "this study",
        "this paper", "this research",
        "this article", "this work",
        "investigative goal",
    ]

    objectives = []
    for sentence in corpus:
        for word in key_words:
            i = str(sentence).find(word)
            if i != -1:
                objectives.append(sentence)
                break
                
    return objectives

def get_methodology(txt):
    corpus = sent_tokenize(txt)

    key_words = [
        'methodology', 
        'methodologies',
        'method', 
        'interviews', 
        'survey', 
        'content',
        'analysis',
        ]
    
    methodology = []

    max = 3
    count = 0
    
    for sentence in corpus:
        for word in key_words:
            i = str(sentence).find(word)
            if i != -1:
                if(count < max):
                    methodology.append(sentence)
                    count += 1
                break

    return methodology

def get_problem(txt):
    introduction = get_introduction(txt)
    corpus = sent_tokenize(introduction)

    key_words = [
        "problem", "issue",
        "challenge", "difficulty",
        "obstacle", "barrier",
        "trouble", "hurdle",
        "dilemma", "predicament",
        "quandary", "impasse",
        "puzzle", "enigma",
        "mystery", "riddle",
        "question", "conundrum",
        "headache", "stumbling block",
        "thorn in one's side"
    ]

    problems = []

    for sentence in corpus:
        for word in key_words:
            i = str(sentence).find(word)
            if i != -1:
                problems.append(sentence)
            
    return problems

def get_contribuition(txt):   
    key_words = [
        "contribution",
        "contribute",
        "contributes",
        "contributions",
    ]

    contribuitions = []

    for word in key_words:
        i = str(txt).find(word)
        if i != -1:
            aux = txt[i:]
            end = aux.find('.')
            contribuitions.append(aux[:end])

def process(): 
    global infos
    global documents
    global articles_list
    
    path = []
    pdfs = []

    articles = os.scandir('artigos')
    new_articles_list = list(articles)
    
    for article in new_articles_list:
        if article.is_file():
            path.append(article.path)
            pdfs.append(PdfReader(article.path))
   
    articles_list_with_quotes = [f'"{entry}"' for entry in articles_list]
    new_articles_list_with_quotes = [f'"{entry}"' for entry in new_articles_list]
    
    if articles_list_with_quotes == new_articles_list_with_quotes:
        return infos, documents
    
    articles_list = new_articles_list
    documents = []
    infos = []
    
    for idx, pdf in enumerate(pdfs):
        print(f'Extraindo informações do PDF {idx+1} de {len(pdfs)}')
        reader = pdf
        content = ''

        title = reader.metadata.title
        for page in reader.pages:
            content += page.extract_text()

        references = get_references(content)

        content = content.split('REFERENCES')[0]
    
        objective = get_objective(content)
        method = get_methodology(content)
        problem = get_problem(content) 
        contribuition = get_contribuition(content)
        content = content.lower()

        text = ''.join([c for c in content if c not in string.punctuation])

        documents.append(text)

        # Tokenização
        tokens = word_tokenize(text)

        # Remoção de stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.lower() not in stop_words]

        # Stemming
        # stemmer = SnowballStemmer('english')
        # tokens = [stemmer.stem(word) for word in tokens]
        # print(tokens)

        # Lematização
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        # Frequência
        freq = nltk.FreqDist(tokens)
        frequency = freq.most_common(10)
        
         # # Bigramas
        bigrams = list(nltk.bigrams(tokens))
        freq_bigrams = nltk.FreqDist(bigrams).most_common(10)

        # # Trigramas
        trigrams = list(nltk.trigrams(tokens))
        freq_trigrams = nltk.FreqDist(trigrams).most_common(10)
        
        results.append({
            'title': title,
            'article': path[idx],
            'objectives': objective,
            'problems': problem,
            'methodology': method,
            'contribuitions': contribuition,
            'references': references,
            'frequency': frequency,
            'bigrams': freq_bigrams,
            'trigrams': freq_trigrams
        })

        infos.append({
            'title': title,
            'path': path[idx],
            'objectives': objective,
            'score': None
        })
       
    write_in_json(results)
    
    return infos, documents
