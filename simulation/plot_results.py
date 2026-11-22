import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
def load(f):
    d=np.loadtxt(f, skiprows=1); return d[:,0]*1e9, d[:,1]
# Figure 1: Rs sweep
plt.figure(figsize=(8,4.5))
for rs in ['1','4.7','10','22','47']:
    t,v=load(f'sweep_{rs}'); plt.plot(t,v,label=f'Rs = {rs} ohm',lw=1.3)
plt.axhline(0,color='k',lw=0.5); plt.axhline(-0.5,color='r',ls=':',lw=0.8,label='-0.5 V abs. min (typ.)')
plt.axvspan(5,15,color='0.9',label='gate on (10 ns)')
plt.xlim(0,60); plt.xlabel('time (ns)'); plt.ylabel('target node V')
plt.title('Crowbar node vs Rs (3.3 V rail, decoupling removed)\nfirst-order model, Lsrc=50 nH, Cnode=225 pF')
plt.legend(fontsize=8,loc='lower right'); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig('crowbar-node-rs-sweep.png',dpi=130)
# Figure 2: decoupling removed vs present
plt.figure(figsize=(8,4.5))
t,v=load('dec_removed'); plt.plot(t,v,label='decoupling removed (Cnode 225 pF)',lw=1.5)
t,v=load('dec_present'); plt.plot(t,v,label='decoupling present (100 nF)',lw=1.5)
plt.axhline(0,color='k',lw=0.5); plt.axvspan(5,15,color='0.9',label='gate on (10 ns)')
plt.xlim(0,60); plt.xlabel('time (ns)'); plt.ylabel('target node V')
plt.title('Why the decoupling is removed (Rs = 10 ohm, 3.3 V rail)')
plt.legend(fontsize=9); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig('crowbar-node-decoupling.png',dpi=130)
print("plots written")
