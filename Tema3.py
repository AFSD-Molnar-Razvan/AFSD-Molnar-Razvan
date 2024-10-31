meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Rony", "David", "Denis", "Alex", "Costel"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
cat_guias_era_la_inceput = meniu.count("guias")
cat_guias_s_a_comandat = comenzi.count("guias")
pret_guias = preturi[1][1]
print(cat_guias_era_la_inceput - cat_guias_s_a_comandat)
print(cat_guias_s_a_comandat * pret_guias)
istoric_comenzi = []
print(studenti[0]+comenzi[0])
tava=tavi.pop()
student=studenti.pop(0)
comanda=comenzi.pop(0)
istoric_comenzi.append(comanda)
while studenti and tavi and comenzi:
    student = studenti.pop(0)
    comanda = comenzi.pop(0)
    tava = tavi.pop(0)
    istoric_comenzi.append([student, comanda])
    print (f"{student} a comandat {comanda}.")
    print("\nIstoricul comenzilor:")
    for comanda in istoric_comenzi:
        print(comanda)
    comenzi_count = {
        "papanasi": 0,
        "ceafa": 0,
        "guias": 0
    }
    for comanda in istoric_comenzi:
        if comanda in comenzi:
            comenzi_count[comanda] += 1
        print(f"\nS-au comandat {comenzi_count['guias']} guias, {comenzi_count['ceafa']} ceafa, {comenzi_count['papanasi']} papanasi.")
        print(f"Mai sunt {len(tavi)} tavi.")
        disponibilitate = {
            "papanasi": meniu.count("papanasi") > 0,
            "ceafa": meniu.count("ceafa") > 0,
            "guias": meniu.count("guias") > 0
        }
        print(f"Mai este ceafa: {not disponibilitate['ceafa']}.")
        print(f"Mai sunt papanasi: {disponibilitate['papanasi']}.")
        print(f"Mai sunt guias: {disponibilitate['guias']}.")
        print(f"Mai sunt {len(tavi)} tavi.")
        total_venit = 0
        for comanda in istoric_comenzi:
            for produs in preturi:
                if produs[0] == comanda:
                    total_venit += produs[1]
        print(f"\nCantina a încasat: {total_venit} lei.")
        produse_mici = [produs for produs in preturi if produs[1] <= 7]
        print(f"Produse care costă cel mult 7 lei: {produse_mici}.")