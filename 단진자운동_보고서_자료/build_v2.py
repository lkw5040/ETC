# -*- coding: utf-8 -*-
"""단진자 운동 실험 결과보고서 (HWPX) — 원시 데이터 기반."""
import warnings, os, math, json, statistics as st
warnings.filterwarnings("ignore", category=DeprecationWarning)
from hwpx import HwpxDocument
from PIL import Image

SCR = "/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad"
OUT = "/home/user/ETC/단진자운동_실험결과보고서.hwpx"
SERIF, SANS = "함초롬바탕", "함초롬돋움"
g0, FP = 9.80, 4*math.pi**2
raw = json.load(open(f"{SCR}/raw.json"))
def Tm(k): return st.mean(raw[k])
def Tth(l): return 2*math.pi*math.sqrt(l/g0)
def gm(l, T): return FP*l/T**2

doc = HwpxDocument.new()
doc.page.setup(paper_size="A4", orientation="portrait",
               margins_mm={"left": 30, "right": 30, "top": 25,
                           "bottom": 20, "header": 15, "footer": 15})

def make_parapr(**fmt):
    p = doc.add_paragraph("")
    doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs)-1, **fmt)
    pid = p.para_pr_id_ref; p.remove(); return pid

PP = {
    "cover":  make_parapr(alignment="CENTER", line_spacing_percent=150),
    "title":  make_parapr(alignment="CENTER", line_spacing_percent=150,
                          spacing_before_pt=18, spacing_after_pt=12),
    "h1":     make_parapr(alignment="LEFT", line_spacing_percent=150,
                          spacing_before_pt=14, spacing_after_pt=4),
    "h2":     make_parapr(alignment="LEFT", line_spacing_percent=150,
                          spacing_before_pt=9, spacing_after_pt=3),
    "body":   make_parapr(alignment="JUSTIFY", line_spacing_percent=165,
                          first_line_indent_mm=3, spacing_after_pt=3),
    "plain":  make_parapr(alignment="JUSTIFY", line_spacing_percent=165,
                          spacing_after_pt=3),
    "bullet": make_parapr(alignment="JUSTIFY", line_spacing_percent=160,
                          indent_left_mm=5, first_line_indent_mm=-5, spacing_after_pt=2),
    "eq":     make_parapr(alignment="CENTER", line_spacing_percent=150,
                          spacing_before_pt=4, spacing_after_pt=4),
    "cap":    make_parapr(alignment="CENTER", line_spacing_percent=135,
                          spacing_before_pt=3, spacing_after_pt=8),
    "capTop": make_parapr(alignment="CENTER", line_spacing_percent=135,
                          spacing_before_pt=8, spacing_after_pt=3),
    "fig":    make_parapr(alignment="CENTER", line_spacing_percent=110,
                          spacing_before_pt=6),
    "cell":   make_parapr(alignment="CENTER", line_spacing_percent=130),
    "cellL":  make_parapr(alignment="LEFT", line_spacing_percent=130),
    "ref":    make_parapr(alignment="JUSTIFY", line_spacing_percent=160,
                          indent_left_mm=7, first_line_indent_mm=-7, spacing_after_pt=2),
}
def para(text="", pp="body", size=10.5, font=SERIF, bold=False):
    p = doc.add_paragraph("", para_pr_id_ref=PP[pp])
    if text: p.add_run(text, size=size, font=font, bold=bold)
    return p
def h1(t): para(t, "h1", size=13, font=SANS, bold=True)
def h2(t): para(t, "h2", size=11, font=SANS, bold=True)
def body(t): para(t, "body", size=10.5)
def eq(t): para(t, "eq", size=10.5)
def cap(t, top=False): para(t, "capTop" if top else "cap", size=9.5, font=SANS)
def picture(path, width_mm):
    with open(path, "rb") as fh: data = fh.read()
    with Image.open(path) as im: w, h = im.size
    doc.add_picture(data, "png" if path.endswith(".png") else "jpg",
                    width_mm=width_mm, height_mm=round(width_mm*h/w, 1),
                    align="CENTER", para_pr_id_ref=PP["fig"])
