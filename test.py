from tkinter import *
from tkinter import filedialog
import os
import ctypes
from numpy import vectorize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


test_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
test_contents = [open(File).read() for File in test_files]
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
 
vectors = vectorize(test_contents)
test_vectors = list(zip(test_files, vectors))

def plagiarism_checking():
    output = set()
    global test_vectors
    for test_a, text_vector_a in test_vectors:
        org_vectors = test_vectors.copy()
        current_index = org_vectors.index((test_a, text_vector_a))
        del org_vectors[current_index]
        for test_b, text_vector_b in org_vectors:
            score = similarity(text_vector_a, text_vector_b)[0][1]
            samp_pair = sorted((test_a, test_b))
            result = samp_pair[0], samp_pair[1], score
            output.add(result)             
    return output
   
def test():
    for data in plagiarism_checking():
        same_data=data[2]*100
        same_data = "%.2f"%same_data
        output=str.format("The plgarized content is "+same_data+" %"+"\n conducted between "+data[0]+" "+data[1])
        result["text"]=output
        

window=Tk()
window.title('Plagrism Checker')
window.configure(background="#9bf6ff")
window.geometry("280x150")
window.resizable(width=False, height=False)

Label(window, text="Detect Plagrism", font=("Times new roman", 20, "bold"),bg="#9bf6ff",fg="#3a0ca3").pack(side=TOP)

short_frame = Frame(window)
result= Label(short_frame,width=62,font=("Arial 10"))
result.pack()
short_frame.pack(pady=10)

Button(window,text="Check",command=test,width=100).pack(side=BOTTOM)
window.mainloop()