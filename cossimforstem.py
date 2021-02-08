def norm(vec):
    return sum([x**2 for x in vec])**0.5
    
def dot(vec1, vec2):
    return sum([x*y for (x,y) in zip(vec1,vec2)]) 
    
def cos(vec1, vec2):
    return dot(vec1,vec2)/(norm(vec1)*norm(vec2))


def word_sim(word1,word2):
    vector1,vector2=[],[]
    if len(word1)!=len(word2):
        if len(word1) < len(word2):
            while len(word1)<len(word2):
                word1+="0"
        else:
            while len(word2)<len(word1):
                word2+="0"
           
    for w1,w2  in zip(list(word1),list(word2)):
        if w1==w2:
            vector1.append(1)
            vector2.append(1)
        else:
            #if w1 == "0":
                #vector1.append(0)
                #vector2.append(1)
            if w2 == 0:
                vector1.append(1)
                vector2.append(0)
            else:
                vector1.append(-1)
                vector2.append(1)
    return cos(vector1,vector2)

        
def sim_stemm(string,wordliste):
    stemmed = []
    for word in string.split():
        if word in wordliste:
            stemmed.append(word)
        else:
            partner = ""
            for entry in wordliste:
                if word_sim(entry,word)>0.7:
                    partner = entry
                    break
            if partner:
                print("_____stemm______:",word,partner,word_sim(partner,word))
                stemmed.append(partner)
            else:
                stemmed.append(word)            
    return " ".join(stemmed)
