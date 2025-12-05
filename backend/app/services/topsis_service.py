# app/services/topsis_service.py

import numpy as np

class TopsisService:

    @staticmethod
    def evaluar(matriz, pesos, tipos):
        X = np.array(matriz, dtype=float)
        pesos = np.array(pesos, dtype=float)

        # normalizar
        norma = np.sqrt((X**2).sum(axis=0))
        Xn = X / norma

        # ponderar
        V = Xn * pesos

        # ideal (+ / -)
        ideal_pos = np.max(V, axis=0)
        ideal_neg = np.min(V, axis=0)

        d_pos = np.sqrt(((V - ideal_pos)**2).sum(axis=1))
        d_neg = np.sqrt(((V - ideal_neg)**2).sum(axis=1))

        score = d_neg / (d_pos + d_neg)
        ranking = np.argsort(score)[::-1]

        return {
            "score": score.tolist(),
            "ranking": ranking.tolist()
        }
