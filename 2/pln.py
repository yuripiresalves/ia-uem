import string
import os

from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

results = [
    # {
    #     'article': '',
    #     'objective': '',
    #     'problem': '',
    #     'abstract': '',
    #     'introduction': '',
    #     'references': ''
    # },
    # {
    #     'article': '',
    #     'objective': '',    
    #     'problem': '',
    #     'abstract': '',
    #     'introduction': '',
    #     'references': ''
    # }
]

def write_in_json(results):
    import json
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

def write_in_file(text):
    with open('results.txt', 'a') as f:
        f.write(text + ';;')

def get_references(txt):
    references = ''
    i = txt.find('REFERENCES')
    references = txt[i+10:].strip()
    write_in_file(references)
    
def get_abstract(txt):
    start = txt.find('Abstract')
    end = txt.find('I.')

    if start != -1 and end != -1:
        abstract = txt[start+8:end].strip()
        return abstract
    else:
        return
    
def get_introduction(txt):
    start = txt.find('INTRODUCTION')
    end = txt.find('II.')
    
    if start != -1 and end != -1:
        introduction = txt[start+12:end].strip()
        return introduction
    else:
        return
    
def get_objective(txt, idx):
    introduction = get_introduction(txt)
    abstract = get_abstract(txt)
    
    key_words = [
        "objective",
        "purpose",
        "aim",
        "goal",
        "hypothesis",
        "research question",
        "intention",
        "motivation",
        "rational",
        "investigative goal",
        "scope",
        "mission",
        "this study",
        "this paper",
        "this research",
        "this article"
    ]

    objectives = []

    for word in key_words:
        i = str(introduction).find(word)
        if i != -1:
            objectives.append(introduction[i:i+100])
            objective = ','.join(objectives)    
            # write_in_file(objective)
            results.append({
                'article': 'article ' + str(idx+1),
                'objective': objective
            })
            write_in_json(results)
            # print('INTRODUÇÃO - Objetivo: ' + objective)
        
        
    for word in key_words:
        i = str(abstract).find(word)
        if i != -1:
            objectives.append(abstract[i:i+100])
            objective = ','.join(objectives) 
            results.append({
                'article': 'article ' + str(idx+1),
                'objective': objective
            })   
            write_in_json(results)
            # write_in_file(objective)
            # print('ABSTRACT - Objetivo: ' + objective)


    # i = txt.find('objective')
    # aux = txt[i:i+100]
    # firstDot = aux.find('.')
    # i2 = aux.find(' is ')
    #if i != -1:
    #    print('Objetivo: ' + aux[i2+5:firstDot])
    #else:
    #    print('Objetivo: Não encontrado')


def get_problem(txt):
    start = txt.find('INTRODUCTION')
    end = txt.find('II.')

    if start != -1 and end != -1:
        introduction = txt[start+12:end].strip()
        #print('Introdução: ' + introduction)
    else:
        #print('Introdução: Não encontrada')
        return
    
    key_words = [
        "problem",
        "issue",
        "challenge",
        "difficulty",
        "obstacle",
        "barrier",
        "trouble",
        "hurdle",
        "dilemma",
        "predicament",
        "quandary",
        "impasse",
        "puzzle",
        "enigma",
        "mystery",
        "riddle",
        "question",
        "conundrum",
        "headache",
        "stumbling block",
        "thorn in one's side"
    ]

    problems = []

    for word in key_words:
        i = introduction.find(word)
        if i != -1:
            problems.append(introduction[i:i+100])
            print('Problema: ' + ','.join(problems))
        else:
            break

def main():
    # Lendo o arquivo PDF
    path = []
    pdfs = []
    
    articles = os.scandir('artigos/web')
    for article in articles:
        if article.is_file():
            path.append(article.path)
            pdfs.append(PdfReader(article.path))

    for idx, pdf in enumerate(pdfs):
        print('------------------------------------------------------------')
        print('Article: ' + path[idx])
        reader = pdf
        content = ''

        for page in reader.pages:
            content += page.extract_text()

        # get_references(content)
        get_objective(content, idx) # Objective of the article
        # get_problem(content) # Problem of the article
        
        content = content.split('REFERENCES')[0] #Remove the references from article
        content = content.lower()

        # exit()
        text = ''.join([c for c in content if c not in string.punctuation])


        # Tokenização
        tokens = word_tokenize(text)
        # print(tokens)

        # Remoção de stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.lower() not in stop_words]
        # print(tokens)

        # Stemming
        # stemmer = SnowballStemmer('english')
        # tokens = [stemmer.stem(word) for word in tokens]
        # print(tokens)

        # Lematização
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # print(tokens)

        # Frequência

        freq = nltk.FreqDist(tokens)
        #print('Frequência de palavras')
        #print(freq.most_common(10))
        if idx < len(results):
            results[idx]['article'] = path[idx]
            # results[idx]['abstract'] = get_abstract(content)
            # results[idx]['introduction'] = get_introduction(content)
            # results[idx]['references'] = get_references(content)
            # results[idx]['problem'] = get_problem(content)
            # results[idx]['objective'] = get_objective(content, idx)
            results[idx]['frequencia'] = freq.most_common(10)
            write_in_json(results)
        else:
            print("No result found for index:", idx)
        #print('-------------------------------------')
        # freq.plot(10, cumulative=False)

        # # Bigramas
        bigrams = list(nltk.bigrams(tokens))
        # print(bigrams)
        freq_bigrams = nltk.FreqDist(bigrams)
        #print('Frequência de bigramas')
        #print(freq_bigrams.most_common(10))
        #print('-------------------------------------')
        # freq_bigrams.plot(10, cumulative=False)

        # # Trigramas
        trigrams = list(nltk.trigrams(tokens))
        # print(trigrams)
        freq_trigrams = nltk.FreqDist(trigrams)
        #print('Frequência de trigramas')
        #print(freq_trigrams.most_common(10))
        #print('-------------------------------------')
        # freq_trigrams.plot(10, cumulative=False)

main()