import random
import csv
import argparse
import time
import sys
from typing import List, Tuple, Set, Dict, Optional

# --- CONSTANTE ȘI PUNCTAJE ---
SCOR_LINIE_5 = 50
SCOR_T = 30
SCOR_L = 20
SCOR_LINIE_4 = 10
SCOR_LINIE_3 = 5


class Formatiune:
    """Reprezintă o formațiune validă detectată (Match)."""

    def __init__(self, tip: str, scor: int, celule: Set[Tuple[int, int]]):
        self.tip = tip  # Ex: "L", "T", "Linie_3"
        self.scor = scor  # Punctajul formațiunii
        self.celule = celule  # Set de coordonate (rând, coloană)

    def __repr__(self):
        return f"{self.tip}({self.scor}pct, {len(self.celule)}celule)"


class TablaJoc:
    def __init__(self, randuri=11, coloane=11, seed=None):
        self.randuri = randuri
        self.coloane = coloane
        self.rng = random.Random(seed)  # Generator de numere aleatoare controlat
        self.matrice = [[0 for _ in range(coloane)] for _ in range(randuri)]
        self.scor = 0

    def initializeaza(self):
        """Populează tabla și rezolvă formațiunile inițiale fără a acorda puncte."""
        # 1. Populare aleatorie cu valori 1-4
        for r in range(self.randuri):
            for c in range(self.coloane):
                self.matrice[r][c] = self.rng.randint(1, 4)

        # 2. Stabilizare (elimină formațiunile existente la start)
        # Conform cerinței, acestea se rezolvă imediat, dar nu punctează.
        stabil = False
        while not stabil:
            potriviri = self.detecteaza_formatiuni()
            if not potriviri:
                stabil = True
            else:
                self.elimina_formatiuni(potriviri, actualizeaza_scor=False)
                self.aplica_gravitatie_si_reumplere()

    def get_celula(self, r, c):
        if 0 <= r < self.randuri and 0 <= c < self.coloane:
            return self.matrice[r][c]
        return 0

    def swap(self, r1, c1, r2, c2):
        """Execută un schimb fizic între două celule."""
        self.matrice[r1][c1], self.matrice[r2][c2] = self.matrice[r2][c2], self.matrice[r1][c1]

    def detecteaza_formatiuni(self) -> List[Formatiune]:
        """
        Detectează toate formațiunile valide conform regulilor.
        Strategie:
        1. Identifică segmente orizontale (H) și verticale (V) >= 3.
        2. Caută intersecții pentru formele complexe T și L.
        3. Generează lista de candidați.
        4. Sortează descrescător după scor (Prioritate: 50 -> 30 -> 20 -> 10 -> 5).
        5. Aplică regula anti-dublare (o celulă aparține unei singure formațiuni per pas).
        """
        segmente_h = []  # (rand, col_start, col_end, culoare, lungime)
        segmente_v = []  # (col, rand_start, rand_end, culoare, lungime)

        # 1. Scanare Orizontală
        for r in range(self.randuri):
            c = 0
            while c < self.coloane:
                culoare = self.matrice[r][c]
                if culoare == 0:
                    c += 1
                    continue
                lungime = 1
                while c + lungime < self.coloane and self.matrice[r][c + lungime] == culoare:
                    lungime += 1

                if lungime >= 3:
                    segmente_h.append({'tip': 'H', 'r': r, 'c_start': c, 'c_end': c + lungime - 1, 'culoare': culoare,
                                       'len': lungime})
                c += lungime

        # 2. Scanare Verticală
        for c in range(self.coloane):
            r = 0
            while r < self.randuri:
                culoare = self.matrice[r][c]
                if culoare == 0:
                    r += 1
                    continue
                lungime = 1
                while r + lungime < self.randuri and self.matrice[r + lungime][c] == culoare:
                    lungime += 1

                if lungime >= 3:
                    segmente_v.append({'tip': 'V', 'c': c, 'r_start': r, 'r_end': r + lungime - 1, 'culoare': culoare,
                                       'len': lungime})
                r += lungime

        candidati = []

        # Helper pentru a obține coordonatele celulelor dintr-un segment
        def get_celule_segment(seg):
            celule = set()
            if seg['tip'] == 'H':
                for c_idx in range(seg['c_start'], seg['c_end'] + 1):
                    celule.add((seg['r'], c_idx))
            else:
                for r_idx in range(seg['r_start'], seg['r_end'] + 1):
                    celule.add((r_idx, seg['c']))
            return celule

        # 3. Detectare Forme Complexe (T și L) prin intersecții
        for h in segmente_h:
            for v in segmente_v:
                if h['culoare'] != v['culoare']:
                    continue

                # Verificăm intersecția geometrică
                if h['c_start'] <= v['c'] <= h['c_end'] and v['r_start'] <= h['r'] <= v['r_end']:
                    intersect_r, intersect_c = h['r'], v['c']

                    # Validăm L și T doar dacă segmentele au minim 3 lungime
                    if h['len'] == 3 and v['len'] == 3:
                        celule_h = get_celule_segment(h)
                        celule_v = get_celule_segment(v)
                        uniune_celule = celule_h.union(celule_v)

                        # Clasificare L vs T
                        este_capat_h = (intersect_c == h['c_start'] or intersect_c == h['c_end'])
                        este_capat_v = (intersect_r == v['r_start'] or intersect_r == v['r_end'])

                        if este_capat_h and este_capat_v:
                            # L: Intersecție la capete
                            candidati.append(Formatiune("L", SCOR_L, uniune_celule))
                        else:
                            # T: Intersecție la mijlocul cel puțin unui segment
                            candidati.append(Formatiune("T", SCOR_T, uniune_celule))

        # 4. Adăugăm liniile simple ca și candidați
        for seg in segmente_h + segmente_v:
            scor = 0
            if seg['len'] >= 5:
                scor = SCOR_LINIE_5
            elif seg['len'] == 4:
                scor = SCOR_LINIE_4
            elif seg['len'] == 3:
                scor = SCOR_LINIE_3

            candidati.append(Formatiune(f"Linie_{seg['len']}", scor, get_celule_segment(seg)))

        # 5. Sortare descrescătoare după scor
        candidati.sort(key=lambda x: x.scor, reverse=True)

        # 6. Selecție Greedy (Anti-dublare)
        formatiuni_finale = []
        celule_folosite = set()

        for form in candidati:
            # Dacă nicio celulă din formațiune nu a fost deja punctată în acest pas
            if not form.celule.intersection(celule_folosite):
                formatiuni_finale.append(form)
                celule_folosite.update(form.celule)

        return formatiuni_finale

    def elimina_formatiuni(self, formatiuni: List[Formatiune], actualizeaza_scor=True):
        """Setează celulele implicate pe 0 și adaugă punctele."""
        puncte = 0
        for f in formatiuni:
            puncte += f.scor
            for r, c in f.celule:
                self.matrice[r][c] = 0  # 0 înseamnă gol

        if actualizeaza_scor:
            self.scor += puncte
        return puncte

    def aplica_gravitatie_si_reumplere(self):
        """Elementele cad în spațiile goale (0), apoi se generează altele noi sus."""
        # Gravitație
        for c in range(self.coloane):
            write_idx = self.randuri - 1
            # Parcurgem de jos în sus
            for r in range(self.randuri - 1, -1, -1):
                if self.matrice[r][c] != 0:
                    self.matrice[write_idx][c] = self.matrice[r][c]
                    write_idx -= 1
            # Umplem restul de sus cu 0
            for r in range(write_idx, -1, -1):
                self.matrice[r][c] = 0

        # Reumplere
        for c in range(self.coloane):
            for r in range(self.randuri):
                if self.matrice[r][c] == 0:
                    self.matrice[r][c] = self.rng.randint(1, 4)

    def executa_pas_complet(self, r1, c1, r2, c2):
        """
        Încearcă un swap. Dacă e valid, declanșează cascada.
        Returnează: (mutare_valida, puncte_castigate, nr_cascade)
        """
        # 1. Swap
        self.swap(r1, c1, r2, c2)

        # 2. Verificare validitate
        potriviri = self.detecteaza_formatiuni()
        if not potriviri:
            # Swap invalid, revenim la starea inițială
            self.swap(r1, c1, r2, c2)
            return False, 0, 0

        # 3. Execuție cascadă
        puncte_total = 0
        nr_cascade = 0

        while potriviri:
            pts = self.elimina_formatiuni(potriviri, actualizeaza_scor=True)
            puncte_total += pts
            self.aplica_gravitatie_si_reumplere()
            nr_cascade += 1

            # Verificăm dacă au apărut noi formațiuni după cădere
            potriviri = self.detecteaza_formatiuni()

        return True, puncte_total, nr_cascade

    def obtine_mutari_posibile(self):
        """
        Găsește toate mutările care ar genera puncte.
        Returnează lista sortată descrescător după scorul estimat.
        """
        mutari = []
        directii = [(0, 1), (1, 0)]  # Dreapta și Jos

        for r in range(self.randuri):
            for c in range(self.coloane):
                for dr, dc in directii:
                    nr, nc = r + dr, c + dc
                    if nr < self.randuri and nc < self.coloane:
                        # Simulare swap
                        self.swap(r, c, nr, nc)
                        potriviri = self.detecteaza_formatiuni()
                        if potriviri:
                            # Estimare scor (doar primul pas, fără cascadă, pentru viteză)
                            scor_estimat = sum(m.scor for m in potriviri)
                            mutari.append({
                                'r': r, 'c': c, 'nr': nr, 'nc': nc, 'scor': scor_estimat
                            })
                        # Revert swap
                        self.swap(r, c, nr, nc)

        # Sortare Greedy: încercăm întâi mutările care dau scorul cel mai mare
        mutari.sort(key=lambda x: x['scor'], reverse=True)
        return mutari


