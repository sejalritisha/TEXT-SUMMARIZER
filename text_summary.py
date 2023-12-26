import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
def summarizer(rawdocs):
 #stopwords
 stopwords=list(STOP_WORDS)
 #spacy module
 nlp=spacy.load('en_core_web_sm')
 #doc have all sentences
 doc=nlp(rawdocs)
 #1.tokenisation
 tokens=[token.text for token in doc]
 #2.word frequency dictionary
 word_freq={}
 for word in doc:
    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
         if word.text not in word_freq.keys():
            word_freq[word.text]=1
         else:
            word_freq[word.text]+=1
 #maximum frequency
 max_freq=max(word_freq.values())
 #3.normalized frequency
 for word in word_freq.keys():
    word_freq[word]=word_freq[word]/max_freq
 #4.sentence token
 sent_tokens=[sent for sent in doc.sents]
 #5.sentence frequency dictionary
 sent_scores={}
 for sent in sent_tokens:
    for word in sent:
        if word.text in word_freq.keys():
            if sent not in sent_scores.keys():
                sent_scores[sent]=word_freq[word.text]
            else:
                sent_scores[sent]+=word_freq[word.text]
 #length of summary 30% of sentence 
 select_len=int(len(sent_tokens)*0.3)
 #6.highest frequency sentences in list
 summary=nlargest(select_len,sent_scores,key=sent_scores.get)
 #summary
 final_summary=[word.text for word in summary]
 summary=' '.join(final_summary)
 #Length of original text=len(rawdocs.split(' '))
 #Length of summary text=len(summary.split(' '))
 return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))