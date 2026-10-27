"""Refit probability calibration by stat family and side on backtest sides,
score it out of sample (2026 backtest + week 6 real lines). Run from the repo root."""
import sys,glob;sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from pathlib import Path
from nfl_proj.cli import load_cfg,_paths
from nfl_proj.build import load_season
from nfl_proj.picks import STATS
def load(fs):
    d=pd.concat([pd.read_csv(f) for f in fs]); d=d[d.actual.notna()&(d.actual!=d.line)]
    return d
tr=load(['output/2025/backtest_V1_25early_paper_ev.csv','output/2025/backtest_F25_final_paper_ev.csv'])
te=load(['output/2026/backtest_V1_final_paper_ev.csv'])
# week 6 real
cfg=load_cfg(Path('config/projection.toml'));t=load_season(_paths(cfg)['db'])
pw=t['player_games'];pw=pw[pw.week==6]
w6=pd.concat([pd.read_csv(f) for f in glob.glob('output/2026/paper/week_06_all_lines_evaluated*.csv')])
w6=w6.merge(pw[['player_id']+[c for c in set(v[0] for v in STATS.values())]],on='player_id',how='inner')
w6['actual']=[getattr(r,STATS[r.stat][0]) for r in w6.itertuples()]
w6=w6[w6.actual!=w6.line]; w6['won']=np.where(w6.side=='over',w6.actual>w6.line,w6.actual<w6.line).astype(float)
print('train',len(tr),tr.week.min(),tr.week.max(),'test26',len(te),te.week.unique(),'w6',len(w6))
lg=lambda p:np.log(np.clip(p,1e-4,1-1e-4)/(1-np.clip(p,1e-4,1-1e-4)))
sig=lambda x:1/(1+np.exp(-x))
def fit(d):
    x=lg(d.p_model.values);y=d.won.values
    X=np.c_[np.ones_like(x),x];b=np.zeros(2)
    for _ in range(50):
        p=sig(X@b);g=X.T@(y-p);H=(X*(p*(1-p))[:,None]).T@X;b=b+np.linalg.solve(H+1e-9*np.eye(2),g)
    return b
def ll(d,p): y=d.won.values;p=np.clip(p,1e-4,1-1e-4);return -np.mean(y*np.log(p)+(1-y)*np.log(1-p))
fam=lambda s:{'receptions':'rec','targets':'rec','rec_yds':'rec','rush_yds':'rush','carries':'rush','pass_yds':'qb','completions':'qb','pass_att':'qb'}.get(s,'other')
for d in (tr,te,w6): d['grp_side']=d.side; d['grp_fam']=d.stat.map(fam)+'_'+d.side
schemes={'current':None,'global':[],'side':['grp_side'],'fam_side':['grp_fam']}
res={}
for name,g in schemes.items():
    out={}
    for tag,d in (('2026wk4-5 stand-in',te),('week6 real',w6),('train',tr)):
        if name=='current': p=sig(0.13+0.45*lg(d.p_model.values))
        elif not g: ab=fit(tr); p=sig(ab[0]+ab[1]*lg(d.p_model.values))
        else:
            p=np.zeros(len(d))
            for k,idx in d.groupby(g).groups.items():
                trk=tr[tr[g[0]]==k]; ab=fit(trk) if len(trk)>50 else fit(tr)
                m=d.index.isin(idx) if False else (d[g[0]]==k).values
                p[m]=sig(ab[0]+ab[1]*lg(d.p_model.values[m]))
        d['p_'+name]=p
        out[tag]=round(ll(d,p),4)
    res[name]=out
print(pd.DataFrame(res).T)
for k,trk in tr.groupby('grp_fam'): print(k,len(trk),fit(trk).round(3))
print('side',{k:fit(v).round(3) for k,v in tr.groupby('side')})
# betting rule outcome on test sets with each scheme: lean p>=th, ROI at -115
for tag,d in (('2026wk4-5',te),('week6 real',w6)):
    for name in schemes:
        p=d['p_'+name]
        for th in (.54,.6):
            m=p>=th; x=d[m]; 
            if len(x): print(tag,name,th,len(x),round(x.won.mean(),3),f"{(x.won.mean()*(1+100/115)-1)*100:+.1f}%")
print('--- intercept scale test (fam_side slope, side intercept scaled)')
fits={k:fit(v) for k,v in tr.groupby('grp_fam')}
for sc in (0,.25,.5,.75,1,1.25):
    out=[]
    for tag,d in (('2026wk4-5',te),('week6 real',w6)):
        p=np.array([sig(sc*fits[g][0]+fits[g][1]*x) for g,x in zip(d.grp_fam,lg(d.p_model.values))])
        out.append(round(ll(d,p),4))
    print(sc,out)
# bootstrap week-6 improvement side vs current
rng=np.random.default_rng(0);diffs=[]
games=w6.game.unique()
for _ in range(1000):
    gs=rng.choice(games,len(games));dd=pd.concat([w6[w6.game==g] for g in gs])
    diffs.append(ll(dd,dd.p_current.values)-ll(dd,dd.p_fam_side.values))
print('w6 gain mean',np.mean(diffs).round(4),'P(gain>0)',np.mean(np.array(diffs)>0))
print('--- thresholds with sc=0.75')
for tag,d in (('2025 train',tr),('2026wk4-5',te),('week6 real',w6)):
    p=np.array([sig(.75*fits[g][0]+fits[g][1]*x) for g,x in zip(d.grp_fam,lg(d.p_model.values))]); d['pn']=p
    for th in (.52,.54,.56,.58,.6,.62):
        x=d[p>=th]; print(tag,th,len(x),round(x.won.mean(),3),f"{(x.won.mean()*(1+100/115)-1)*100:+.1f}%", 'overs',int((x.side=='over').sum()))
for k,v in fits.items(): print(k, (0.75*v[0]).round(3), v[1].round(3))
print('--- per-stat fits')
for st,v in tr.groupby('stat'):
    ov=v[v.side=='over']; print(st,len(ov),fit(ov).round(3))
fam2=lambda s:{'carries':'car','rush_yds':'rush','receptions':'rec','targets':'rec','rec_yds':'rec','pass_yds':'qb','completions':'qb'}[s]
for d in (tr,te,w6): d['f2']=d.stat.map(fam2)+'_'+d.side
f2={k:fit(v) for k,v in tr.groupby('f2')}
for name,key,F in (('fam',  'grp_fam',fits),('fam+carries','f2',f2)):
    out=[]
    for tag,d in (('26',te),('w6',w6)):
        p=np.array([sig(.75*F[g][0]+F[g][1]*x) for g,x in zip(d[key],lg(d.p_model.values))]); out.append(round(ll(d,p),4))
        c=d[d.stat=='carries'];pc=p[(d.stat=='carries').values]; out.append(('car',round(ll(c,pc),4)))
    print(name,out)
c=te[te.stat=='carries'];print('26 carries current',round(ll(c,c.p_current.values),4))
c=w6[w6.stat=='carries'];print('w6 carries current',round(ll(c,c.p_current.values),4), len(c))
print({k:(0.75*v[0]).round(3) for k,v in f2.items()}, {k:v[1].round(3) for k,v in f2.items()})
