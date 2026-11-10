import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import json, math, random, statistics as st
fp='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=10
O='/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad'
raw=json.load(open(f'{O}/raw.json')); runs=json.load(open(f'{O}/runs.json'))
random.seed(7)
g0=9.80; FP=4*math.pi**2
BLUE='#1f4e79'; LIGHT='#9dc3e6'; RED='#c0504d'; GREY='#808080'; GREEN='#2f7d32'; GOLD='#b8860b'
T=lambda k: st.mean(raw[k])

def style(ax):
    ax.grid(alpha=.35, ls='-', lw=.6, color='#d9d9d9'); ax.set_axisbelow(True)
    for s in ('top','right'): ax.spines[s].set_visible(False)
def sc(ax,x,v,w,lab=None):
    ax.plot([x+random.uniform(-w,w) for _ in v], v,'o',ms=3.2,color=LIGHT,
            alpha=.55,mec='none',label=lab,zorder=2)
def save(fig,name):
    fig.tight_layout(); fig.savefig(f'{O}/{name}.png'); plt.close(fig)

ANG=[10,20,30,40,50]; AK=['S','A20','A30','A40','A50']
LS=[0.300,0.500,0.700]; LK=['B300','S','B700']
MS=[59.235,164.955,188.120]; MK=['C1','C2','S']

# 1 ── 진폭 - 주기
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
for i,(a,k) in enumerate(zip(ANG,AK)): sc(ax,a,raw[k],1.6,'측정된 주기 (원시 데이터)' if i==0 else None)
m=[T(k) for k in AK]
ax.plot(ANG,m,'-o',color=BLUE,ms=7,lw=1.8,label='조건별 평균',zorder=4)
for a,v in zip(ANG,m): ax.annotate(f'{v:.3f}',(a,v),xytext=(0,11),textcoords='offset points',
                                   ha='center',fontsize=8,color=BLUE,fontweight='bold')
