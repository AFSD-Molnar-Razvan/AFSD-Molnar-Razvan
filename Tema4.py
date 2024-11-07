import random

# 1. Lista de cuvinte și alegerea cuvântului la întâmplare
cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]

# 2. Inițializarea numărului de încercări
incercari_ramase = 6
litere_incercate = []


print("Bine ai venit la jocul Spanzuratoarea! ✎")
print("Cuvantul de ghicit este 🤔: " + " ".join(progres))
print(f"Incercari ramase: {incercari_ramase}")


while "_" in progres and incercari_ramase > 0:

    litera = input("Introdu o litera de pe ⌨: ").lower()


    if len(litera) != 1 or not litera.isalpha():
        print("Te rog sa introduci o singura litera valida. 🤬")
        continue

    if litera in litere_incercate:
        print("Ai mai incercat deja aceasta litera. Alege o litera noua.")
        continue


    litere_incercate.append(litera)


    if litera in cuvant_de_ghicit:


        for index, caracter in enumerate(cuvant_de_ghicit):
            if caracter == litera:
                progres[index] = litera
        print("Bine facut! Litera este în cuvant.")
    else:
        incercari_ramase -= 1
        print("Imi pare rau, litera nu este in cuvant. Incercari ramase: " + str(incercari_ramase))


    print("Cuvantul de ghicit este: " + " ".join(progres))
    print(f"Incercări ramase: {incercari_ramase}")


if "_" not in progres:
    print("Felicitari 😃! Ai ghicit cuvantul: " + cuvant_de_ghicit)
else:
    print("Ai pierdut 😭! Cuvantul era: " + cuvant_de_ghicit)