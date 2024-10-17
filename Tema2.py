import string

text ='În 2015, BMW a fost al 12-lea cel mai mare producător mondial de autovehicule, cu 2.279.503 de vehicule produse. Membrii familiei Quandt sunt acționari pe termen lung ai companiei, restul de acțiuni fiind deținute de publicul de tip float.'
mijloc=len(text)//2
prima_parte=text[:mijloc]
a_doua_parte=text[mijloc:]
text_majuscule=prima_parte.upper()
print(text_majuscule)
text_fara_spatiu=text.replace(" ", "")
print(text_fara_spatiu)
inverseaza_ordinea_caracterelor=a_doua_parte[::-1]
print(inverseaza_ordinea_caracterelor)
cuvant="Litera"
prima_litera_majuscula=cuvant.capitalize()
print(prima_litera_majuscula)
print(a_doua_parte)
text_fara_punctuatie=text.translate(str.maketrans('', '', string.punctuation))
print(text_fara_punctuatie)