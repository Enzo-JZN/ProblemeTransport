# Projet de Recherche Opérationnelle - Problème de Transport

## Introduction

Ce projet implémente la résolution du problème de transport avec plusieurs méthodes :
- **Algorithme du Nord-Ouest** (initialisation simple)
- **Algorithme de Balas-Hammer** (initialisation optimisée)
- **Méthode du marchepied avec potentiels** (optimisation)

## Structure du projet

```
projet_transport-main/
├── main.py                    # Point d'entrée - menu interactif
├── complexite.py             # Script d'analyse de complexité
├── generer_donnees.py         # Génère des données simulées
├── generer_graphes.py         # Génère les graphiques
├── generer_traces.py          # Génère les traces d'exécution
├── transport/                 # Module des algorithmes
│   ├── initiales.py          # Nord-Ouest & Balas-Hammer
│   ├── marche_pied.py        # Méthode du marchepied
│   ├── potentiels.py         # Calcul des potentiels
│   ├── graphe.py             # Gestion cycles & connexité
│   ├── io_affichage.py       # Affichage des tableaux
│   └── menu.py               # Interface menu
├── problemes/                 # Les 12 fichiers de problèmes
├── traces/                   # Les traces d'exécution
└── complexite/               # Résultats & graphiques
    └── *.png                 # 8 graphiques de complexité
```

## Comment utiliser

### 1. Lancer le programme principal

```bash
python3 main.py
```

Permet de résoudre un problème de transport avec choix de la méthode d'initialisation.

### 2. Générer des données de complexité

```bash
python3 generer_donnees.py
```

Génère des données simulées (sans exécuter les vrais algorithmes).

### 3. Générer les graphiques

```bash
python3 generer_graphes.py
```

Crée les 8 graphiques PNG dans le dossier `complexite/`.

### 4. Analyse de complexité (vraie exécution)

```bash
python3 complexite.py
```

**Attention** : Very long pour les grandes valeurs de n (plusieurs heures).

## Les algorithmes

### Nord-Ouest (θ_NO)
- **Complexité** : O(n²)
- **Principe** : Remplissage en escalier depuis le coin supérieur gauche

### Balas-Hammer (θ_BH)
- **Complexité** : O(n³)
- **Principe** : Calcul des pénalités à chaque étape pour choisir la meilleure case

### Marchepied (t_NO / t_BH)
- **Complexité** : O(n⁴) avec NO, O(n³) avec BH
- **Principe** : Itérations jusqu'à l'optimum en utilisant les potentiels

## Résultats de complexité

| Algorithme | Complexité | Observations |
|------------|------------|--------------|
| θ_NO | O(n²) | Linéaire en pratique, dominé par l'initialisation |
| θ_BH | O(n³) | Croissance rapide |
| t_NO | O(n²) à O(n⁴) | Dépend du nombre d'itérations |
| t_BH | O(n²) à O(n³) | Meilleure convergence avec BH |

## Graphiques générés

1. `nuage_theta_no.png` - Temps init Nord-Ouest
2. `nuage_theta_bh.png` - Temps init Balas-Hammer
3. `nuage_t_no.png` - Temps marchepied après NO
4. `nuage_t_bh.png` - Temps marchepied après BH
5. `nuage_total_no.png` - Temps total avec NO
6. `nuage_total_bh.png` - Temps total avec BH
7. `comparaison_pire_cas.png` - Comparaison avec O(n²)
8. `ratio_no_bh.png` - Ratio NO/BH

## Équipe

- Jin Johnny
- Eric Eung
- Hugo Juzyna
- Enzo Juzyna
- James Him
- Léa Marachli

## Annexe : Compilation descomplexités

| Partie | Complexité |
|--------|------------|
| Initialisation matrice | O(n²) |
| Calcul pénalités | O(n²) |
| Calcul potentiels | O(n²) |
| Coûts marginaux | O(n²) |
| Une itération marchepied | O(n²) |
| Itérations (NO) | O(n²) |
| Itérations (BH) | O(n) |
| **Marchepied NO** | **O(n⁴)** |
| **Marchepied BH** | **O(n³)** |
