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

objective = ''
references = ''
problem = ''
    
results = [
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
    i = txt.find('REFERENCES')
    references = txt[i+10:].strip()
    return references
    # print(idx)
    # results.append({
    #     'references': references
    # })
    
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
    
def get_objective(txt):
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
            aux = introduction[i:]
            end = aux.find('.')
            objectives.append(introduction[i:i+end])
            
            # objective = ','.join(objectives) 
            # return objective 
            # write_in_file(objective)
            # results.append({
            #     # 'article': 'article ' + str(idx+1),
            #     'objective': objective
            # })
            # print('INTRODUÇÃO - Objetivo: ' + objective)
        
    objective = ','.join(objectives)
    return objective
        
    # for word in key_words:
    #     i = str(abstract).find(word)
    #     if i != -1:
    #         objectives.append(abstract[i:i+100])
            # objective = ','.join(objectives) 
            # return objective
            # results.append({
            #     # 'article': 'article ' + str(idx+1),
            #     'objective': objective
            # })   
            # write_in_file(objective)
            # print('ABSTRACT - Objetivo: ' + objective)

    # print(objectives)
    # i = txt.find('objective')
    # aux = txt[i:i+100]
    # firstDot = aux.find('.')
    # i2 = aux.find(' is ')
    #if i != -1:
    #    print('Objetivo: ' + aux[i2+5:firstDot])
    #else:
    #    print('Objetivo: Não encontrado')

def get_methodology(txt):
    methodology = ''

    words = [
        'methodology', 
        'methodologies',
        'method', 
        'interviews', 
        'survey', 
        'content'
        'analysis'
        ]
    
    for word in words:
        start = txt.find(word)
        if start != -1:
            aux = txt[start:]
            end = aux.find('.')
            methodology = txt[start+12:end].strip()

    return methodology


def get_problem(txt):

    introduction = get_introduction(txt)
    
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
        i = str(introduction).find(word)
        if i != -1:
            problems.append(introduction[i:i+100])
            # print('Problema: ' + ','.join(problems))
            
    problem = ','.join(problems)
    return problem

def get_contribuition(txt):

    
    key_words = [
        "contribution",
        "contribute",
        "contributes"
    ]

    contribuitions = []

    for word in key_words:
        i = str(txt).find(word)
        if i != -1:
            contribuitions.append(txt[i:i+100])
            # print('Problema: ' + ','.join(problems))

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
        # print('------------------------------------------------------------')
        print(f'Extraindo informações do PDF {idx+1} de {len(pdfs)}')
        reader = pdf
        content = ''

        title = reader.metadata.title
        for page in reader.pages:
            content += page.extract_text()

        references = get_references(content)
        objective = get_objective(content) # Objective of the article
        problem = get_problem(content) # Problem of the article
        methodology = get_methodology(content)
        contribuition = get_contribuition(content)
        
        content = content.split('REFERENCES')[0] #Remove the references from article
        content = content.lower()

        #exit()
        text = ''.join([c for c in content if c not in string.punctuation])


        # Tokenização
        tokens = word_tokenize(text)
        # print(tokens)

        # Remoção de stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.lower() not in stop_words]
        # print('-------------------------')
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
        
        # results.append({
        #     'frquency': freq.most_common(10)
        # })
        
        
        results.append({
            'title': title,
            'article': path[idx],
            'objective': objective,
            'problem': problem,
            'methodology': methodology,
            # 'abstract': '',
            # 'introduction': '',
            'references': references
        })
        
        # results[idx]['article'] = path[idx]
        # results[idx]['abstract'] = get_abstract(content)
        # results[idx]['introduction'] = get_introduction(content)
        # results[idx]['problem'] = get_problem(content)
        # results[idx]['objective'] = get_objective(content, idx)
        # results[idx]['frequency'] = freq.most_common(10)
        
        
        
        #print('Frequência de palavras')
        #print(freq.most_common(10))
        # if idx < len(results):
        #     # results[idx]['article'] = path[idx]
        #     # results[idx]['abstract'] = get_abstract(content)
        #     # results[idx]['introduction'] = get_introduction(content)
        #     # results[idx]['references'] = get_references(content)
        #     # results[idx]['problem'] = get_problem(content)
        #     # results[idx]['objective'] = get_objective(content, idx)
        #     # results[idx]['frequencia'] = freq.most_common(10)
        #     # write_in_json(results)
        # else:
        #     print("No result found for index:", idx)
        #print('-------------------------------------')
        # freq.plot(10, cumulative=False)

        # # Bigramas
        bigrams = list(nltk.bigrams(tokens))
        # print(bigrams)
        freq_bigrams = nltk.FreqDist(bigrams)
        #print('Frequência de bigramas')
        # print(freq_bigrams.most_common(10))
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
    
    write_in_json(results)

main()