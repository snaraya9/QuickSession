from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud.speech import enums
from google.cloud.speech import types
from moviepy.editor import VideoFileClip, concatenate_videoclips
from copy import deepcopy
from nltk.corpus import wordnet
import moviepy.editor as mpe
import os
import io
import moviepy.editor as mp


def timeval(a,t):
    for i in t:
        l = i.split()
        
        if a in l:
            return t[i]

def retrieve(a,t,subt):
    for i in t:
        if a-t[i]==subt:
            return i
    return ""

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def match(a,b):
    store = []
    for i in a:
        original_length = 0
        for j in b:
            i1 = i.split()
            j1 = j.split()
            common_list = intersection(i1,j1)
            
            if len(common_list)>original_length:
                final = j
                original_length = len(common_list)
        temp = [b[final]-10,b[final]]
        
        if temp not in store:
            store.append(temp)
        
        else:
            temp = [b[final]+10,b[final]+20]
            store.append(temp)
    
    return store

def find(a):
    synonyms = []
    for syn in wordnet.synsets(a):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/nischalkashyap/Downloads/Coding Practice/HackNC/key.json"

file_name = os.path.join(os.path.dirname(__file__))
clip_length = VideoFileClip("test2.mp4")
value = 0
return_list = []

client = speech_v1.SpeechClient()

encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
sample_rate_hertz = 44100
language_code = 'en-US'
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code, 'audio_channel_count': 2}
text_list2 = {}
while (value+10)<clip_length.duration:
    return_list2 = []
    initial_value = value
    value+=10
    print(initial_value,value)
    clip = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(initial_value,value)
    clip.audio.write_audiofile(os.path.join(file_name, "test.wav"))

    f_name = os.path.join(file_name, "test.wav")

    # Loads the audio into memory
    with io.open(f_name, 'rb') as audio_file:
        content = audio_file.read()
        audio=types.RecognitionAudio(content=content)

    response = client.recognize(config, audio)
    return_list.append(response.results)
    return_list2.append(deepcopy(response.results))
    
    for i in return_list2:
        for j in i:
            text_list2[j.alternatives.pop().transcript] = value
    
text_list = []
for i in return_list:
    for j in i:
        text_list.append(j.alternatives.pop().transcript)

text = ' '.join(text_list)

intro_words = ["firstly","lecture","means","talks","first","start","like","given","define","called","before","introducing","states","Lets","say"]
mid_words = ["notice","here","example","connect","equations","another","so","main","point"]
conc_words = ["so","hence","therefore","thank","thanks","questions","any","finally","wraps","well","ok","next","week","concluding"]
stopwords = ["hey","guys","i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
inserted = []
required = ""

sentence_list = text.split()

position = oldtime_val = flag1 = flag2 = flag3 = count1 = count2 = count3 = 0

for i in intro_words:
    position = 0
    for j in sentence_list:
        syn = find(j)
        
        if (i==j or i in syn) and i not in stopwords:
            count1+=1
            flag1=1
            a = position-5
            b = position+5
            
            if a<0:
                a = 0
            
            if b>len(sentence_list):
                b = len(sentence_list)
            required += " ".join(sentence_list[a:b+1])
            inserted.append(" ".join(sentence_list[a:b+1]))
            break
        position+=1
    
    if flag1==1 and count1==2:
        break

for i in mid_words:
    position = 0
    for j in sentence_list:
        time_val = timeval(j,text_list2)
        syn = find(j)
        
        if (i==j or i in syn) and i not in stopwords:
            count2+=1
            r = ""
            
            if flag1!=1:
                r = retrieve(time_val,text_list2,10)
                inserted.append(r)
                flag1=1
            flag2=1
            a = position-5
            b = position+5
            
            if a<0:
                a = 0
            
            if b>len(sentence_list):
                b = len(sentence_list)
            required += " " + r + " " + " ".join(sentence_list[a:b+1])
            inserted.append(" ".join(sentence_list[a:b+1]))
            break
        position+=1
    
    if flag2==1 and count2==2:
        break

for i in conc_words:
    position = 0
    for j in sentence_list:
        time_val = timeval(j,text_list2)
        syn = find(j)
        
        if (i==j or i in syn) and i not in stopwords:
            count3+=1
            r1 = ""
            r2 = ""
            
            if flag1!=1:
                r1 = retrieve(time_val,text_list2,20)
                inserted.append(r1)
                flag1 = 1
            
            if flag2!=1:
                r2 = retrieve(time_val,text_list2,10)
                inserted.append(r2)
                flag2 = 1
            flag3=1
            a = position-5
            b = position+5
            
            if a<0:
                a = 0
            
            if b>len(sentence_list):
                b = len(sentence_list)
            required += " " + r1 + " " + r2 + " " + " ".join(sentence_list[a:b+1])
            inserted.append(" ".join(sentence_list[a:b+1]))
            break
        position+=1
    
    if flag3==1 and count3==2:
        break

if flag1==1:
    
    if flag2==1 and flag3==0:
        required += " " + list(text_list2.keys())[-1]
        temp = list(text_list2.keys())
        inserted.append(temp[int(3*len(temp)/4)])
        inserted.append(list(text_list2.keys())[-1])
    
    elif flag2==0 and flag3==0:
        temp = list(text_list2.keys())
        required += " " + temp[int(len(temp)/2)]
        inserted.append(temp[int(len(temp)/2)]) 
        inserted.append(temp[int(3*len(temp)/4)])
        inserted.append(temp[int(9*len(temp)/10)])
        inserted.append(temp[-1])


print("TIMESTAMP")
time_stamp = match(inserted,text_list2)
time_stamp_list = sorted(time_stamp,key=lambda l:l[1])
print(time_stamp_list)

clip1 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[0][0],time_stamp_list[0][1])
clip2 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[1][0],time_stamp_list[1][1])
clip3 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[2][0],time_stamp_list[2][1])
clip4 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[3][0],time_stamp_list[3][1])
clip5 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[4][0],time_stamp_list[4][1])
clip6 = mp.VideoFileClip(os.path.join(file_name, "test2.mp4")).subclip(time_stamp_list[5][0],time_stamp_list[5][1])

final_clip = concatenate_videoclips([clip1,clip2,clip3,clip4,clip5,clip6])
final_clip.write_videofile("my_concatenation.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")




    