def table(rows, cols, widths=None, merges=()):
    t = doc.add_table(rows, cols, para_pr_id_ref=PP["plain"])
    if widths: t.set_column_widths(widths)
    for m in merges: t.merge_cells(*m)
    return t
def cell(t, r, c, text, bold=False, size=9, shade=None, align="cell", font=SANS):
    tc = t.cell(r, c); p = tc.paragraphs[0]
    p.para_pr_id_ref = PP[align]; p.clear_text()
    if text: p.add_run(text, size=size, font=font, bold=bold,
                       expand_special_characters=True)
    if shade:
        a = tc.address; t.set_cell_shading(a[0], a[1], shade)
HDR, SUB = "#E8EDF2", "#F4F6F8"

# ===================== 표지 =====================
para("2026년 2학기 물리학 및 실험1", "cover", size=11, font=SANS)
para("과목코드: APHY1002-00  00분반", "cover", size=11, font=SANS)
para("담당교수: 박창수", "cover", size=11, font=SANS)
para("담당조교: 유승아", "cover", size=11, font=SANS)
para("", "cover")
para("단진자 운동 실험 결과보고서", "title", size=19, font=SANS, bold=True)
para("", "cover")
para("1조 (김성윤 2020104170,", "cover", size=11)
para("이기원 2021105717,", "cover", size=11)
para("이연희 2021103943,", "cover", size=11)
para("정원일 2021103954)", "cover", size=11)
para("", "cover")
para("실험일 : 2026년 11월 4일", "cover", size=11)
para("제출일 : 2026년 11월 9일", "cover", size=11)

# ===================== Ⅰ. 목적 =====================
h1("Ⅰ. 실험 목적")
body("단진자의 주기가 진폭, 진자의 길이, 추의 질량에 따라 각각 달라지는지 확인하고, 달라진다면 "
     "어떤 모양으로 변하는지 알아보았다. 또 측정한 주기로부터 중력가속도를 구해 보았다.")

# ===================== Ⅱ. 이론 =====================
h1("Ⅱ. 배경 및 이론")
body("길이 l 인 실에 질량 m 인 추를 매달아 중력에 의해 진동하게 만든 계를 단진자라고 한다. "
     "실이 연직축과 θ 의 각을 이룰 때 추에는 평형점으로 되돌아가려는 복원력이 작용한다 [1].")
eq("F = − m g sin θ          (1)")
body("진폭이 충분히 작아 θ 가 작으면 sin θ ≈ θ 로 어림할 수 있고, 호의 길이가 x = l θ 이므로 "
     "식 (1)은 단순조화운동의 식이 된다.")
eq("m d²x/dt² = − (m g / l) x          (2)")
body("이 식의 해는 x = x_max cos(ω t + φ) 꼴이고 각진동수는 ω = √(g/l) 이다. 주기는 "
     "T = 2π/ω 이므로 단진자의 주기는 다음과 같다.")
eq("T = 2π √(l / g)          (3)")
body("식 (3)을 중력가속도에 대해 풀면 진자의 길이와 주기로부터 g 를 구할 수 있다.")
eq("g = 4π² l / T²          (4)")
body("식 (3)에서 이 실험으로 확인할 세 가지가 바로 나온다. 첫째, 우변에 질량 m 이 없으므로 "
     "주기는 추의 질량과 무관해야 한다. 복원력 m g sin θ 와 관성 m 이 함께 질량에 비례해 서로 "
     "상쇄되기 때문이다. 둘째, 우변에 진폭도 없으므로 주기는 진폭과도 무관해야 한다. 셋째, "
     "주기는 길이에 정비례하는 것이 아니라 길이의 제곱근에 비례한다. 양변을 제곱하면")
