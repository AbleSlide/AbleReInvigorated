
import openai
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from flask_session import Session
from flask import Flask, jsonify, request, session


load_dotenv()



COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

MAX_SECTION_LEN = 500
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

openai.api_key = os.environ.get("openai_key")
COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
}
def answer_query_with_context(query,df,document_embeddings,show_prompt):
    prompt, arrInds = construct_prompt(
        query,
        document_embeddings,
        df
    )
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"].strip(" \n"), arrInds

def construct_prompt(question, context_embeddings, df):
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)
    chosen_sections = []
    chosen_sections_indexes = []

    count = min(30, df.shape[0]) #if the number of rows is less than 30, then it will scan the entire document
    
    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.  
        # print(section_index)      
        # print("DATAFRAME: ")
        # print(df.head(94))
        print(section_index)
        document_section = df.loc[section_index]
        
        if count == 0:
            break
        else:
            count -= 1 
            
        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index[1]))
    
    arrInds = chosen_sections_indexes
    
    header = """Answer the question as truthfully as possible using the provided context from a youtube video, and if the answer is not contained within the text below, say "This question cannot be answered with the information in the video. Please ask a different question or rephrase."\n\nContext:\n"""
    
    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:", arrInds

def get_embedding(text, model=EMBEDDING_MODEL):
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

def compute_doc_embeddings(df):
    return {
        idx: get_embedding(r.content) for idx, r in df.iterrows()
    }
def load_embeddings(fname):
    df = pd.read_csv(fname, header=0)
    max_dim = max([int(c) for c in df.columns if c != "title" and c != "heading"])
    return {
           (r.title, r.heading): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
    }
def vector_similarity(x, y):
    return np.dot(np.array(x), np.array(y))

def order_document_sections_by_query_similarity(query, contexts):
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities

def remove_non_ascii(string):
    return ''.join(char for char in string if ord(char) < 128)


#===========================
#=====TIMESTAMP=CODE========
#===========================

def makeNumArr(arrInds):
    num = arrInds
    arr = []
    for i in range(len(num)):
        arr.append(int(num[i]))
    return arr 

def get_start_and_end(output_transcript, df, arrInds):
    arrNum = makeNumArr(arrInds)
    output = output_transcript

    arrPut = output

    arrTime = []
    for i in range(len(arrNum)):
        text = df['content'][arrNum[i]-1]
        text = text.strip()
        text = text.lower()
        for j in range(len(arrPut)):
            temp = arrPut[j]['text']
            temp = temp.strip()
            temp = temp.lower()
            if temp == text: 
                arrTime.append( ( int(arrPut[j]['start']) , int(arrPut[j]['end'] )) )

    return arrTime

def getLinks(df, output_transcript, arrInds):
    arrTimes = get_start_and_end(output_transcript, df, arrInds)
    sorted(arrTimes)
    arrLink = [] 

    for i in range(len(arrTimes)):
        arrLink.append(str(arrTimes[i][0]-3))
    
    return arrLink

def filterLinks(vid_length, df, output_transcript, arrInds, is_article=False):
    if(is_article):
        arrNum = makeNumArr(arrInds)