from itertools import permutations
import hashlib

hash_tinta = hashlib.sha256("Abc1$z".encode()).hexdigest()

litere_mari = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
litere_mici = 'abcdefghijklmnopqrstuvwxyz'
cifre = '0123456789'
speciale = '!@#$'

numar_apeluri = 0
parola_gasita = False

def calculeaza_hash(parola):
    return hashlib.sha256(parola.encode()).hexdigest()

for L in litere_mari:
    for m1 in litere_mici:
        for m2 in litere_mici:
            for m3 in litere_mici:
                for d in cifre:
                    for s in speciale:
                        caractere = [L, m1, m2, m3, d, s]
                        for perm in set(permutations(caractere)):
                            parola = ''.join(perm)
                            numar_apeluri += 1
                            if calculeaza_hash(parola) == hash_tinta:
                                print(f"Parola gasita: {parola}")
                                print(f"Numar incercari: {numar_apeluri}")
                                parola_gasita = True
                                break
                        if parola_gasita:
                            break
                    if parola_gasita:
                        break
                if parola_gasita:
                    break
            if parola_gasita:
                break
        if parola_gasita:
            break
    if parola_gasita:
        break

if not parola_gasita:
    print("Parola nu a fost gasita.")