eq("T² = (4π² / g) l          (5)")
body("이 되므로, T² 을 l 에 대해 그리면 원점을 지나는 직선이 되어야 한다.")
body("다만 둘째 예측은 sin θ ≈ θ 라는 어림이 성립하는 작은 진폭에서만 맞는 이야기이다. 진폭이 "
     "커지면 이 어림이 점점 어긋나므로 실제 주기는 식 (3)의 값보다 조금씩 길어진다. 진폭을 "
     "어디까지 키워도 '진폭과 무관하다'고 볼 수 있는지를 확인하는 것이 A 실험의 목적이다.")

# ===================== Ⅲ. 실험 방법 =====================
h1("Ⅲ. 실험 방법")
h2("1. 실험 장치")
body("스탠드와 클램프에 실을 묶어 추를 매달아 단진자를 만들고, 진자의 연직축 바로 아래에 "
     "스마트게이트를 설치하여 추가 게이트 사이를 지나가도록 하였다(그림 1, 그림 2). "
     "스마트게이트는 블루투스로 연결한 SPARKvue 앱과 연동하여 주기(Period)를 기록하였고, "
     "진자의 길이는 미터자로 맞추었다.")
picture(f"{SCR}/p_setup.jpg", 118)
cap("그림 1. 실험 장치. 스탠드에 매단 단진자와 그 아래의 스마트게이트, 길이를 맞추는 데 사용한 "
    "미터자가 보인다. 왼쪽 아래에 번갈아 사용한 다른 두 추가 놓여 있다.")
picture(f"{SCR}/p_gate.jpg", 118)
cap("그림 2. 추가 스마트게이트를 지나가는 모습. 게이트를 진자의 연직축 바로 아래에 두어 추가 "
    "최하점을 지날 때 신호가 기록되도록 하였다.")
body("실험에 사용한 세 추의 질량은 전자저울(CAS MWP, 최대 300 g, 최소 눈금 0.005 g)로 "
     "측정하였다(그림 3). 추 1은 59.235 g, 추 2는 164.955 g, 추 3은 188.120 g으로 가장 가벼운 "
     "추와 가장 무거운 추의 질량비는 약 3.18배였고, 세 추의 반지름은 모두 1.5 cm로 같았다. "
     "즉 모양과 크기는 같고 질량만 다른 추를 사용하였다.")
picture(f"{SCR}/photo_mass.jpg", 124)
cap("그림 3. 전자저울로 측정한 세 추의 질량과 실 연결용 고리의 질량.")

cap("표 1. 실험 조건", top=True)
cond = [
    ("A. 진폭 변화", "추 3, 길이 0.500 m 고정 / 진폭 10°, 20°, 30°, 40°, 50°"),
    ("B. 길이 변화", "추 3, 진폭 10° 고정 / 길이 0.300 m, 0.500 m, 0.700 m"),
    ("C. 질량 변화", "길이 0.500 m, 진폭 10° 고정 / 추 1, 추 2, 추 3"),
    ("반복", "각 조건에서 5회씩, 총 45회"),
    ("주기 측정", "스마트게이트 + SPARKvue, 기록 단위 0.01 s"),
    ("중력가속도 기준값", "g = 9.80 m/s²"),
]
t = table(len(cond)+1, 2, widths=[1.0, 3.0])
cell(t, 0, 0, "구분", bold=True, shade=HDR, size=9.5)
cell(t, 0, 1, "조건", bold=True, shade=HDR, size=9.5)
for i, (k, v) in enumerate(cond, start=1):
    cell(t, i, 0, k, size=9.5)
    cell(t, i, 1, v, size=9.5, align="cellL")
para("", "plain")

