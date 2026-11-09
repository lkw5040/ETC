import csv, math, statistics as st, json
path="/root/.claude/uploads/75bb76ef-4ca8-544c-9ba0-f132e07a100b/035bce6e-ExportedData.csv"
rows=list(csv.reader(open(path,encoding='utf-8-sig')))
runs=[]
for r in range(45):
    b=r*4; per=[]
    for row in rows[1:]:
        if len(row)>b+2 and row[b+2].strip(): per.append(float(row[b+2]))
    med=st.median(per)
    runs.append([v for v in per if abs(v-med)<=0.05])        # 이상치 제거

COND=[("C1",0,5),("C2",5,10),("S",10,15),("A20",15,20),("A30",20,25),
      ("A40",25,30),("A50",30,35),("B700",35,40),("B300",40,45)]
raw={k:[v for r in runs[a:b] for v in r] for k,a,b in COND}

g0=9.80; FP=4*math.pi**2
def Tth(l): return 2*math.pi*math.sqrt(l/g0)
def gm(l,T): return FP*l/T**2

print(f"{'조건':<22}{'n':>5}{'평균T':>9}{'표준편차':>9}{'최소':>7}{'최대':>7}")
def line(name,key):
    d=raw[key]
    print(f"{name:<22}{len(d):>5}{st.mean(d):>9.4f}{st.pstdev(d):>9.4f}{min(d):>7.2f}{max(d):>7.2f}")
    return st.mean(d)

print("\n--- A. 진폭 (l=0.500 m, 추3) ---")
A={}
A[10]=line("10°","S"); A[20]=line("20°","A20"); A[30]=line("30°","A30")
A[40]=line("40°","A40"); A[50]=line("50°","A50")
print(f"  10°->50° 주기 증가 {(A[50]/A[10]-1)*100:.1f} %")

print("\n--- B. 길이 (10°, 추3) ---")
B={}
B[0.300]=line("0.300 m","B300"); B[0.500]=line("0.500 m","S"); B[0.700]=line("0.700 m","B700")
print(f"  길이 {0.700/0.300:.2f}배 -> 주기 {B[0.700]/B[0.300]:.2f}배 (√2.33 = {math.sqrt(0.7/0.3):.2f})")
print(f"  {'l':>7}{'T':>9}{'T²':>9}{'T²/l':>9}{'T_th':>9}{'측정g':>9}")
for l in (0.300,0.500,0.700):
    T=B[l]; print(f"  {l:>7.3f}{T:>9.4f}{T*T:>9.4f}{T*T/l:>9.4f}{Tth(l):>9.4f}{gm(l,T):>9.4f}")
ls=[0.300,0.500,0.700]; T2=[B[l]**2 for l in ls]
n=3; sx=sum(ls); sy=sum(T2); sxx=sum(x*x for x in ls); sxy=sum(x*y for x,y in zip(ls,T2))
slope=(n*sxy-sx*sy)/(n*sxx-sx*sx); icpt=(sy-slope*sx)/n
print(f"  추세선  T² = {slope:.3f} l {icpt:+.4f}   ->  g = 4π²/기울기 = {FP/slope:.3f} m/s²")

print("\n--- C. 질량 (l=0.500 m, 10°) ---")
C={}
C[59.235]=line("추1  59.235 g","C1"); C[164.955]=line("추2 164.955 g","C2")
C[188.120]=line("추3 188.120 g","S")
v=list(C.values())
print(f"  질량 {188.120/59.235:.2f}배 -> 주기 차 {(max(v)-min(v))*1000:.0f} ms ({(max(v)/min(v)-1)*100:.2f} %)")

print("\n--- 중력가속도 ---")
allg=[gm(0.500,A[a]) for a in A]+[gm(l,B[l]) for l in (0.300,0.700)]+[gm(0.500,C[m]) for m in (59.235,164.955)]
print(f"  9개 조건 {min(allg):.2f} ~ {max(allg):.2f}, 평균 {st.mean(allg):.2f}")
small=[gm(0.300,B[0.300]),gm(0.700,B[0.700])]+[gm(0.500,C[m]) for m in C]
print(f"  진폭 10° 조건 5개 평균 g = {st.mean(small):.3f} (오차 {abs(st.mean(small)-g0)/g0*100:.1f} %)")
print(f"  B 추세선 g = {FP/slope:.3f} (오차 {abs(FP/slope-g0)/g0*100:.1f} %)")

json.dump({k:v for k,v in raw.items()}, open("/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad/raw.json","w"))
print("\nraw.json 저장")