class SimulatorJoc:
    def __init__(self, nr_jocuri, randuri, coloane, tinta_scor, seed_start=0, fisier_iesire="results.csv"):
        self.nr_jocuri = nr_jocuri
        self.randuri = randuri
        self.coloane = coloane
        self.tinta_scor = tinta_scor
        self.seed_start = seed_start
        self.fisier_iesire = fisier_iesire
        self.rezultate = []

    def ruleaza(self):
        print(f"Începe simularea a {self.nr_jocuri} jocuri...")
        timp_start = time.time()

        for i in range(self.nr_jocuri):
            game_id = i
            seed = self.seed_start + i
            tabla = TablaJoc(self.randuri, self.coloane, seed=seed)
            tabla.initializeaza()

            swap_uri = 0
            total_cascade = 0
            mutari_pana_la_10000 = None
            tinta_atinsa = False
            motiv_oprire = ""

            while True:
                # Verificare condiții oprire
                if tabla.scor >= self.tinta_scor:
                    tinta_atinsa = True
                    motiv_oprire = "REACHED_TARGET"  # Păstrăm EN pentru CSV standardizat
                    if mutari_pana_la_10000 is None:
                        mutari_pana_la_10000 = swap_uri
                    break

                # Căutare cea mai bună mutare
                mutari_posibile = tabla.obtine_mutari_posibile()
                if not mutari_posibile:
                    motiv_oprire = "NO_MOVES"
                    break

                # Execută mutarea cu cel mai mare potențial
                cea_mai_buna = mutari_posibile[0]
                valid, pts, cascade = tabla.executa_pas_complet(
                    cea_mai_buna['r'], cea_mai_buna['c'], cea_mai_buna['nr'], cea_mai_buna['nc']
                )

                if valid:
                    swap_uri += 1
                    total_cascade += cascade
                    # Verificăm dacă am atins ținta chiar în timpul acestui pas
                    if mutari_pana_la_10000 is None and tabla.scor >= self.tinta_scor:
                        mutari_pana_la_10000 = swap_uri
                else:
                    break

            # Salvare date per joc
            res = {
                "game_id": game_id,
                "points": tabla.scor,
                "swaps": swap_uri,
                "total_cascades": total_cascade,
                "reached_target": tinta_atinsa,
                "stopping_reason": motiv_oprire,
                "moves_to_10000": mutari_pana_la_10000 if mutari_pana_la_10000 is not None else ""
            }
            self.rezultate.append(res)

            # Bară de progres
            if (i + 1) % 10 == 0:
                print(f"Progres: {i + 1}/{self.nr_jocuri} jocuri finalizate.")

        durata = time.time() - timp_start
        self.salveaza_csv()
        self.afiseaza_raport(durata)

    def salveaza_csv(self):
        if not self.rezultate:
            return

        chei = self.rezultate[0].keys()
        try:
            with open(self.fisier_iesire, 'w', newline='') as f:
                dict_writer = csv.DictWriter(f, fieldnames=chei)
                dict_writer.writeheader()
                dict_writer.writerows(self.rezultate)
            print(f"Rezultatele au fost salvate în {self.fisier_iesire}")
        except IOError as e:
            print(f"Eroare la scrierea fișierului: {e}")

    def afiseaza_raport(self, durata):
        total_p = sum(r['points'] for r in self.rezultate)
        total_s = sum(r['swaps'] for r in self.rezultate)
        medie_p = total_p / len(self.rezultate)
        medie_s = total_s / len(self.rezultate)

        jocuri_succes = [r for r in self.rezultate if r['reached_target']]
        if jocuri_succes:
            medie_mutari_win = sum(r['moves_to_10000'] for r in jocuri_succes) / len(jocuri_succes)
        else:
            medie_mutari_win = 0

        print("-" * 40)
        print(f"SIMULARE COMPLETĂ în {durata:.2f}s")
        print(f"Jocuri simulate: {len(self.rezultate)}")
        print(f"Medie Puncte: {medie_p:.2f}")
        print(f"Medie Swap-uri (Total): {medie_s:.2f}")
        print(f"Rată Succes (>=10k): {len(jocuri_succes)}/100")
        if jocuri_succes:
            print(f"Medie Swap-uri pentru a atinge 10.000: {medie_mutari_win:.2f}")
        print("-" * 40)


