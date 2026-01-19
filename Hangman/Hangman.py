import re
import csv
import random
import logging
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Set, Optional


# Configurare logging pentru a înlocui print-urile simple, dacă e nevoie (opțional)
# Aici folosim print pentru a păstra exact output-ul cerut.

class HangmanSolver:
    def __init__(self, fisier_cuvinte: str = "cuvinte.txt"):
        self.toate_cuvintele = self._incarca_cuvinte(fisier_cuvinte)

    def _incarca_cuvinte(self, cale_fisier: str) -> List[str]:
        """Încarcă și filtrează cuvintele din fișier."""
        p = Path(cale_fisier)
        if not p.exists():
            raise FileNotFoundError(f"{cale_fisier} nu a fost găsit.")

        with p.open("r", encoding="utf-8") as f:
            # List comprehension combinat pentru eficiență
            cuvinte = [
                linie.strip().lower()
                for linie in f
                if linie.strip() and all(c.isalpha() or c == '-' for c in linie.strip())
            ]

        print(f"{len(cuvinte)} cuvinte încărcate din {cale_fisier}")
        return cuvinte

    def _filtreaza_candidate(self, pattern: str, pool_cuvinte: List[str], litere_incercate: Set[str]) -> List[str]:
        """
        Returnează cuvintele care se potrivesc cu pattern-ul și nu conțin litere
        deja încercate care s-au dovedit a fi greșite.
        """
        # Transformăm pattern-ul în regex: * sau _ devine .
        regex_pattern = '^' + pattern.replace('*', '.').replace('_', '.') + '$'
        regex = re.compile(regex_pattern)

        # Identificăm literele care s-au dovedit a fi greșite (sunt în setul încercat, dar nu în pattern)
        # Optimizare: folosim set-uri pentru viteză
        litere_in_pattern = set(c for c in pattern if c.isalpha())
        litere_gresite = litere_incercate - litere_in_pattern

        candidati = []
        for cuvant in pool_cuvinte:
            # 1. Verificăm regex-ul
            if regex.match(cuvant):
                # 2. Verificăm dacă cuvântul conține litere pe care știm deja că nu le are
                # (intersecția dintre literele cuvântului și literele greșite trebuie să fie vidă)
                if litere_gresite.isdisjoint(set(cuvant)):
                    candidati.append(cuvant)

        return candidati

    def _alege_litera_optima(self, candidati: List[str], litere_incercate: Set[str]) -> Optional[str]:
        """Alege cea mai frecventă literă din candidați, excluzând cele deja încercate."""
        counter = Counter()
        for cuvant in candidati:
            # Adăugăm literele unice din cuvânt care nu au fost încercate
            counter.update(set(cuvant) - litere_incercate)

        if not counter:
            return None
        # Returnează cea mai comună literă
        return counter.most_common(1)[0][0]

    def rezolva(self, cuvant_real: str, pool_personalizat: List[str] = None, pattern_start: str = None) -> Tuple[
        bool, int, str]:
        """Logica principală a jocului."""
        # Dacă nu se specifică un pool, folosim dicționarul întreg
        pool = pool_personalizat if pool_personalizat is not None else self.toate_cuvintele

        pattern = pattern_start if pattern_start else '*' * len(cuvant_real)
        litere_incercate = {c for c in pattern if c.isalpha()}
        incercari = 0

        while '*' in pattern or '_' in pattern:
            # 1. Filtrare
            posibile = self._filtreaza_candidate(pattern, pool, litere_incercate)

            # 2. Alegere literă
            litera = self._alege_litera_optima(posibile, litere_incercate)

            # Fallback: Dacă nu există candidați (cuvântul nu e în dicționar),
            # trișăm puțin și luăm o literă din cuvântul real pentru a nu bloca bucla
            if not litera:
                litera = next((l for l in cuvant_real if l not in litere_incercate), None)
                if not litera: break  # Siguranță

            litere_incercate.add(litera)
            incercari += 1

            # 3. Actualizare pattern
            # Reconstruim pattern-ul
            pattern_nou = []
            for i, ch_real in enumerate(cuvant_real):
                if ch_real == litera:
                    pattern_nou.append(litera)
                else:
                    pattern_nou.append(pattern[i])
            pattern = "".join(pattern_nou)

        return True, incercari, pattern

    def ruleaza_simulare_random(self, n: int = 100, exclude_set: Set[str] = None) -> List[Tuple]:
        """Alege n cuvinte random și le rezolvă."""
        candidates = self.toate_cuvintele
        if exclude_set:
            candidates = [w for w in candidates if w not in exclude_set]

        if len(candidates) < n:
            raise ValueError("Nu există suficiente cuvinte pentru simulare.")

        selectate = random.sample(candidates, n)
        rezultate = []

        for cuv in selectate:
            gasit, incercari, _ = self.rezolva(cuv)
            rezultate.append((cuv, gasit, incercari))

        medie = sum(r[2] for r in rezultate) / len(rezultate)
        succes = sum(1 for r in rezultate if r[1]) / len(rezultate) * 100

        print(f"\nSimulare pentru {n} cuvinte random:")
        print(f"  Medie încercări per cuvânt: {medie:.2f}")
        print(f"  Procent succes: {succes:.2f}%")

        return rezultate

    @staticmethod
    def incarca_teste(cale_fisier: str) -> List[Tuple[str, str]]:
        """Încarcă fișierul cu pattern;cuvant."""
        p = Path(cale_fisier)
        if not p.exists():
            raise FileNotFoundError(f"{cale_fisier} nu a fost găsit.")

        teste = []
        with p.open("r", encoding="utf-8") as f:
            for linie in f:
                parts = linie.strip().split(";")
                if len(parts) >= 3:
                    # Format: id;pattern;cuvant
                    _, pattern, cuvant = parts[:3]
                    pattern, cuvant = pattern.strip().lower(), cuvant.strip().lower()

                    if len(pattern) == len(cuvant):
                        teste.append((pattern, cuvant))
                    else:
                        print(f"Atenție: lungimi diferite, ignor: {linie.strip()}")
        print(f"{len(teste)} teste încărcate din {cale_fisier}")
        return teste

    @staticmethod
    def salveaza_csv(nume_fisier: str, header: List[str], randuri: List[Tuple]):
        """Funcție utilitară pentru scrierea CSV."""
        with open(nume_fisier, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(randuri)
        print(f"Rezultate salvate în {nume_fisier}")


# =============================
# Execuție Principală
# =============================
if __name__ == "__main__":
    # 1. Inițializare Solver
    solver = HangmanSolver("cuvinte.txt")

    # 2. Încărcare Teste
    lista_teste = HangmanSolver.incarca_teste("cuvinte_de_verificat.txt")

    # 3. Rulare Teste din Fișier
    print("\n--- Teste din fișier (cuvântul real eliminat din pool) ---")
    rezultate_teste = []

    for pattern, cuvant_real in lista_teste:
        # Simulăm scenariul "necunoscut" eliminând cuvântul țintă din dicționar
        pool_fara_target = [w for w in solver.toate_cuvintele if w != cuvant_real]

        gasit, incercari, pattern_final = solver.rezolva(
            cuvant_real,
            pool_personalizat=pool_fara_target,
            pattern_start=pattern
        )

        rezultate_teste.append((pattern, cuvant_real, gasit, incercari, pattern_final))
        print(f"{cuvant_real.upper():<20} | pattern inițial: {pattern} | găsit: {gasit} | încercări: {incercari}")

    HangmanSolver.salveaza_csv(
        "rezultate_teste.csv",
        ["pattern_initial", "cuvant_real", "gasit", "incercari", "pattern_final"],
        rezultate_teste
    )

    # 4. Simulare Random
    print("\n--- Simulare pe 100 de cuvinte random ---")
    # Excludem cuvintele din teste pentru a nu influența aleatorul, exact ca în original
    set_cuvinte_test = set(t[1] for t in lista_teste)

    rezultate_random = solver.ruleaza_simulare_random(
        n=100,
        exclude_set=set_cuvinte_test
    )

    HangmanSolver.salveaza_csv(
        "rezultate_random.csv",
        ["cuvant", "gasit", "incercari"],
        rezultate_random
    )