import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import json, math, random, statistics as st
fp='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=10
OUT='/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad'
raw=json.load(open(f'{OUT}/raw.json'))
random.seed(7)
g0=9.80; FP=4*math.pi**2
BLUE='#1f4e79'; LIGHT='#9dc3e6'; RED='#c0504d'; GREY='#808080'

def style(ax):
    ax.grid(alpha=0.35, ls='-', lw=0.6, color='#d9d9d9'); ax.set_axisbelow(True)
    for s in ('top','right'): ax.spines[s].set_visible(False)

def scatter_raw(ax, x, vals, w, label=None):
    xs=[x+random.uniform(-w,w) for _ in vals]
    ax.plot(xs, vals, 'o', ms=3.2, color=LIGHT, alpha=0.55, mec='none',
            label=label, zorder=2)

# ---------- 그림 : 진폭 - 주기 ----------
ang=[10,20,30,40,50]; keys=['S','A20','A30','A40','A50']
means=[st.mean(raw[k]) for k in keys]
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
for i,(a,k) in enumerate(zip(ang,keys)):
    scatter_raw(ax,a,raw[k],1.6,'측정된 주기 (원시 데이터)' if i==0 else None)
ax.plot(ang,means,'-o',color=BLUE,ms=7,lw=1.8,label='조건별 평균',zorder=4)
for a,m in zip(ang,means):
    ax.annotate(f'{m:.3f}',xy=(a,m),xytext=(0,11),textcoords='offset points',
                ha='center',fontsize=8,color=BLUE,fontweight='bold')
ax.text(30,1.372,'진폭 10° → 50° 에서 주기 약 3.8 % 증가',
        fontsize=9,color=RED,ha='center')
ax.set_xlabel('초기 진폭 θ (°)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(2,58); ax.set_ylim(1.365,1.48); ax.set_xticks(ang)
style(ax); ax.legend(fontsize=8.5,loc='upper left')
fig.tight_layout(); fig.savefig(f'{OUT}/g_amp.png'); plt.close(fig)

# ---------- 그림 : 길이 - 주기 ----------
ls=[0.300,0.500,0.700]; lk=['B300','S','B700']
lm=[st.mean(raw[k]) for k in lk]
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xs=[0.05+0.005*i for i in range(151)]
ax.plot(xs,[2*math.pi*math.sqrt(x/g0) for x in xs],'-',color=GREY,lw=1.5,
        label=r'이론 곡선  $T = 2\pi\sqrt{l/g}$')
for i,(l,k) in enumerate(zip(ls,lk)):
    scatter_raw(ax,l,raw[k],0.016,'측정된 주기 (원시 데이터)' if i==0 else None)
ax.plot(ls,lm,'o',color=BLUE,ms=8,label='조건별 평균',zorder=4)
for l,m in zip(ls,lm):
    ax.annotate(f'{m:.3f} s',xy=(l,m),xytext=(10,-4),textcoords='offset points',
                fontsize=8.5,color=BLUE,fontweight='bold')
ax.set_xlabel('진자 길이 $l$ (m)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(0.15,0.85); ax.set_ylim(0.8,1.9)
style(ax); ax.legend(fontsize=8.5,loc='upper left')
fig.tight_layout(); fig.savefig(f'{OUT}/g_len.png'); plt.close(fig)

# ---------- 그림 : T^2 - l (추세선) ----------
T2=[m*m for m in lm]
n=3; sx=sum(ls); sy=sum(T2); sxx=sum(x*x for x in ls); sxy=sum(x*y for x,y in zip(ls,T2))
slope=(n*sxy-sx*sy)/(n*sxx-sx*sx); icpt=(sy-slope*sx)/n
ybar=sy/n
r2=1-sum((y-(slope*x+icpt))**2 for x,y in zip(ls,T2))/sum((y-ybar)**2 for y in T2)
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xx=[0,0.85]
ax.plot(xx,[slope*x+icpt for x in xx],'--',color=RED,lw=1.5,
        label=f'추세선  $T^2$ = {slope:.3f} $l$ - {abs(icpt):.3f}')
ax.plot(xx,[FP/g0*x for x in xx],'-',color=GREY,lw=1.4,
        label=r'이론 직선  $T^2 = (4\pi^2/g)\,l$ ,  $g$ = 9.80')
ax.plot(ls,T2,'o',color=BLUE,ms=9,zorder=4,label='측정 평균으로 계산한 $T^2$')
for l,t in zip(ls,T2):
    ax.annotate(f'{t:.3f}',xy=(l,t),xytext=(9,-11),textcoords='offset points',
                fontsize=8.5,color=BLUE,fontweight='bold')
ax.text(0.055,2.72,f'$R^2$ = {r2:.4f}\n기울기에서  $g$ = 4$\\pi^2$ / {slope:.3f} = {FP/slope:.2f} m/s$^2$',
        fontsize=9,color='#333333',va='top',
        bbox=dict(boxstyle='round,pad=0.45',fc='#f7f7f7',ec='#bfbfbf',lw=0.8))
ax.set_xlabel('진자 길이 $l$ (m)'); ax.set_ylabel('주기의 제곱 $T^2$ (s$^2$)')
ax.set_xlim(0,0.85); ax.set_ylim(0,3.1)
style(ax); ax.legend(fontsize=8.5,loc='lower right')
fig.tight_layout(); fig.savefig(f'{OUT}/g_len2.png'); plt.close(fig)

# ---------- 그림 : 질량 - 주기 ----------
ms=[59.235,164.955,188.120]; mk=['C1','C2','S']
mm=[st.mean(raw[k]) for k in mk]
fig,ax=plt.subplots(figsize=(6.6,3.6),dpi=200)
for i,(m,k) in enumerate(zip(ms,mk)):
    scatter_raw(ax,m,raw[k],3.0,'측정된 주기 (원시 데이터)' if i==0 else None)
ax.plot(ms,mm,'-o',color=BLUE,ms=8,lw=1.8,label='조건별 평균',zorder=4)
for m,t in zip(ms,mm):
    ax.annotate(f'{t:.3f} s',xy=(m,t),xytext=(0,14),textcoords='offset points',
                ha='center',fontsize=8.5,color=BLUE,fontweight='bold')
ax.axhline(st.mean(mm),color=RED,ls='--',lw=1.3,
           label=f'세 추의 평균 {st.mean(mm):.3f} s')
ax.text(124,1.357,'질량 3.18배 차이 → 주기 차이 0.006 s (약 0.4 %)\n세 추의 주기가 사실상 같다',
        fontsize=9,color=RED,ha='center')
ax.set_xlabel('추의 질량 m (g)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(30,215); ax.set_ylim(1.34,1.45)
style(ax); ax.legend(fontsize=8.5,loc='upper left')
fig.tight_layout(); fig.savefig(f'{OUT}/g_mass.png'); plt.close(fig)
print('charts built;  slope=%.4f  R2=%.5f  g=%.3f'%(slope,r2,FP/slope))
