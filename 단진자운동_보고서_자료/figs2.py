import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import math
fp='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=10
OUT='/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad'
g0=9.80; FP=4*math.pi**2
BLUE='#1f4e79'; RED='#c0504d'; GREY='#9aa0a6'

def Tth(l): return 2*math.pi*math.sqrt(l/g0)
T0=Tth(0.500)

# ---------- 그림 2 : 진폭 - 주기 ----------
ang=[10,20,30,40,50]; Tm=[1.3960,1.4000,1.4140,1.4300,1.4480]
sd =[0.0055,0.0000,0.0055,0.0000,0.0045]
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xs=[i*0.5 for i in range(0,121)]
def kfac(a):
    s=math.sin(math.radians(a)/2); return 1+s**2/4+9*s**4/64
ax.axhline(T0,color=GREY,lw=1.6,label='소각 근사 이론값  $T_0$ = 1.4192 s (진폭 무관)')
ax.plot(xs,[T0*kfac(a) for a in xs],'--',color=RED,lw=1.4,
        label='유한 진폭까지 고려한 이론값')
ax.errorbar(ang,Tm,yerr=sd,fmt='o',ms=6,color=BLUE,capsize=4,lw=1.2,label='측정 평균 (5회)')
for a,t in zip(ang,Tm):
    ax.annotate(f'{t:.3f}',xy=(a,t),xytext=(0,-15),textcoords='offset points',
                ha='center',fontsize=7.5,color=BLUE)
ax.set_xlabel('초기 진폭 θ (°)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(0,60); ax.set_ylim(1.37,1.51); ax.set_xticks(range(0,61,10))
ax.grid(alpha=0.3,ls=':'); ax.legend(fontsize=8.3,loc='upper left')
fig.tight_layout(); fig.savefig(f'{OUT}/fig_a.png'); plt.close(fig)

# ---------- 그림 3 : T^2 - l ----------
ls=[0.300,0.500,0.700]; T2=[1.0900**2,1.3960**2,1.6680**2]
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xx=[0,0.8]
ax.plot(xx,[FP/g0*x for x in xx],'-',color=GREY,lw=1.6,
        label=r'이론 직선  $T^2 = (4\pi^2/g)\,l$,  $g$ = 9.80')
ax.plot(xx,[3.9853*x-0.01961 for x in xx],'--',color=RED,lw=1.4,
        label='측정값을 지나는 직선 (기울기 3.985)')
ax.plot(ls,T2,'o',ms=7,color=BLUE,label='측정값')
for l,t in zip(ls,T2):
    ax.annotate(f'{t:.3f}',xy=(l,t),xytext=(7,-10),textcoords='offset points',
                fontsize=7.8,color=BLUE)
ax.set_xlabel('진자 길이 $l$ (m)'); ax.set_ylabel('주기의 제곱 $T^2$ (s$^2$)')
ax.set_xlim(0,0.8); ax.set_ylim(0,3.3)
ax.grid(alpha=0.3,ls=':'); ax.legend(fontsize=8.3,loc='upper left')
fig.tight_layout(); fig.savefig(f'{OUT}/fig_b.png'); plt.close(fig)

# ---------- 그림 4 : 질량 - 주기 ----------
ms=[59.235,164.955,188.120]; Tc=[1.3900,1.3920,1.3960]
sdc=[0.0000,0.0045,0.0055]
fig,ax=plt.subplots(figsize=(6.6,3.6),dpi=200)
ax.axhspan(1.385,1.405,color='#e8edf2',label='스마트게이트 분해능 0.01 s 범위')
ax.axhline(1.3927,color=GREY,lw=1.3,ls='-',label='세 추의 평균 1.3927 s')
ax.errorbar(ms,Tc,yerr=sdc,fmt='o',ms=7,color=BLUE,capsize=4,lw=1.2,label='측정 평균 (5회)')
for m,t,nm in zip(ms,Tc,['추 1','추 2','추 3']):
    ax.annotate(f'{nm}  {t:.3f} s',xy=(m,t),xytext=(11,0),textcoords='offset points',
                ha='left',va='center',fontsize=8,color=BLUE)
ax.set_xlabel('추의 질량 m (g)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(30,245); ax.set_ylim(1.37,1.42)
ax.grid(alpha=0.3,ls=':'); ax.legend(fontsize=8.3,loc='lower right')
fig.tight_layout(); fig.savefig(f'{OUT}/fig_c.png'); plt.close(fig)

# ---------- 그림 5 : 조건별 측정 g ----------
labels=['10°','20°','30°','40°','50°','0.300 m','0.700 m','추 1','추 2']
gv=[10.1288,10.0710,9.8726,9.6529,9.4144,9.9685,9.9327,10.2165,10.1871]
cols=[BLUE]*5+['#2f7d32']*2+['#8a6d3b']*2
fig,ax=plt.subplots(figsize=(6.6,3.6),dpi=200)
ax.bar(range(len(gv)),gv,width=0.62,color=cols,edgecolor='#333333',lw=0.5)
ax.axhline(g0,color=RED,lw=1.5,ls='--',label='기준값 9.80 m/s²')
for i,v in enumerate(gv):
    ax.text(i,v+0.03,f'{v:.2f}',ha='center',fontsize=7.4)
ax.set_xticks(range(len(gv))); ax.set_xticklabels(labels,fontsize=8.5)
ax.set_ylabel('측정한 중력가속도 g (m/s²)'); ax.set_ylim(9.0,10.5)
ax.set_xlabel('A. 진폭 변화                B. 길이 변화        C. 질량 변화',fontsize=9)
ax.grid(axis='y',alpha=0.3,ls=':'); ax.set_axisbelow(True); ax.legend(fontsize=8.5)
fig.tight_layout(); fig.savefig(f'{OUT}/fig_g.png'); plt.close(fig)
print('figures built')