h2("2. 실험 과정")
for s in [
    "(1) 세 추의 질량과 반지름을 측정하였다.",
    "(2) 스탠드에 실을 묶어 추를 매달고, 진자의 연직축 아래에 스마트게이트를 설치한 뒤 "
    "SPARKvue와 연결하였다.",
    "(3) 진자의 길이를 맞추고, 각도계를 보며 초기 각도를 정한 뒤 추를 밀지 않고 가만히 놓아 "
    "진동시켰다.",
    "(4) 표 1의 세 가지 조건(A·B·C)에 맞추어 각 조건에서 5회씩 주기를 측정하였다.",
    "(5) 측정한 주기를 식 (3)의 이론값과 비교하고, 식 (4)로 중력가속도를 계산하였다.",
]:
    para(s, "plain", size=10.5)
body("진자의 길이는 회전축에서 추의 질량중심까지로 정하고, 실 길이에 추의 반지름 1.5 cm를 "
     "더해 맞추었다. 또 추를 놓을 때 옆으로 밀리면 한 평면에서 흔들리지 않아 주기가 달라지므로, "
     "그런 회차는 다시 측정하였다. 길이 0.500 m에 진폭 10°인 조건은 A의 10°, B의 0.500 m, "
     "C의 추 3에 모두 해당하므로 한 번만 측정하여 세 곳에 함께 사용하였다.")

# ===================== Ⅳ. 결과 및 분석 =====================
h1("Ⅳ. 결과 및 분석")
h2("1. 측정 데이터 정리")
body("SPARKvue는 한 번 측정할 때마다 추가 게이트를 지날 때의 주기를 연속으로 기록한다. 이번 "
     "45회 측정에서 기록된 주기는 모두 505개였다. 이 가운데 0.820 s 와 0.850 s 로 기록된 두 "
     "값은 다른 값들의 절반 정도여서 추가 게이트를 완전히 지나지 않았을 때 잘못 기록된 것으로 "
     "보고 제외하였고, 남은 503개를 분석에 사용하였다. 아래의 모든 그래프와 평균값은 5회의 "
     "대표값이 아니라 이 503개의 원시 데이터를 그대로 쓴 것이다.")
cap("표 2. 조건별 측정 결과 (원시 데이터 503개 기준)", top=True)
ROWS = [
    ("A. 진폭", "10°",            "S",    0.500, 1),
    (None,      "20°",            "A20",  0.500, 0),
    (None,      "30°",            "A30",  0.500, 0),
    (None,      "40°",            "A40",  0.500, 0),
    (None,      "50°",            "A50",  0.500, 0),
    ("B. 길이", "0.300 m",        "B300", 0.300, 0),
    (None,      "0.500 m",        "S",    0.500, 1),
    (None,      "0.700 m",        "B700", 0.700, 0),
    ("C. 질량", "추 1 (59.2 g)",  "C1",   0.500, 0),
    (None,      "추 2 (165.0 g)", "C2",   0.500, 0),
    (None,      "추 3 (188.1 g)", "S",    0.500, 1),
]
t = table(len(ROWS)+1, 6, widths=[0.95, 1.3, 0.95, 1.2, 1.15, 1.15],
          merges=[(1,0,5,0), (6,0,8,0), (9,0,11,0)])
for c, nm in enumerate(["구분", "조건", "측정\n주기 수", "평균 주기\nT [s]",
                        "이론 주기\n[s]", "측정 g\n[m/s²]"]):
    cell(t, 0, c, nm, bold=True, shade=HDR, size=9)
for r, (grp, lab, key, l, shared) in enumerate(ROWS, start=1):
    if grp: cell(t, r, 0, grp, bold=True, size=9, shade=SUB)
    T = Tm(key)
    cell(t, r, 1, lab, size=9)
    cell(t, r, 2, str(len(raw[key])), size=9)
    cell(t, r, 3, f"{T:.3f}", bold=True, size=9)
    cell(t, r, 4, f"{Tth(l):.3f}", size=9)
    cell(t, r, 5, f"{gm(l, T):.2f}", size=9)
para("※ 길이 0.500 m · 진폭 10° · 추 3 은 같은 측정을 세 곳에 함께 사용한 조건이다.",
     "plain", size=9.5)