# --- CLI (Interfața Linie de Comandă) ---
def main():
    parser = argparse.ArgumentParser(description="Proiect Automatizare Candy Crush")
    parser.add_argument("--games", type=int, default=100, help="Număr de jocuri de simulat")
    parser.add_argument("--rows", type=int, default=11, help="Număr rânduri")
    parser.add_argument("--cols", type=int, default=11, help="Număr coloane")
    parser.add_argument("--target", type=int, default=10000, help="Scor țintă")
    # Funcție lambda pentru a parsa corect bool din string
    parser.add_argument("--input_predefined", type=lambda x: (str(x).lower() == 'true'), default=True,
                        help="Folosește seed-uri deterministe (True/False)")
    parser.add_argument("--out", type=str, default="summary.csv", help="Calea fișierului CSV de ieșire")

    args = parser.parse_args()

    # Dacă input_predefined este True, pornim cu seed 0. Altfel, seed bazat pe ceas.
    seed_start = 0 if args.input_predefined else int(time.time())

    runner = SimulatorJoc(
        nr_jocuri=args.games,
        randuri=args.rows,
        coloane=args.cols,
        tinta_scor=args.target,
        seed_start=seed_start,
        fisier_iesire=args.out
    )
    runner.ruleaza()


if __name__ == "__main__":
    main()