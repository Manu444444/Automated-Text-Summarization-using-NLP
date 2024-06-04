# In[1]:


text=""" I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best foodMy family is very important to me. We do lots of things together. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much."""


# In[2]:


len(text)


# In[3]:


pip install spacy


# In[4]:


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


# In[5]:


get_ipython().system('python -m spacy download en')


# In[6]:


nlp = spacy.load('en_core_web_sm')


# In[7]:


doc=nlp(text)


# In[8]:


tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text !='\n']


# In[9]:


tokens


# In[10]:


tokens1=[]
stopwords = list(STOP_WORDS)
allowed_pos = ['ADJ','PROPN','VERB','NOUN']
for token in doc:
    if token.text in stopwords or token.text in punctuation:
        continue
    if token.pos_ in allowed_pos:
        tokens1.append(token.text)


# In[11]:


tokens1


# In[12]:


from collections import Counter


# In[13]:


word_freq = Counter(tokens)
word_freq


# In[14]:


max_freq = max(word_freq.values())
max_freq


# In[15]:


for word in word_freq.keys():
    word_freq[word]=word_freq[word]/max_freq
word_freq


# In[16]:


sent_token = [sent.text for sent in doc.sents]


# In[17]:


sent_token


# In[18]:


sent_score={}
for sent in sent_token:
    for word in sent.split():
        if word.lower() in word_freq.keys():
            if sent not in sent_score.keys():
                sent_score[sent]=word_freq[word]
            else:
                sent_score[sent]+=word_freq[word]
        print(word)


# In[19]:


sent_score


# In[20]:


import pandas as pd
pd.DataFrame(list(sent_score.items()),columns=['sentence','score'])


# In[21]:


from heapq import nlargest


# In[22]:


num_sentences=3
n = nlargest(num_sentences,sent_score,key=sent_score.get)


# In[23]:


" ".join(n)


# In[ ]:


import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import END

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

def summarize_text():
    text = text_box.get("1.0", "end-1c")
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc 
              if not token.is_stop and not token.is_punct and token.text != '\n']

    word_freq = Counter(tokens)
    if not word_freq:
        messagebox.showerror("Error", "No words found in the text.")
        return
    
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    
    sent_token = [sent.text for sent in doc.sents]

    sent_score = {}
    for sent in sent_token:
        for word in sent.split():
            if word.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]

    
    num_sentences = int(num_sentences_entry.get())
    summarized_sentences = nlargest(num_sentences, sent_score, key=sent_score.get)

    result_box.delete(1.0, END)
    result_box.insert(END, " ".join(summarized_sentences))

root = tk.Tk()
root.title("Text Summarizer")

text_box = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
text_box.pack(pady=10)

num_sentences_label = tk.Label(root, text="Number of Sentences:")
num_sentences_label.pack()
num_sentences_entry = tk.Entry(root, width=10)
num_sentences_entry.insert(END, "3")  # Default value
num_sentences_entry.pack()

summarize_button = tk.Button(root, text="Summarize", command=summarize_text)
summarize_button.pack(pady=5)

result_box = scrolledtext.ScrolledText(root, width=50, height=5, wrap=tk.WORD)
result_box.pack(pady=10)

root.mainloop()


# In[25]:


from transformers import pipeline


# summarizer=pipeline("summarization",model='t5-base',tokenizer='t5-base',framework='pt')

# In[13]:


text=""" I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best foodMy family is very important to me. We do lots of things together. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much."""


# In[11]:


summary = summarizer(text,max_length=100,min_length=10,do_sample=False)
summary


# In[12]:


print(summary[0]['summary_text'])


# In[ ]:


import tkinter as tk
from transformers import pipeline

def summarize_text():
    text = text_entry.get("1.0", "end-1c")
    summary = summarizer(text, max_length=100, min_length=10, do_sample=False)
    output_text.delete("1.0", "end")
    output_text.insert("1.0", summary[0]['summary_text'])
window = tk.Tk()
window.title("Text Summarizer")
text_entry = tk.Text(window, height=10, width=60)
text_entry.pack(pady=10)
summarize_button = tk.Button(window, text="Summarize", command=summarize_text)
summarize_button.pack()
output_text = tk.Text(window, height=10, width=60)
output_text.pack(pady=10)
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")
window.mainloop()





