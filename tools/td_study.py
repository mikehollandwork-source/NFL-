"""What predicts a skill player scoring a TD? Out-of-sample study on nflverse
play-by-play: trailing same-season usage features -> logistic regression,
trained on earlier seasons, scored on later ones (log-loss vs base)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nfl_proj.td_model import *  # noqa: F401,F403
from nfl_proj.td_model import MODEL


def main(seasons=range(2021, 2026)):
    g = rows(seasons)
    g["y"] = (g["tds"] > 0).astype(float)
    eps = 1e-9
    g["sh_tgt"] = g["m_tgt"] / (g["m_T_tgt"] + eps)
    g["sh_car"] = g["m_car"] / (g["m_T_car"] + eps)
    g["sh_rz"] = (g["m_rz_tgt"] + g["m_rz_car"]) / (g["m_T_rz_tgt"] + g["m_T_rz_car"] + eps)
    g["sh_i10"] = (g["m_i10_tgt"] + g["m_i5_car"]) / (g["m_T_i10_tgt"] + g["m_T_i5_car"] + eps)
    g["sh_ez"] = g["m_ez_tgt"] / (g["m_T_ez_tgt"] + eps)
    g["sh_deep"] = g["m_deep_tgt"] / (g["m_tgt"] + eps)
    g["log_impl"] = np.log(g["implied"].clip(3))
    sets = {
        "volume (targets, carries per game)": ["m_tgt", "m_car"],
        "+ red-zone touches/game": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car"],
        "+ inside-10 / inside-5": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car"],
        "+ end-zone targets": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt"],
        "+ team implied points": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl"],
        "+ team TDs & opp TDs allowed (no market)": FEATS,
        "+ TD rate so far": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "m_tds"],
        "+ last-week end-zone incompletions": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "ez_inc_last"],
        "+ deep share, air yards": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "sh_deep", "m_ay"],
        "shares instead of counts": ["sh_tgt", "sh_car", "sh_rz", "sh_i10", "sh_ez", "log_impl", "m_T_tds"],
    }
    out = []
    for test in sorted(g["season"].unique())[2:]:
        tr, te = g[g["season"] < test], g[g["season"] == test]
        base = ll(te["y"].values, np.full(len(te), tr["y"].mean()))
        for name, f in sets.items():
            mu, sd = tr[f].mean(), tr[f].std() + 1e-9
            b = fit_logit(((tr[f] - mu) / sd).values, tr["y"].values)
            p = pred(b, ((te[f] - mu) / sd).values)
            out.append({"test": test, "set": name, "logloss": ll(te["y"].values, p), "base": base, "n": len(te)})
    r = pd.DataFrame(out)
    piv = r.pivot(index="set", columns="test", values="logloss")
    piv["mean"] = piv.mean(axis=1)
    piv = piv.loc[list(sets)]
    print(f"rows {len(g)}, scored-rate {g['y'].mean():.3f}")
    print(piv.round(4).to_string())
    # final model on all but last season: coefficient view
    f = sets["+ team implied points"]
    mu, sd = g[f].mean(), g[f].std()
    b = fit_logit(((g[f] - mu) / sd).values, g["y"].values)
    print("standardized coefficients:", dict(zip(f, np.round(b[1:], 3))))
    pass
    return g, r


def save(seasons=range(2021, 2026)):
    import json
    g = rows(seasons)
    mu, sd = g[FEATS].mean(), g[FEATS].std()
    b = fit_logit(((g[FEATS] - mu) / sd).values, g["y"].values)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_text(json.dumps({"features": FEATS, "mu": mu.to_dict(), "sd": sd.to_dict(), "b": b.tolist(),
                                 "seasons": [int(s) for s in seasons], "n": int(len(g))}, indent=1))
    print(f"saved {MODEL} ({len(g)} player-games)")


if __name__ == "__main__":
    save() if "--save" in sys.argv else main()
