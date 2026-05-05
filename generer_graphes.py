import json
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DOSSIER_RESULTATS = "complexite"

with open(os.path.join(DOSSIER_RESULTATS, "resultats.json"), 'r') as f:
    res = json.load(f)

tailles = res['tailles']
NB_TESTS = res['nb_runs']

def trace_nuage(donnees, label, fichier, ylabel="Temps (s)"):
    fig, ax = plt.subplots(figsize=(10, 7))
    couleurs = ['blue', 'red', 'green', 'orange']
    for i, n in enumerate(tailles):
        vals = donnees[str(n)]
        ax.scatter([n] * len(vals), vals, alpha=0.5, s=30, color=couleurs[i], label=f'n={n}')
    maxs = [max(donnees[str(n)]) for n in tailles]
    ax.plot(tailles, maxs, 'r-', label='Maximum (pire cas)', linewidth=2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Taille n')
    ax.set_ylabel(ylabel)
    ax.set_title(f'Nuage de points - {label}')
    ax.legend(loc='upper left')
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DOSSIER_RESULTATS, fichier), dpi=120)
    plt.close()
    print(f"Généré: {fichier}")


def total(d1, d2):
    return {str(n): [a + b for a, b in zip(d1[str(n)], d2[str(n)])] for n in tailles}


print("Génération des graphiques...")

trace_nuage(res['theta_no'], r'Temps initialisation - Methode Nord-Ouest', 'nuage_theta_no.png')
trace_nuage(res['theta_bh'], r'Temps initialisation - Methode Balas-Hammer', 'nuage_theta_bh.png')
trace_nuage(res['t_no'], r'Temps optimisation - Marche-pied ( depuis Nord-Ouest )', 'nuage_t_no.png')
trace_nuage(res['t_bh'], r'Temps optimisation - Marche-pied ( depuis Balas-Hammer )', 'nuage_t_bh.png')

theta_t_no = total(res['theta_no'], res['t_no'])
theta_t_bh = total(res['theta_bh'], res['t_bh'])
trace_nuage(theta_t_no, r'Temps total - Nord-Ouest + Marche-pied', 'nuage_total_no.png')
trace_nuage(theta_t_bh, r'Temps total - Balas-Hammer + Marche-pied', 'nuage_total_bh.png')

fig, ax = plt.subplots(figsize=(11, 8))
m_theta_no = [max(res['theta_no'][str(n)]) for n in tailles]
m_theta_bh = [max(res['theta_bh'][str(n)]) for n in tailles]
m_t_no = [max(res['t_no'][str(n)]) for n in tailles]
m_t_bh = [max(res['t_bh'][str(n)]) for n in tailles]
m_tot_no = [max(theta_t_no[str(n)]) for n in tailles]
m_tot_bh = [max(theta_t_bh[str(n)]) for n in tailles]

ax.plot(tailles, m_theta_no, 'o-', color='blue', label='Theta Nord-Ouest')
ax.plot(tailles, m_theta_bh, 's-', color='red', label='Theta Balas-Hammer')
ax.plot(tailles, m_t_no, '^-', color='green', label='Temps Nord-Ouest')
ax.plot(tailles, m_t_bh, 'v-', color='orange', label='Temps Balas-Hammer')
ax.plot(tailles, m_tot_no, 'd--', color='purple', label='Total Nord-Ouest')
ax.plot(tailles, m_tot_bh, 'p--', color='brown', label='Total Balas-Hammer')

n_arr = np.array(tailles, dtype=float)
ref_n2 = (max(m_theta_no) / max(n_arr) ** 2) * n_arr ** 2
ax.plot(tailles, ref_n2, 'k:', alpha=0.5, label='Reference O(n^2)')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Taille n')
ax.set_ylabel('Temps maximum (secondes)')
ax.set_title('Comparaison des temps - Methode Nord-Ouest vs Balas-Hammer')
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(DOSSIER_RESULTATS, 'comparaison_pire_cas.png'), dpi=120)
plt.close()
print("Généré: comparaison_pire_cas.png")

fig, ax = plt.subplots(figsize=(10, 7))
couleurs = ['blue', 'red', 'green', 'orange']
for i, n in enumerate(tailles):
    no = theta_t_no[str(n)]
    bh = theta_t_bh[str(n)]
    ratios = [a / b if b > 1e-9 else 0 for a, b in zip(no, bh)]
    ax.scatter([n] * len(ratios), ratios, alpha=0.5, s=30, color=couleurs[i], label=f'n={n}')
m_ratios = []
for n in tailles:
    no = theta_t_no[str(n)]
    bh = theta_t_bh[str(n)]
    ratios = [a / b if b > 1e-9 else 0 for a, b in zip(no, bh)]
    m_ratios.append(max(ratios))
ax.plot(tailles, m_ratios, 'b-', label='Ratio max (NO/BH)', linewidth=2)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Equivalence (ratio=1)')
ax.set_xscale('log')
ax.set_xlabel('Taille n')
ax.set_ylabel(r'Ratio temps total (NO / BH)')
ax.set_title('Comparaison performance: Methode Nord-Ouest vs Balas-Hammer')
ax.legend()
ax.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(DOSSIER_RESULTATS, 'ratio_no_bh.png'), dpi=120)
plt.close()
print("Généré: ratio_no_bh.png")

print("\nTerminé! Fichiers générés:")
for f in sorted(os.listdir(DOSSIER_RESULTATS)):
    if f.endswith('.png'):
        print(f"  - {f}")