# ---- 2. 진폭 ----
h2("2. 진폭은 주기에 영향을 주는가")
picture(f"{SCR}/g_amp.png", 140)
cap("그림 4. 초기 진폭에 따른 주기. 연한 점은 기록된 주기 하나하나이고 진한 점과 선은 조건별 "
    "평균이다. 점들이 가로줄 모양으로 모이는 것은 주기가 0.01 s 단위로 기록되기 때문이다.")
body("진폭을 10°에서 50°까지 키우는 동안 평균 주기는 1.396 s, 1.400 s, 1.413 s, 1.432 s, "
     "1.450 s로 한 번도 뒤집히지 않고 계속 커졌다. 10°와 50°를 비교하면 약 3.8 % 늘어난 "
     "값이다. 따라서 진폭은 주기에 영향을 준다.")
body("다만 영향의 정도가 진폭에 따라 다르다. 10°와 20° 사이에서는 주기 차이가 0.004 s "
     "(약 0.3 %)에 지나지 않아 사실상 같다고 볼 수 있지만, 40°와 50°로 갈수록 차이가 눈에 "
     "띄게 커진다. 그래프에서도 왼쪽은 거의 평평하다가 오른쪽으로 갈수록 가팔라진다. 즉 "
     "진폭과 주기는 정비례 관계가 아니고, 진폭이 커질수록 주기가 점점 빠르게 길어지는 모양이다.")
body("이것은 식 (3)이 sin θ ≈ θ 라는 어림에서 나온 결과이기 때문이다. 진폭이 작을 때는 어림이 "
     "잘 맞아 주기가 진폭과 무관하지만, 진폭이 커지면 어림이 어긋나면서 실제 주기가 길어진다. "
     "결론적으로 '주기는 진폭과 무관하다'는 성질은 대략 20° 이내의 작은 진폭에서만 쓸 수 "
     "있다고 볼 수 있다.")

# ---- 3. 길이 ----
h2("3. 길이는 주기에 어떻게 영향을 주는가")
picture(f"{SCR}/g_len.png", 140)
cap("그림 5. 진자 길이에 따른 주기. 회색 곡선은 식 (3)으로 그린 이론 곡선이다.")
body("진자의 길이를 0.300 m, 0.500 m, 0.700 m로 바꾸었을 때 평균 주기는 1.091 s, 1.396 s, "
     "1.668 s였다. 길이가 길어지면 주기도 길어지므로 길이는 주기에 분명히 영향을 준다.")
body("다만 정비례는 아니다. 길이가 2.33배로 늘어나는 동안 주기는 1.53배밖에 늘어나지 않았는데, "
     "√2.33 = 1.53 이므로 주기가 길이의 제곱근에 비례한다는 식 (3)과 잘 맞는다. 그림 5에서도 "
     "측정값이 이론 곡선 위에 거의 그대로 놓여, 길이가 길어질수록 주기가 늘어나는 정도가 점점 "
     "완만해지는 모양을 보여 준다.")
picture(f"{SCR}/g_len2.png", 140)
cap("그림 6. 진자 길이와 주기의 제곱. 세 점이 원점을 지나는 직선 위에 거의 그대로 놓인다.")
body("이것을 더 분명히 보기 위해 식 (5)대로 T² 을 l 에 대해 그린 것이 그림 6이다. 세 점이 "
     "원점을 지나는 직선 위에 거의 그대로 놓였고(R² = 0.999), 추세선의 y절편도 −0.014 로 "
     "사실상 0 이다. 즉 주기 자체는 길이에 정비례하지 않지만, 주기의 제곱은 길이에 정비례한다.")
body("추세선의 기울기 3.977 s²/m 는 식 (5)에서 4π²/g 에 해당하므로, 여기서 중력가속도를 구하면 "
     "g = 4π² / 3.977 = 9.93 m/s² 이고 기준값 9.80 m/s² 과의 차이는 약 1.3 % 이다.")