ax.axhline(m[0],color=GREY,ls=':',lw=1.2,label='10° 의 주기 (기준선)')
ax.set_xlabel('초기 진폭 θ (°)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(2,58); ax.set_ylim(1.378,1.478); ax.set_xticks(ANG)
style(ax); ax.legend(fontsize=8.5,loc='upper left'); save(fig,'g_amp')

# 2 ── 진폭 - 주기 변화율
fig,ax=plt.subplots(figsize=(6.6,3.5),dpi=200)
d=[(v/m[0]-1)*100 for v in m]
bars=ax.bar(ANG,d,width=5.5,color=[LIGHT]*2+[ '#6fa8d4']+[RED]*2,edgecolor=BLUE,lw=.8)
for a,v in zip(ANG,d): ax.text(a,v+.09,f'{v:.2f} %',ha='center',fontsize=8.5,color=BLUE,fontweight='bold')
ax.axhspan(-0.5,0.5,color='#eaf2e8',zorder=0)
ax.text(11,0.62,'차이 0.5 % 이내 — 사실상 같음',fontsize=8.5,color=GREEN)
ax.set_xlabel('초기 진폭 θ (°)'); ax.set_ylabel('10° 대비 주기 증가율 (%)')
ax.set_xlim(4,56); ax.set_ylim(-0.5,4.6); ax.set_xticks(ANG)
style(ax); save(fig,'g_amp2')

# 3 ── 길이 - 주기
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xs=[.05+.005*i for i in range(151)]
ax.plot(xs,[2*math.pi*math.sqrt(x/g0) for x in xs],'-',color=GREY,lw=1.5,
        label=r'이론 곡선  $T = 2\pi\sqrt{l/g}$')
for i,(l,k) in enumerate(zip(LS,LK)): sc(ax,l,raw[k],.016,'측정된 주기 (원시 데이터)' if i==0 else None)
lm=[T(k) for k in LK]
ax.plot(LS,lm,'o',color=BLUE,ms=8,label='조건별 평균',zorder=4)
for l,v in zip(LS,lm): ax.annotate(f'{v:.3f} s',(l,v),xytext=(10,-4),textcoords='offset points',
                                   fontsize=8.5,color=BLUE,fontweight='bold')
ax.set_xlabel('진자 길이 $l$ (m)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(.15,.85); ax.set_ylim(.8,1.9)
style(ax); ax.legend(fontsize=8.5,loc='upper left'); save(fig,'g_len')

# 4 ── T^2 - l
T2=[v*v for v in lm]
n=3; sx=sum(LS); sy=sum(T2); sxx=sum(x*x for x in LS); sxy=sum(x*y for x,y in zip(LS,T2))
sl=(n*sxy-sx*sy)/(n*sxx-sx*sx); ic=(sy-sl*sx)/n
r2=1-sum((y-(sl*x+ic))**2 for x,y in zip(LS,T2))/sum((y-sy/n)**2 for y in T2)
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xx=[0,.85]
ax.plot(xx,[sl*x+ic for x in xx],'--',color=RED,lw=1.5,label=f'추세선  $T^2$ = {sl:.3f} $l$ - {abs(ic):.3f}')
ax.plot(xx,[FP/g0*x for x in xx],'-',color=GREY,lw=1.4,label=r'이론 직선  $T^2=(4\pi^2/g)\,l$ ,  $g$=9.80')
ax.plot(LS,T2,'o',color=BLUE,ms=9,zorder=4,label='측정 평균으로 계산한 $T^2$')
for l,v in zip(LS,T2): ax.annotate(f'{v:.3f}',(l,v),xytext=(9,-11),textcoords='offset points',
                                   fontsize=8.5,color=BLUE,fontweight='bold')
ax.text(.055,2.72,f'$R^2$ = {r2:.4f}\n기울기에서  $g$ = 4$\\pi^2$ / {sl:.3f} = {FP/sl:.2f} m/s$^2$',
        fontsize=9,va='top',bbox=dict(boxstyle='round,pad=.45',fc='#f7f7f7',ec='#bfbfbf',lw=.8))
ax.set_xlabel('진자 길이 $l$ (m)'); ax.set_ylabel('주기의 제곱 $T^2$ (s$^2$)')
ax.set_xlim(0,.85); ax.set_ylim(0,3.1)
style(ax); ax.legend(fontsize=8.5,loc='lower right'); save(fig,'g_len2')

# 5 ── log-log
X=[math.log10(l) for l in LS]; Y=[math.log10(v) for v in lm]
sx=sum(X); sy=sum(Y); sxx=sum(x*x for x in X); sxy=sum(x*y for x,y in zip(X,Y))
ne=(n*sxy-sx*sy)/(n*sxx-sx*sx); ic2=(sy-ne*sx)/n
r2b=1-sum((y-(ne*x+ic2))**2 for x,y in zip(X,Y))/sum((y-sy/n)**2 for y in Y)
fig,ax=plt.subplots(figsize=(6.6,3.9),dpi=200)
xx=[-.60,-.08]
ax.plot(xx,[ne*x+ic2 for x in xx],'--',color=RED,lw=1.5,label=f'추세선 기울기 = {ne:.4f}')
ax.plot(xx,[0.5*x+ic2 for x in xx],'-',color=GREY,lw=1.4,label='이론 기울기 = 0.5 (제곱근 비례)')
ax.plot(X,Y,'o',color=BLUE,ms=9,zorder=4,label='측정값')
for l,x,y in zip(LS,X,Y): ax.annotate(f'{l:.3f} m',(x,y),xytext=(9,-11),textcoords='offset points',
                                      fontsize=8.5,color=BLUE,fontweight='bold')
ax.text(-.585,.205,f'$T \\propto l^{{\\,{ne:.3f}}}$   ( 이론 : $l^{{\\,0.5}}$ )\n$R^2$ = {r2b:.4f}',
        fontsize=9.5,va='top',bbox=dict(boxstyle='round,pad=.45',fc='#f7f7f7',ec='#bfbfbf',lw=.8))
ax.set_xlabel('log $l$'); ax.set_ylabel('log $T$')
ax.set_xlim(-.60,-.08); ax.set_ylim(.0,.26)
style(ax); ax.legend(fontsize=8.5,loc='lower right'); save(fig,'g_loglog')

# 6 ── 질량 - 주기
fig,ax=plt.subplots(figsize=(6.6,3.6),dpi=200)
for i,(mm_,k) in enumerate(zip(MS,MK)): sc(ax,mm_,raw[k],3.0,'측정된 주기 (원시 데이터)' if i==0 else None)
cm=[T(k) for k in MK]
ax.plot(MS,cm,'-o',color=BLUE,ms=8,lw=1.8,label='조건별 평균',zorder=4)
for mm_,v in zip(MS,cm): ax.annotate(f'{v:.3f} s',(mm_,v),xytext=(0,14),textcoords='offset points',
                                     ha='center',fontsize=8.5,color=BLUE,fontweight='bold')
ax.axhline(st.mean(cm),color=RED,ls='--',lw=1.3,label=f'세 추의 평균 {st.mean(cm):.3f} s')
ax.text(124,1.357,'질량 3.18배 차이 → 주기 차이 0.006 s (약 0.4 %)\n세 추의 주기가 사실상 같다',
        fontsize=9,color=RED,ha='center')
ax.set_xlabel('추의 질량 m (g)'); ax.set_ylabel('주기 T (s)')
ax.set_xlim(30,215); ax.set_ylim(1.34,1.45)
style(ax); ax.legend(fontsize=8.5,loc='upper left'); save(fig,'g_mass')

# 7 ── 세 요인 비교
fig,ax=plt.subplots(figsize=(6.6,4.0),dpi=200)
ax.plot([l/LS[0] for l in LS],[(v/lm[0]-1)*100 for v in lm],'-o',color=BLUE,ms=8,lw=2,
        label='진자의 길이 (0.300 m 기준)')
ax.plot([a/ANG[0] for a in ANG],[(v/m[0]-1)*100 for v in m],'-s',color=GOLD,ms=7,lw=2,
        label='초기 진폭 (10° 기준)')
ax.plot([x/MS[0] for x in MS],[(v/cm[0]-1)*100 for v in cm],'-^',color=GREEN,ms=7,lw=2,
        label='추의 질량 (59.2 g 기준)')
ax.annotate('길이 2.33배 → 주기 +52.8 %',(LS[2]/LS[0],52.82),xytext=(12,-2),
            textcoords='offset points',ha='left',fontsize=8.8,color=BLUE,fontweight='bold')
ax.annotate('진폭 5배 → +3.8 %',(5,3.82),xytext=(8,6),textcoords='offset points',
            fontsize=8.8,color=GOLD,fontweight='bold')
ax.annotate('질량 3.18배 → +0.4 %',(MS[2]/MS[0],0.42),xytext=(8,-14),textcoords='offset points',
            fontsize=8.8,color=GREEN,fontweight='bold')
ax.axhline(0,color='#333333',lw=.8)
ax.set_xlabel('조건을 몇 배로 바꾸었는가 (가장 작은 조건 = 1)')
ax.set_ylabel('주기 변화율 (%)')
ax.set_xlim(.8,5.6); ax.set_ylim(-4,62)
style(ax); ax.legend(fontsize=9,loc='center right',framealpha=.95); save(fig,'g_summary')

# 8 ── 조건별 g
labs=['10°','20°','30°','40°','50°','0.300 m','0.700 m','추 1','추 2']
keys=['S','A20','A30','A40','A50','B300','B700','C1','C2']
lens=[.5,.5,.5,.5,.5,.3,.7,.5,.5]
gv=[FP*l/T(k)**2 for k,l in zip(keys,lens)]
cols=[BLUE]*5+[GREEN]*2+[GOLD]*2
fig,ax=plt.subplots(figsize=(6.8,3.7),dpi=200)
ax.bar(range(9),gv,width=.62,color=cols,edgecolor='#333333',lw=.5)
ax.axhline(g0,color=RED,lw=1.6,ls='--',label='기준값 9.80 m/s²')
ax.axhline(FP/sl,color='#444444',lw=1.4,ls=':',label=f'$T^2$-$l$ 추세선에서 구한 값 {FP/sl:.2f} m/s²')
for i,v in enumerate(gv): ax.text(i,v+.03,f'{v:.2f}',ha='center',fontsize=7.6)
ax.set_xticks(range(9)); ax.set_xticklabels(labs,fontsize=8.5)
ax.set_ylabel('측정한 중력가속도 g (m/s²)'); ax.set_ylim(9.0,10.5)
ax.set_xlabel('A. 진폭 변화                    B. 길이         C. 질량',fontsize=9)
style(ax); ax.legend(fontsize=8.3,loc='lower left'); save(fig,'g_gvals')

# 9 ── 측정 중 주기 감쇠
fig,ax=plt.subplots(figsize=(6.6,3.8),dpi=200)
cmap=['#9dc3e6','#6fa8d4','#3d7eb8','#c0504d','#8f2d2a']
for (nm,k),c in zip([('10°','S'),('20°','A20'),('30°','A30'),('40°','A40'),('50°','A50')],cmap):
    rs=runs[k]; L=min(len(r) for r in rs)
    seq=[st.mean(r[i] for r in rs) for i in range(L)]
    ax.plot(range(1,L+1),[(v-seq[0])*1000 for v in seq],'-o',ms=4,lw=1.6,color=c,label=f'진폭 {nm}')
ax.axhline(0,color='#333333',lw=.8)
ax.set_xlabel('한 번의 측정 안에서 몇 번째 주기인가')
ax.set_ylabel('첫 주기 대비 변화 (ms)')
ax.set_xlim(.5,10.5); ax.set_ylim(-24,6); ax.set_xticks(range(1,11))
ax.text(5.5,-21.5,'진폭 10° 는 거의 일정하지만, 진폭 50° 는 10주기 만에 20 ms 짧아진다',
        fontsize=9,color=RED,ha='center')
style(ax); ax.legend(fontsize=8.5,loc='lower left',ncol=5,columnspacing=.8,handletextpad=.4)
save(fig,'g_decay')

# 10 ── 조건별 분포 (각 조건 평균 기준 편차)
fig,ax=plt.subplots(figsize=(6.8,3.7),dpi=200)
data=[[(v-T(k))*1000 for v in raw[k]] for k in keys]
ax.axhspan(-5,5,color='#eaf2e8',zorder=0)
ax.text(0.62,5.6,'기록 단위 0.01 s 의 절반 (±5 ms)',fontsize=8.3,color=GREEN)
bp=ax.boxplot(data,patch_artist=True,widths=.55,
              medianprops=dict(color=RED,lw=1.6),
              flierprops=dict(marker='o',ms=3,mfc='#bbbbbb',mec='none'))
for p_,c in zip(bp['boxes'],cols): p_.set_facecolor(c); p_.set_alpha(.45); p_.set_edgecolor(c)
for i,k in enumerate(keys,1):
    ax.text(i,-13.4,f'n={len(raw[k])}',ha='center',fontsize=7.2,color='#555555')
ax.axhline(0,color='#333333',lw=.8)
ax.set_xticklabels(labs,fontsize=8.5)
ax.set_ylabel('조건별 평균에서 벗어난 정도 (ms)')
ax.set_xlabel('A. 진폭 변화                    B. 길이         C. 질량',fontsize=9)
ax.set_ylim(-14.5,14.5)
style(ax); save(fig,'g_box')
print(f'10 charts built.  slope={sl:.4f} R2={r2:.5f} g={FP/sl:.3f} | logslope={ne:.4f} R2={r2b:.5f}')
