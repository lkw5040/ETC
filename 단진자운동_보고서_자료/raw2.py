import csv, math, json, statistics as st
SCR="/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad"
path="/root/.claude/uploads/75bb76ef-4ca8-544c-9ba0-f132e07a100b/035bce6e-ExportedData.csv"
rows=list(csv.reader(open(path,encoding='utf-8-sig')))
runs=[]
for r in range(45):
    b=r*4; per=[]
    for row in rows[1:]:
        if len(row)>b+2 and row[b+2].strip(): per.append(float(row[b+2]))
    med=st.median(per)
    runs.append([v for v in per if abs(v-med)<=0.05])
COND=[("C1",0,5),("C2",5,10),("S",10,15),("A20",15,20),("A30",20,25),
      ("A40",25,30),("A50",30,35),("B700",35,40),("B300",40,45)]
json.dump({k:runs[a:b] for k,a,b in COND}, open(f"{SCR}/runs.json","w"))

g0=9.80; FP=4*math.pi**2
raw={k:[v for r in runs[a:b] for v in r] for k,a,b in COND}
T=lambda k: st.mean(raw[k])

print("--- log-log : T = C · l^n ---")
ls=[0.300,0.500,0.700]; lk=['B300','S','B700']
X=[math.log10(l) for l in ls]; Y=[math.log10(T(k)) for k in lk]
n=3; sx=sum(X); sy=sum(Y); sxx=sum(x*x for x in X); sxy=sum(x*y for x,y in zip(X,Y))
nexp=(n*sxy-sx*sy)/(n*sxx-sx*sx); ic=(sy-nexp*sx)/n
ybar=sy/n
r2=1-sum((y-(nexp*x+ic))**2 for x,y in zip(X,Y))/sum((y-ybar)**2 for y in Y)
print(f"  지수 n = {nexp:.4f}  (이론 0.5),  R² = {r2:.5f}")
print(f"  C = 10^{ic:.4f} = {10**ic:.4f}   (이론 2π/√g = {2*math.pi/math.sqrt(g0):.4f})")

print("\n--- 세 요인 비교 (가장 작은 조건 대비 주기 변화율) ---")
print("  진폭:", [(a, round((T(k)/T('S')-1)*100,2)) for a,k in
                 zip([10,20,30,40,50],['S','A20','A30','A40','A50'])])
print("  길이:", [(l, round((T(k)/T('B300')-1)*100,2)) for l,k in zip(ls,lk)])
print("  질량:", [(m, round((T(k)/T('C1')-1)*100,2)) for m,k in
                 zip([59.235,164.955,188.120],['C1','C2','S'])])

print("\n--- 측정 중 주기 감쇠 (회차별 i번째 주기 평균) ---")
for name,k in [("10°",'S'),("20°",'A20'),("30°",'A30'),("40°",'A40'),("50°",'A50')]:
    rs=json.load(open(f"{SCR}/runs.json"))[k]
    L=min(len(r) for r in rs)
    seq=[st.mean(r[i] for r in rs) for i in range(L)]
    print(f"  {name:>4}: 1번째 {seq[0]:.4f} -> {L}번째 {seq[-1]:.4f}  (감소 {(seq[0]-seq[-1])*1000:.0f} ms)")

print("\n--- 조건별 분포 ---")
for name,k,l in [("10°",'S',0.5),("20°",'A20',0.5),("30°",'A30',0.5),("40°",'A40',0.5),
                 ("50°",'A50',0.5),("0.300 m",'B300',0.3),("0.700 m",'B700',0.7),
                 ("추1",'C1',0.5),("추2",'C2',0.5)]:
    d=raw[k]
    print(f"  {name:>8}  n={len(d):>3}  평균 {st.mean(d):.4f}  표준편차 {st.pstdev(d):.4f}  "
          f"범위 {min(d):.2f}~{max(d):.2f}  g={FP*l/st.mean(d)**2:.3f}")