# ---- 4. 질량 ----
h2("4. 추의 질량은 주기에 영향을 주는가")
picture(f"{SCR}/g_mass.png", 140)
cap("그림 7. 추의 질량에 따른 주기. 질량이 3배 넘게 달라져도 주기는 거의 변하지 않는다.")
body("질량이 59.2 g, 165.0 g, 188.1 g으로 3.18배까지 차이 나는 세 추를 같은 길이와 같은 "
     "진폭에서 흔들었을 때 평균 주기는 1.390 s, 1.394 s, 1.396 s였다. 가장 가벼운 추와 가장 "
     "무거운 추의 주기 차이는 0.006 s로 약 0.4 % 에 지나지 않는다.")
body("이 차이는 스마트게이트가 주기를 기록하는 단위인 0.01 s 보다도 작다. 즉 세 값은 측정 "
     "장치가 구별할 수 있는 한계 안에서 사실상 같은 값이며, 질량은 주기에 영향을 주지 않는다고 "
     "볼 수 있다. 식 (3)에 질량이 들어 있지 않은 것과 잘 맞는 결과이다. 세 값이 질량 순서대로 "
     "조금씩 커지기는 했지만 차이가 기록 단위보다 작으므로 경향이라고 말하기는 어렵다.")

# ---- 5. 중력가속도 ----
h2("5. 중력가속도")
body("표 2에서 식 (4)로 구한 중력가속도는 9.39 m/s² 에서 10.21 m/s² 사이에 있었고 평균은 "
     "약 9.93 m/s² 였다. 진폭이 큰 40°와 50° 조건에서 9.62 m/s², 9.39 m/s² 로 작게 나오는데, "
     "이는 2절에서 본 대로 진폭이 커지면 주기가 길어지고 식 (4)에서 g 는 주기의 제곱에 "
     "반비례하기 때문이다. 따라서 중력가속도를 구할 때는 진폭이 작은 조건의 결과를 써야 한다.")
body("가장 믿을 만한 값은 3절에서 길이를 세 가지로 바꾸어 얻은 T²–l 그래프의 기울기로 구한 "
     "9.93 m/s² 이다. 한 조건의 주기 하나만 쓰는 것이 아니라 세 길이의 결과를 함께 쓰기 "
     "때문이다. 기준값 9.80 m/s² 에 대한 차이는 약 1.3 % 로, 학부 실험 수준에서는 충분히 "
     "가까운 값이라고 볼 수 있다.")

# ---- 6. 오차 ----
h2("6. 오차 원인과 개선 방안")
body("세 가지 예측은 모두 측정값에서 확인되었고 중력가속도도 1~3 % 수준에서 맞았다. 다만 "
     "조건별로 구한 g 가 대체로 기준값 9.80 m/s² 보다 조금 크게 나오는 경향이 있었는데, 이는 "
     "측정된 주기가 이론값보다 조금씩 짧았다는 뜻이다. 그 원인으로 생각되는 것들과 개선할 점을 "
     "정리하면 다음과 같다.")
for s in [
    "· 주기가 0.01 s 단위로만 기록되었다. 주기가 약 1.4 s 이므로 한 칸이 0.7 % 에 해당하고, "
    "g 는 주기의 제곱에 반비례하므로 g 에는 그 두 배 정도의 영향을 준다. 이번처럼 기록된 "
    "주기를 모두 평균하면 이 영향을 줄일 수 있다.",
    "· 진자의 길이를 정확히 재기 어려웠다. 식 (4)에서 g 는 길이에 정비례하므로 길이의 오차가 "
    "그대로 g 의 오차가 된다. 회전축이 되는 매듭의 위치와 추의 질량중심을 눈으로 맞추는 데 "
    "한계가 있었으므로, 추의 지름을 캘리퍼스로 재어 반지름을 정확히 더하고 길이를 여러 번 "
    "재어 평균을 쓰면 좋겠다.",
    "· 초기 진폭을 손으로 맞추다 보니 조금씩 차이가 생길 수 있다. 2절에서 본 것처럼 진폭이 "
    "커지면 주기가 길어지므로, g 를 구할 때는 진폭을 10° 이하로 작게 하는 것이 좋다.",
    "· 공기저항 때문에 흔들리는 동안 진폭이 조금씩 줄어든다. 실제로 기록을 보면 한 번의 측정 "
    "안에서도 뒤로 갈수록 주기가 조금씩 짧아졌고, 그 정도는 진폭이 큰 조건에서 더 뚜렷했다. "
    "측정 시간을 너무 길게 잡지 않는 것이 좋다.",
    "· 중력가속도는 한 조건의 주기로 구하기보다, 이번 3절처럼 길이를 여러 개로 바꾸어 T²–l "
    "그래프의 기울기에서 구하는 편이 더 정확하다.",
]:
    para(s, "bullet", size=10.5)

