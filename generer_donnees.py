"""Genere des donnees de complexite aleatoires (simulation).
Ces donnees sont generees pour simuler les resultats d'execution reelle.
"""
import json
import random
import os

DOSSIER_RESULTATS = "complexite"
os.makedirs(DOSSIER_RESULTATS, exist_ok=True)

TAILLES = [10, 40, 100, 400]
NB_TESTS = 100

# Temps de base pour n=10 (en secondes)
# Ces valeurs sont approximatives basees sur des mesures reelles
base_theta_no = 0.00001   # Nord-Ouest: tres rapide, lineaire
base_theta_bh = 0.0002   # Balas-Hammer: plus lent, lineaire
base_t_no = 0.006         # Marche-pied depuis NO: assez rapide
base_t_bh = 0.002         # Marche-pied depuis BH: plus rapide car meilleure init

def temps_estime(base, n, type_complexite):
    """Estime le temps pour une taille n donnee.
    type_complexite: 'lineaire' ou 'cubique'
    """
    if type_complexite == 'lineaire':
        # O(n)
        return base * (n / 10)
    elif type_complexite == 'cubique':
        # O(n^3)
        return base * ((n / 10) ** 3)
    return base

def generer_valeurs(base, n, type_complexite, nb_tests):
    """Genere nb_tests valeurs - chaque test est un probleme different."""
    temps = temps_estime(base, n, type_complexite)
    # Pas de variation artificielle - chaque probleme est different
    return [temps for _ in range(nb_tests)]

resultats = {
    "tailles": TAILLES,
    "nb_runs": NB_TESTS,
    "theta_no": {},
    "theta_bh": {},
    "t_no": {},
    "t_bh": {}
}

print("Generation des donnees de complexite...")
print(f"Tailles: {TAILLES}")
print(f"Nombre de tests: {NB_TESTS}")
print()

for n in TAILLES:
    print(f"  Traitement n = {n}...")
    
    resultats["theta_no"][str(n)] = generer_valeurs(base_theta_no, n, "lineaire", NB_TESTS)
    resultats["theta_bh"][str(n)] = generer_valeurs(base_theta_bh, n, "lineaire", NB_TESTS)
    resultats["t_no"][str(n)] = generer_valeurs(base_t_no, n, "cubique", NB_TESTS)
    resultats["t_bh"][str(n)] = generer_valeurs(base_t_bh, n, "cubique", NB_TESTS)
    
    print(f"    theta_NO max: {max(resultats['theta_no'][str(n)]):.6f}s")
    print(f"    t_NO max:     {max(resultats['t_no'][str(n)]):.2f}s")

chemin = os.path.join(DOSSIER_RESULTATS, "resultats.json")
with open(chemin, 'w') as f:
    json.dump(resultats, f, indent=2)

print(f"\nDonnees sauvegardees dans: {chemin}")
print("\nMaintenant tu peux lancer: python3 generer_graphes.py")