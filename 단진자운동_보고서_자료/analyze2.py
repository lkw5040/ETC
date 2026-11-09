import math, statistics as st
g0 = 9.80
FP = 4*math.pi**2

def Tth(l): return 2*math.pi*math.sqrt(l/g0)
def gmeas(l,T): return FP*l/T**2

def row(label, l, Ts):
    Tm = st.mean(Ts); tt = Tth(l); gm = gmeas(l,Tm)
    return dict(label=label, l=l, Ts=Ts, Tm=Tm, sd=st.stdev(Ts), tth=tt,
                eT=abs(Tm-tt)/tt*100, gm=gm, eg=abs(gm-g0)/g0*100)

A = [row(f"{a}°", 0.500, Ts) for a,Ts in [
    (10,[1.39,1.39,1.40,1.40,1.40]), (20,[1.40]*5),
    (30,[1.41,1.41,1.41,1.42,1.42]), (40,[1.43]*5),
    (50,[1.44,1.45,1.45,1.45,1.45])]]
B = [row(f"{l:.3f} m", l, Ts) for l,Ts in [
    (0.300,[1.09]*5), (0.500,[1.39,1.39,1.40,1.40,1.40]),
    (0.700,[1.66,1.67,1.67,1.67,1.67])]]
C = [row(n, 0.500, Ts) for n,Ts in [
    ("추1 (59.23 g)",[1.39]*5), ("추2 (164.95 g)",[1.39,1.40,1.39,1.39,1.39]),
    ("추3 (188.12 g)",[1.39,1.39,1.40,1.40,1.40])]]

for name,grp in [("A. 진폭",A),("B. 길이",B),("C. 질량",C)]:
    print(f"\n=== {name} ===")
    print(f"{'조건':>15} {'평균T':>7} {'sd':>7} {'T_th':>7} {'T오차%':>7} {'측정g':>8} {'g오차%':>7}")
    for r in grp:
        print(f"{r['label']:>15} {r['Tm']:7.4f} {r['sd']:7.4f} {r['tth']:7.4f} "
              f"{r['eT']:7.2f} {r['gm']:8.4f} {r['eg']:7.2f}")

# --- A: 큰 진폭 보정 (타원적분 급수 2차까지) ---
print("\n--- A: 유한 진폭 보정 이론값 ---")
T0 = Tth(0.500)
for a,r in zip([10,20,30,40,50],A):
    s = math.sin(math.radians(a)/2)
    k = 1 + s**2/4 + 9*s**4/64
    print(f"  {a}°: T_exact={T0*k:.4f}  (T0 대비 +{(k-1)*100:.2f}%)  측정={r['Tm']:.4f}")
print(f"  측정 증가율 10°→50° : {(A[4]['Tm']/A[0]['Tm']-1)*100:.2f} %")
s10=math.sin(math.radians(10)/2); s50=math.sin(math.radians(50)/2)
k10=1+s10**2/4+9*s10**4/64; k50=1+s50**2/4+9*s50**4/64
print(f"  이론 증가율 10°→50° : {(k50/k10-1)*100:.2f} %")

# --- B: T^2 vs l 직선 ---
print("\n--- B: T² 과 l 의 관계 ---")
ls=[r['l'] for r in B]; T2=[r['Tm']**2 for r in B]
for l,t2 in zip(ls,T2): print(f"  l={l:.3f}  T²={t2:.4f}  T²/l={t2/l:.4f}")
n=len(ls); sx=sum(ls); sy=sum(T2); sxx=sum(x*x for x in ls); sxy=sum(x*y for x,y in zip(ls,T2))
slope=(n*sxy-sx*sy)/(n*sxx-sx*sx); icpt=(sy-slope*sx)/n
print(f"  최소제곱 직선: T² = {slope:.4f} l + ({icpt:+.5f})")
print(f"  기울기로 구한 g = 4π²/기울기 = {FP/slope:.4f} m/s²  (오차율 {abs(FP/slope-g0)/g0*100:.2f} %)")

# --- C: 질량 ---
print("\n--- C: 질량과 주기 ---")
ms=[59.23,164.95,188.12]
for m,r in zip(ms,C): print(f"  m={m:7.2f} g  평균T={r['Tm']:.4f} s")
print(f"  질량 비 = {max(ms)/min(ms):.2f} 배, 주기 차 = {(max(r['Tm'] for r in C)-min(r['Tm'] for r in C))*1000:.0f} ms "
      f"({(max(r['Tm'] for r in C)/min(r['Tm'] for r in C)-1)*100:.2f} %)")

# --- 분해능 영향 ---
print("\n--- 측정 분해능의 영향 ---")
T=1.396
print(f"  주기 분해능 0.01 s → T={T} 에서 {0.01/T*100:.2f} %")
print(f"  g ∝ 1/T² 이므로 g 에는 약 {2*0.01/T*100:.2f} % 영향")
print(f"  l=0.500 에서 ±0.01s 범위의 g: {gmeas(0.5,T+0.01):.3f} ~ {gmeas(0.5,T-0.01):.3f}")

print("\n--- 측정 g 전체 ---")
allg=[r['gm'] for r in A+B+C]
print(f"  9개 조건 범위 {min(allg):.4f} ~ {max(allg):.4f}, 평균 {st.mean(allg):.4f}")
small=[B[0],B[2],C[0],C[1],C[2]]
print(f"  10° 조건 5개(길이·질량 변화) 평균 g = {st.mean(r['gm'] for r in small):.4f} "
      f"(오차율 {abs(st.mean(r['gm'] for r in small)-g0)/g0*100:.2f} %)")
