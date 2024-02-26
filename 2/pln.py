from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import string
import os

# parts = []

references = ''

# def visitor_body(text, cm, tm, font_dict, font_size):
#     isRefering = False
#     references = ''
#     parts = []
#     y = cm[5]
#     if isRefering:
#         references += text
#     if(text.strip() == 'REFERENCES'):
#         print('entra')
#         isRefering = True
#     parts.append(text)
#     print(references)

def get_objective(txt):
    
    start = txt.find('INTRODUCTION')
    end = txt.find('II.')
    
    if start != -1 and end != -1:
        introduction = txt[start+12:end].strip()
        #print('Introdução: ' + introduction)
    else:
        #print('Introdução: Não encontrada')
        return

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
        "this study is"
    ]

    objectives = []

    for word in key_words:
        i = introduction.find(word)
        if i != -1:
            objectives.append(introduction[i:i+100])
            print('Objetivo: ' + ','.join(objectives))
        else:
            break

    # i = txt.find('objective')
    # aux = txt[i:i+100]
    # firstDot = aux.find('.')
    # i2 = aux.find(' is ')
    #if i != -1:
    #    print('Objetivo: ' + aux[i2+5:firstDot])
    #else:
    #    print('Objetivo: Não encontrado')

def getReferences(txt):
    i = txt.find('REFERENCES')
    references = txt[i+10:].strip()
    # print(references)
    # txt.split('REFERENCES')

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
    scandir = os.scandir('artigos/web')
    for entry in scandir:
        if entry.is_file():
            path.append(entry.path)
            pdfs.append(PdfReader(entry.path))
    # reader = PdfReader("artigos/web/Strategies_for_web_application_development_methodologies.pdf")

    parts = []

    for idx, pdf in enumerate(pdfs):
        print('-------------------------------------------------------------------------------')
        print('Article: ' + path[idx])
       # print('Article: ' + pdf.metadata.title)
        reader = pdf
        content = '' 

        for page in reader.pages:
            content += page.extract_text()

        getReferences(content)
        get_objective(content) # Objective of the article
        get_problem(content) # Problem of the article
        
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