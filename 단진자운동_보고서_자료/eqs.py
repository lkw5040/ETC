import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
O='/tmp/claude-0/-home-user-ETC/75bb76ef-4ca8-544c-9ba0-f132e07a100b/scratchpad/eq'
import os; os.makedirs(O, exist_ok=True)
plt.rcParams['mathtext.fontset']='cm'
FS, DPI = 15, 400
EQS = {
 1: r"F = -\,m g \sin\theta",
 2: r"m a = -\,m g \sin\theta \;\;\Rightarrow\;\; a = -\,g \sin\theta",
 3: r"\frac{d^{2}x}{dt^{2}} = -\,\frac{g}{l}\,x",
 4: r"T = 2\pi\sqrt{\frac{l}{g}}",
 5: r"g = \frac{4\pi^{2} l}{T^{2}}",
 6: r"T^{2} = \frac{4\pi^{2}}{g}\,l",
 7: r"T \approx T_{0}\left(1 + \frac{\theta^{2}}{16}\right)",
}
for n, tex in EQS.items():
    fig = plt.figure(figsize=(0.01,0.01), dpi=DPI)
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${tex}$", fontsize=FS, color='black')
    p = f"{O}/eq{n}.png"
    fig.savefig(p, dpi=DPI, bbox_inches='tight', pad_inches=0.04, transparent=True)
    plt.close(fig)
    from PIL import Image
    im = Image.open(p)
    print(f"eq{n}: {im.size}  ->  {im.width/DPI*25.4:.1f} x {im.height/DPI*25.4:.1f} mm")