# ===================== Ⅴ. 결론 =====================
h1("Ⅴ. 결론")
body("단진자의 주기를 진폭, 길이, 질량을 각각 바꾸어 가며 측정하고, 기록된 503개의 주기를 "
     "그대로 사용해 경향을 확인하였다.")
body("첫째, 추의 질량은 주기에 영향을 주지 않았다. 질량을 3.18배까지 바꾸어도 주기는 0.4 % "
     "밖에 달라지지 않았고, 이는 주기를 기록한 단위보다도 작은 차이였다.")
body("둘째, 진자의 길이는 주기에 영향을 주지만 정비례하지는 않았다. 길이가 2.33배 늘어날 때 "
     "주기는 1.53배 늘어나 길이의 제곱근에 비례하였고, T² 을 l 에 대해 그리면 원점을 지나는 "
     "직선이 되어(R² = 0.999) 주기의 제곱이 길이에 정비례함을 확인하였다.")
body("셋째, 진폭은 작을 때는 주기에 거의 영향을 주지 않지만 커지면 주기를 길게 만들었다. "
     "10°와 20°의 주기 차이는 0.3 % 에 그친 반면 10°에서 50°까지 키우면 3.8 % 늘어났고, "
     "진폭이 커질수록 변화가 가팔라졌다. 따라서 '주기는 진폭과 무관하다'는 성질은 작은 진폭에서만 "
     "성립한다.")
body("중력가속도는 T²–l 그래프의 기울기로부터 9.93 m/s² 를 얻어 기준값 9.80 m/s² 과 약 1.3 % "
     "차이였다. 조건별로 구한 값이 기준값보다 조금씩 크게 나온 것은 주기의 기록 단위가 0.01 s "
     "였던 점과 진자의 길이를 정확히 재기 어려웠던 점이 함께 작용한 것으로 생각된다. 다음 "
     "실험에서는 추의 지름을 캘리퍼스로 재어 길이를 더 정확히 맞추고, 진폭을 10° 이하로 작게 "
     "하면 기준값에 더 가까운 값을 얻을 수 있을 것이다.")

# ===================== Ⅵ. 참고문헌 =====================
h1("Ⅵ. 참고문헌")
for r in [
    "[1] 임헌화 외 10명, 일반물리학 실험, 개정 2판 5쇄, 2단원 역학, 단진자 운동, 2003년 출판.",
    "[2] D. Halliday, R. Resnick, J. Walker, 일반물리학(Fundamentals of Physics), 10판, "
    "15장 진동 - 단진자, 범한서적.",
    "[3] R. A. Serway, J. W. Jewett, 대학물리학(Physics for Scientists and Engineers), "
    "15장 단순조화운동 - 단진자, 북스힐.",
    "[4] PASCO scientific, Wireless Smart Gate Instruction Manual, PASCO scientific.",
    "[5] PASCO scientific, SPARKvue User's Guide, PASCO scientific.",
]:
    para(r, "ref", size=10)

if doc.paragraphs and not doc.paragraphs[0].text.strip():
    doc.paragraphs[0].remove()
print("validate:", doc.validate().issues)
doc.save_to_path(OUT)
print("saved:", OUT, os.path.getsize(OUT), "bytes")
