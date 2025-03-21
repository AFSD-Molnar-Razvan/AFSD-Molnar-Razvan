import time
import random
import csv

judete = [
    "Alba", "Arad", "Arges", "Bacau", "Bihor", "Bistrita-Nasaud", "Botosani", "Brasov", "Braila", "Buzau",
    "Caras-Severin", "Calarasi", "Cluj", "Constanta", "Covasna", "Dambovita", "Dolj", "Galati", "Giurgiu", "Gorj",
    "Harghita", "Hunedoara", "Ialomita", "Iasi", "Ilfov", "Maramures", "Mehedinti", "Mures", "Neamt", "Olt",
    "Prahova", "Satu Mare", "Salaj", "Sibiu", "Suceava", "Teleorman", "Timis", "Tulcea", "Vaslui", "Valcea",
    "Vrancea", "Bucuresti"
]

judet_procentaj = {
    "Alba": 1.0, "Arad": 1.4, "Arges": 2.0, "Bacau": 2.4, "Bihor": 2.2, "Bistrita-Nasaud": 0.7, "Botosani": 1.0,
    "Brasov": 2.6, "Braila": 1.2, "Buzau": 1.1, "Caras-Severin": 0.8, "Calarasi": 0.8, "Cluj": 3.1, "Constanta": 2.5,
    "Covasna": 0.6, "Dambovita": 1.5, "Dolj": 2.2, "Galati": 2.5, "Giurgiu": 0.9, "Gorj": 1.0, "Harghita": 0.8,
    "Hunedoara": 1.1, "Ialomita": 0.7, "Iasi": 3.0, "Ilfov": 2.3, "Maramures": 1.2, "Mehedinti": 0.7, "Mures": 1.5,
    "Neamt": 1.0, "Olt": 1.5, "Prahova": 2.5, "Satu Mare": 0.8, "Salaj": 0.5, "Sibiu": 1.2, "Suceava": 1.7,
    "Teleorman": 1.4, "Timis": 3.0, "Tulcea": 0.7, "Vaslui": 1.0, "Valcea": 1.4, "Vrancea": 1.1, "Bucuresti": 7.1
}

def get_sex_from_cnp(cnp):
    first_digit = int(cnp[0])
    if first_digit in [1, 3, 5]:
        return "Masculin 👦"
    elif first_digit in [2, 4, 6]:
        return "Feminin 👧"
    else:
        return "Necunoscut"

def get_judet_by_probability():
    judete_list = list(judet_procentaj.keys())
    procentaje = list(judet_procentaj.values())
    return random.choices(judete_list, procentaje)[0]

class HashTable:
    def __init__(self, size=1000000):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, cnp):
        return sum(map(int, cnp)) % self.size

    def insert(self, cnp, nume, judet, sex):
        index = self.hash_function(cnp)
        self.table[index].append((cnp, nume, judet, sex))

    def search(self, cnp):
        index = self.hash_function(cnp)
        for cnp_stocat, nume, judet, sex in self.table[index]:
            if cnp_stocat == cnp:
                return nume, judet, sex
        return None

hash_table = HashTable()
judet_count = {judet: 0 for judet in judete}

with open("cnp_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    data = list(reader)

for cnp, nume in data:
    judet = get_judet_by_probability()
    sex = get_sex_from_cnp(cnp)
    hash_table.insert(cnp, nume, judet, sex)
    judet_count[judet] += 1

print("Tabelul hash a fost incarcata cu succes! ✅")

cnp_test = random.sample(data, 1000)

found_count = 0
not_found_count = 0
first_found = None
start_time = time.time()

for cnp, _ in cnp_test:
    result = hash_table.search(cnp)
    if result:
        found_count += 1
        if first_found is None:
            first_found = (cnp, result[0], result[1], result[2])
    else:
        not_found_count += 1

end_time = time.time()

print(f"Timp total de cautare: {end_time - start_time:.6f} secunde")
print(f"CNP-uri gasite: {found_count}")
print(f"CNP-uri negasite: {not_found_count}")

if first_found:
    judetul = first_found[2]
    procent = judet_procentaj[judetul]
    print(f"Prima persoana gasita: CNP = {first_found[0]}, Nume = {first_found[1]}, Judet = {judetul}, Sex = {first_found[3]}, Procentaj Judet = {procent}%")

print("\nProcentajul tuturor judetelor in baza de date:")
total_cnp = len(data)
for judet in judete:
    procent_real = (judet_count[judet] / total_cnp) * 100
    print(f"{judet}: {procent_real:.2f}%")
