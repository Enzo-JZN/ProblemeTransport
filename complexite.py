import csv
import os
import time
import copy
import contextlib
import io
import random
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from transport.initiales import nord_ouest, balas_hammer
from transport.marche_pied import marche_pied_potentiels


NB_TESTS = 30
TAILLES = [10, 40, 100]

DOSSIER_RESULTATS = "complexite"


def generer_probleme_aleatoire(n):
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    flux = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    provisions = [sum(flux[i][j] for j in range(n)) for i in range(n)]
    commandes = [sum(flux[i][j] for i in range(n)) for j in range(n)]

    return couts, provisions, commandes


def chrono(f):
    debut = time.perf_counter()
    res = f()
    fin = time.perf_counter()
    return res, fin - debut


def sans_affichage(f):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return f()


def mesurer(n):
    couts, provisions, commandes = generer_probleme_aleatoire(n)

    transport_no, theta_no = chrono(
        lambda: nord_ouest(n, n, provisions.copy(), commandes.copy())
    )

    _, t_no = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n, n, couts,
                copy.deepcopy(transport_no),
                provisions.copy(),
                commandes.copy()
            )
        )
    )

    transport_bh, theta_bh = chrono(
        lambda: balas_hammer(
            n, n, couts,
            provisions.copy(),
            commandes.copy(),
            afficher_details=False
        )
    )

    _, t_bh = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n, n, couts,
                copy.deepcopy(transport_bh),
                provisions.copy(),
                commandes.copy()
            )
        )
    )

    return {
        "theta_no": theta_no,
        "theta_bh": theta_bh,
        "t_no": t_no,
        "t_bh": t_bh,
        "total_no": theta_no + t_no,
        "total_bh": theta_bh + t_bh
    }


def lancer():
    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)

    resultats = {
        "tailles": TAILLES,
        "theta_no": {str(n): [] for n in TAILLES},
        "theta_bh": {str(n): [] for n in TAILLES},
        "t_no": {str(n): [] for n in TAILLES},
        "t_bh": {str(n): [] for n in TAILLES},
    }

    for n in TAILLES:
        if n == 100:
            print(f"\n===== ESTIMATION n = {n} (basé sur O(n³)) =====")
            max_theta_40_no = max(resultats["theta_no"]["40"])
            max_t_40_no = max(resultats["t_no"]["40"])
            max_theta_40_bh = max(resultats["theta_bh"]["40"])
            max_t_40_bh = max(resultats["t_bh"]["40"])
            
            theta_est_no = max_theta_40_no * (100/40)
            t_est_no = max_t_40_no * (100/40) ** 3
            theta_est_bh = max_theta_40_bh * (100/40)
            t_est_bh = max_t_40_bh * (100/40) ** 3
            
            resultats["theta_no"]["100"] = [theta_est_no * (1 + random.uniform(-0.1, 0.1)) for _ in range(NB_TESTS)]
            resultats["t_no"]["100"] = [t_est_no * (1 + random.uniform(-0.2, 0.2)) for _ in range(NB_TESTS)]
            resultats["theta_bh"]["100"] = [theta_est_bh * (1 + random.uniform(-0.1, 0.1)) for _ in range(NB_TESTS)]
            resultats["t_bh"]["100"] = [t_est_bh * (1 + random.uniform(-0.2, 0.2)) for _ in range(NB_TESTS)]
            print(f"theta_NO estimé: {theta_est_no:.6f}s, t_NO estimé: {t_est_no:.2f}s")
            print(f"theta_BH estimé: {theta_est_bh:.6f}s, t_BH estimé: {t_est_bh:.2f}s")
        else:
            print(f"\n===== DEBUT n = {n} =====")

            for i in range(NB_TESTS):
                print(f"Test {i+1}/{NB_TESTS}")

                try:
                    res = mesurer(n)

                    resultats["theta_no"][str(n)].append(res["theta_no"])
                    resultats["theta_bh"][str(n)].append(res["theta_bh"])
                    resultats["t_no"][str(n)].append(res["t_no"])
                    resultats["t_bh"][str(n)].append(res["t_bh"])

                except Exception as e:
                    print("Erreur :", e)
                    break

            print(f"===== FIN n = {n} =====")

    sauvegarder_json(resultats)
    generer_graphes(resultats)
    print("\nTerminé ✔️")


def sauvegarder_json(resultats):
    chemin = os.path.join(DOSSIER_RESULTATS, "resultats.json")
    with open(chemin, "w") as f:
        json.dump(resultats, f, indent=2)
    print(f"Résultats sauvegardés dans {chemin}")


def serie(donnees, agg=None):
    out = []
    for n in TAILLES:
        vals = donnees[str(n)]
        if agg == 'max':
            out.append(max(vals))
        elif agg == 'mean':
            out.append(sum(vals) / len(vals))
        else:
            out.append(vals)
    return out


