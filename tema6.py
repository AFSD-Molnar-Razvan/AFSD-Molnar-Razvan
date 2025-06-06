from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)
FISIER_DATE = 'produse.json'

def incarca_produse():
    if not os.path.exists(FISIER_DATE):
        with open(FISIER_DATE, 'w') as f:
            json.dump([], f)
    with open(FISIER_DATE, 'r') as f:
        return json.load(f)

def salveaza_produse(lista):
    with open(FISIER_DATE, 'w') as f:
        json.dump(lista, f, indent=2)

@app.route('/produse', methods=['GET'])
def toate_produsele():
    return jsonify(incarca_produse()), 200

@app.route('/produse/<int:id_produs>', methods=['GET'])
def produs_dupa_id(id_produs):
    produse = incarca_produse()
    produs = next((p for p in produse if p['id'] == id_produs), None)
    return (jsonify(produs), 200) if produs else (jsonify({'eroare': 'Nu exista'}), 404)

@app.route('/produse', methods=['POST'])
def adauga_produs():
    produse = incarca_produse()
    nou = request.get_json()
    nou['id'] = max((p['id'] for p in produse), default=0) + 1
    produse.append(nou)
    salveaza_produse(produse)
    return jsonify(nou), 201

@app.route('/produse/<int:id_produs>', methods=['PUT'])
def actualizeaza(id_produs):
    produse = incarca_produse()
    modificat = request.get_json()
    for i, p in enumerate(produse):
        if p['id'] == id_produs:
            produse[i].update(modificat)
            salveaza_produse(produse)
            return jsonify(produse[i]), 200
    return jsonify({'eroare': 'Nu a fost gasit'}), 404

@app.route('/produse/<int:id_produs>', methods=['DELETE'])
def sterge(id_produs):
    produse = incarca_produse()
    noi = [p for p in produse if p['id'] != id_produs]
    if len(noi) != len(produse):
        salveaza_produse(noi)
        return jsonify({'mesaj': 'Sters'}), 200
    return jsonify({'eroare': 'Nu a fost gasit'}), 404

HTML = """
<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="UTF-8">
  <title>Catalog Produse</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f2f2f2; padding: 20px; }
    h1 { text-align: center; }
    table { width: 80%%; margin: auto; border-collapse: collapse; background: white; }
    th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
    th { background: #eee; }
    button { padding: 6px 12px; margin: 2px; cursor: pointer; border: none; border-radius: 4px; }
    .add { background: #28a745; color: white; }
    .edit { background: #ffc107; }
    .delete { background: #dc3545; color: white; }
    .edit:hover, .add:hover, .delete:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <h1>Catalog Produse</h1>
  <div style="text-align:center; margin-bottom: 10px;">
    <button class="add" onclick="adauga()">Adauga produs</button>
  </div>
  <table id="tabelProduse">
    <tr><th>ID</th><th>Nume</th><th>Pret</th><th>Actiuni</th></tr>
  </table>

<script>
async function incarca() {
  const r = await fetch('/produse');
  const produse = await r.json();
  const tabel = document.getElementById("tabelProduse");
  tabel.innerHTML = '<tr><th>ID</th><th>Nume</th><th>Pret</th><th>Actiuni</th></tr>';
  produse.forEach(p => {
    tabel.innerHTML += `
      <tr>
        <td>${p.id}</td>
        <td>${p.name}</td>
        <td>${p.price} lei</td>
        <td>
          <button class="edit" onclick="modifica(${p.id})">Edit</button>
          <button class="delete" onclick="sterge(${p.id})">Sterge</button>
        </td>
      </tr>`;
  });
}

async function adauga() {
  const nume = prompt("Nume produs:");
  const pret = parseFloat(prompt("Pret:"));
  if (!nume || isNaN(pret)) return alert("Date invalide");
  await fetch('/produse', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: nume, price: pret})
  });
  incarca();
}

async function modifica(id) {
  const nume = prompt("Nume nou:");
  const pret = parseFloat(prompt("Pret nou:"));
  if (!nume || isNaN(pret)) return alert("Date invalide");
  await fetch('/produse/' + id, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: nume, price: pret})
  });
  incarca();
}

async function sterge(id) {
  if (!confirm("Esti sigur ca vrei sa stergi?")) return;
  const r = await fetch('/produse/' + id, {method: 'DELETE'});
  const result = await r.json();
  alert(result.mesaj || result.eroare);
  incarca();
}

window.onload = incarca;
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    if not os.path.exists(FISIER_DATE):
        salveaza_produse([
            {"id": 1, "name": "Laptop", "price": 2000},
            {"id": 2, "name": "Telefon", "price": 1500},
            {"id": 3, "name": "Monitor", "price": 800}
        ])
    app.run(debug=True)