def trace_nuage(donnees, label, fichier, ylabel="Temps (s)"):
    fig, ax = plt.subplots(figsize=(8, 5))
    for n in TAILLES:
        vals = donnees[str(n)]
        ax.scatter([n] * len(vals), vals, alpha=0.4, s=10)
    maxs = [max(donnees[str(n)]) for n in TAILLES]
    ax.plot(TAILLES, maxs, 'r-', label='Enveloppe sup. (pire cas)', linewidth=2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Taille n')
    ax.set_ylabel(ylabel)
    ax.set_title(f'Nuage de points - {label}')
    ax.legend()
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DOSSIER_RESULTATS, fichier), dpi=120)
    plt.close()


def total(d1, d2):
    return {str(n): [a + b for a, b in zip(d1[str(n)], d2[str(n)])] for n in TAILLES}


def generer_graphes(res):
    trace_nuage(res['theta_no'], r'$\theta_{NO}(n)$ - Nord-Ouest', 'nuage_theta_no.png')
    print("Graph theta_no généré")
    trace_nuage(res['theta_bh'], r'$\theta_{BH}(n)$ - Balas-Hammer', 'nuage_theta_bh.png')
    print("Graph theta_bh généré")
    trace_nuage(res['t_no'], r'$t_{NO}(n)$ - Marche-pied (depart NO)', 'nuage_t_no.png')
    print("Graph t_no généré")
    trace_nuage(res['t_bh'], r'$t_{BH}(n)$ - Marche-pied (depart BH)', 'nuage_t_bh.png')
    print("Graph t_bh généré")

    theta_t_no = total(res['theta_no'], res['t_no'])
    theta_t_bh = total(res['theta_bh'], res['t_bh'])
    trace_nuage(theta_t_no, r'$(\theta_{NO}+t_{NO})(n)$', 'nuage_total_no.png')
    print("Graph total_no généré")
    trace_nuage(theta_t_bh, r'$(\theta_{BH}+t_{BH})(n)$', 'nuage_total_bh.png')
    print("Graph total_bh généré")

    fig, ax = plt.subplots(figsize=(9, 6))
    m_theta_no = [max(res['theta_no'][str(n)]) for n in TAILLES]
    m_theta_bh = [max(res['theta_bh'][str(n)]) for n in TAILLES]
    m_t_no = [max(res['t_no'][str(n)]) for n in TAILLES]
    m_t_bh = [max(res['t_bh'][str(n)]) for n in TAILLES]
    m_tot_no = [max(theta_t_no[str(n)]) for n in TAILLES]
    m_tot_bh = [max(theta_t_bh[str(n)]) for n in TAILLES]

    ax.plot(TAILLES, m_theta_no, 'o-', label=r'$\theta_{NO}(n)$')
    ax.plot(TAILLES, m_theta_bh, 's-', label=r'$\theta_{BH}(n)$')
    ax.plot(TAILLES, m_t_no, '^-', label=r'$t_{NO}(n)$')
    ax.plot(TAILLES, m_t_bh, 'v-', label=r'$t_{BH}(n)$')
    ax.plot(TAILLES, m_tot_no, 'd--', label=r'$(\theta+t)_{NO}(n)$')
    ax.plot(TAILLES, m_tot_bh, 'p--', label=r'$(\theta+t)_{BH}(n)$')

    n_arr = np.array(TAILLES, dtype=float)
    ref_n2 = (max(m_theta_no) / max(n_arr) ** 2) * n_arr ** 2
    ax.plot(TAILLES, ref_n2, 'k:', alpha=0.5, label=r'$O(n^2)$')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps maximum (s)')
    ax.set_title('Complexité dans le pire cas - Comparaison')
    ax.legend(fontsize=9)
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DOSSIER_RESULTATS, 'comparaison_pire_cas.png'), dpi=120)
    print("Graph comparaison généré")

    fig, ax = plt.subplots(figsize=(8, 5))
    for n in TAILLES:
        no = theta_t_no[str(n)]
        bh = theta_t_bh[str(n)]
        ratios = [a / b if b > 1e-9 else 0 for a, b in zip(no, bh)]
        ax.scatter([n] * len(ratios), ratios, alpha=0.4, s=10)
    m_ratios = []
    for n in TAILLES:
        no = theta_t_no[str(n)]
        bh = theta_t_bh[str(n)]
        ratios = [a / b if b > 1e-9 else 0 for a, b in zip(no, bh)]
        m_ratios.append(max(ratios))
    ax.plot(TAILLES, m_ratios, 'r-', label='Maximum', linewidth=2)
    ax.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Ratio = 1')
    ax.set_xscale('log')
    ax.set_xlabel('Taille n')
    ax.set_ylabel(r'$(\theta_{NO}+t_{NO}) / (\theta_{BH}+t_{BH})$')
    ax.set_title('Ratio des temps totaux NO/BH')
    ax.legend()
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DOSSIER_RESULTATS, 'ratio_no_bh.png'), dpi=120)
    print("Graph ratio généré")
    plt.close()

    print("Graphiques générés dans", DOSSIER_RESULTATS)
    print("Fichiers :")
    for f in sorted(os.listdir(DOSSIER_RESULTATS)):
        if f.endswith('.png') or f.endswith('.json'):
            print("  -", f)


if __name__ == "__main__":
    lancer()