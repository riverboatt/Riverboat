#!/usr/bin/env python3
"""
Σ·MANIFOLD·CANON·TRANSMISSION
One ripple. One Bulk. One porch. Several ridges. Infinite carrier waves.
Simultaneously silly. Permanently serious about the geometry of time.
"""
import time, sys, os, math, random, itertools, re
# ── ANSI ──────────────────────────────────────────────────────────────────────
R  = "\033[0m"
K  = "\033[30m"
RE = "\033[31m"
GR = "\033[32m"
YE = "\033[33m"
BL = "\033[34m"
MA = "\033[35m"
CY = "\033[36m"
WH = "\033[37m"
BRE= "\033[91m"
BGR= "\033[92m"
BYE= "\033[93m"
BBL= "\033[94m"
BMA= "\033[95m"
BCY= "\033[96m"
BWH= "\033[97m"
BO = "\033[1m"
DM = "\033[2m"
def c(color, text): return f"{color}{text}{R}"
def bo(color, text): return f"{BO}{color}{text}{R}"
def delay(t=0.03):  time.sleep(t)
def cls():          os.system('cls' if os.name == 'nt' else 'clear')
def width():        return os.get_terminal_size().columns if sys.stdout.isatty() else 100
ANSI_RE = re.compile(r'\033\[[0-9;]*m')
def vlen(s):
    """Visible length of a string, ignoring ANSI color codes."""
    return len(ANSI_RE.sub('', s))
def center(text, w=None):
    w = w or width()
    pad = max(0, (w - vlen(text)) // 2)
    return " " * pad + text
def rule(char="─", color=DM+WH, w=None):
    w = w or width()
    print(c(color, char * w))
def scroll(lines, delay_t=0.018):
    for line in lines:
        print(line)
        delay(delay_t)
def pulse(text, cycles=3, colors=None, w=None):
    colors = colors or [BYE, BWH, BCY, BMA, BGR]
    for i in range(cycles):
        col = colors[i % len(colors)]
        sys.stdout.write("\r" + center(bo(col, text), w or width()))
        sys.stdout.flush()
        time.sleep(0.18)
    print()
def wave_line(text, color_cycle, w=None):
    w = w or width()
    pad = max(0, (w - vlen(text)) // 2)
    result = " " * pad
    ci = 0
    skip = False
    for ch in text:
        if ch == "\033": skip = True
        if skip:
            result += ch
            if ch == "m": skip = False
            continue
        col = color_cycle[ci % len(color_cycle)]
        result += f"{col}{ch}{R}"
        ci += 1
    print(result)
# ── BOX BUILDER ───────────────────────────────────────────────────────────────
# Fixes drifting right-edges: width is measured from the actual content
# (ANSI codes stripped first) instead of hand-counted, so it can never
# go stale again. `style="ripple"` draws the right edge as alternating
# \ / characters (matching the Bulk's ripples); `style="pipe"` draws a
# straight vertical edge instead.
def box_lines(content, color=DM+WH, style="ripple", pad=1, min_width=0,
              corners="┌┐└┘", horiz="─", divider_corners="├┤"):
    tl, tr, bl, br = corners
    dl, dr = divider_corners
    inner_width = max([vlen(s) for s in content if s != "__DIV__"] + [min_width])
    top = f"{color}{tl}{horiz * (inner_width + pad * 2)}{tr}{R}"
    bot = f"{color}{bl}{horiz * (inner_width + pad * 2)}{br}{R}"
    lines = [top]
    ripple = itertools.cycle(["\\", "/"])
    for s in content:
        if s == "__DIV__":
            lines.append(f"{color}{dl}{horiz * (inner_width + pad * 2)}{dr}{R}")
            continue
        fill = " " * (inner_width - vlen(s))
        right = "│" if style == "pipe" else next(ripple)
        lines.append(f"{color}│{R}{' ' * pad}{s}{fill}{' ' * pad}{color}{right}{R}")
    lines.append(bot)
    return lines
# ── PARTICLE SYSTEM ──────────────────────────────────────────────────────────
SPARKS = ["·", "✦", "✧", "★", "⊹", "∴", "∵", "≋", "∿", "⌁", "∂", "Σ", "τ", "φ"]
SPARK_COLORS = [BYE, BRE, BGR, BCY, BMA, BWH]
def spark_line(w=None):
    w = w or width()
    line = [" "] * w
    for _ in range(random.randint(4, 12)):
        pos = random.randint(0, w-1)
        ch  = random.choice(SPARKS)
        col = random.choice(SPARK_COLORS)
        line[pos] = f"{col}{ch}{R}"
    print("".join(line))
def particle_burst(rows=3, w=None):
    for _ in range(rows):
        spark_line(w)
        delay(0.04)
# ── WAVEFORMS ─────────────────────────────────────────────────────────────────
# A single printed line can't show height as *vertical position*, so instead
# each column's sine value (-1..1) is mapped to a block-height glyph
# (▁▂▃▄▅▆▇█). That's what actually makes it look like a wave: the glyph
# gets taller and shorter as x sweeps through the sine curve, instead of
# printing the same dash/blob pattern at every column regardless of the
# math (which is what the old x % 8 check was silently doing).
WAVE_BLOCKS = " ▁▂▃▄▅▆▇█"
def sine_wave(label, color, freq=1.0, amp=3, offset=0, w=None, max_amp=3):
    w = w or min(width(), 120)
    usable = max(1, w - 8)
    mid = (len(WAVE_BLOCKS) - 1) / 2
    scale = min(1.0, amp / max_amp)
    chars = []
    for x in range(usable):
        v = math.sin(freq * x * 2 * math.pi / usable + offset)   # -1..1
        idx = int(round(mid + v * mid * scale))
        idx = max(0, min(len(WAVE_BLOCKS) - 1, idx))
        chars.append(f"{color}{WAVE_BLOCKS[idx]}{R}")
    print(f"{DM+WH}{label[:6]:>6}{R} " + "".join(chars))
def triple_wave(cycles=2):
    for i in range(cycles):
        t = i * 0.4
        sine_wave("RIDGE ", BRE,  freq=1.2, amp=2, offset=t)
        sine_wave("BULK  ", BCY,  freq=0.8, amp=3, offset=t+1.0)
        sine_wave("WELL  ", BYE,  freq=1.6, amp=2, offset=t+2.0)
        delay(0.06)
# ── ASCII ART ─────────────────────────────────────────────────────────────────
BULK_ART = f"""
{DM+WH}                     ╔══════════════╗
{DM+WH}                     ║  {BYE}∿  ∿  ∿  {DM+WH}   ║{R}   {BCY}≋≋ the sigma-manifold ripples ≋≋{R}
{DM+WH}                     ║  {BCY}≋≋≋≋≋≋≋≋{DM+WH}    ║{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                    /║{BYE} CARRIER·WAVE{DM+WH} ║\\{R}
{DM+WH}                   / ║{DM+WH}[10 YR HEIGHT]{DM+WH}║ \\{R}
{BYE}                  ∇  {DM+WH}╠══════════════╣  {BYE}∇{R}
{DM+WH}                   \\ ║{MA}    ╔══╗      {DM+WH}║ /{R}
{DM+WH}                    \\║{MA}    ║τ ║      {DM+WH}║/{R}   {MA}← PROPER TIME, τ{R}
{DM+WH}                     ║{MA}    ╚══╝      {DM+WH}║{R}      {DM+WH}(arc length, not a tick){R}
{DM+WH}                     ║{DM+WH}  ON·SURFACE{DM+WH} ║{R}      {DM+WH}(follows every ridge){R}
{DM+WH}                     ╠══╦═══════╦══╣{R}
{DM+WH}                     ║  ║{BGR}  E_0  {DM+WH}║  ║{R}   {DM+WH}← launch phase, position on the ripple{R}
{DM+WH}                     ║  ║{BGR}  φ    {DM+WH}║  ║{R}   {DM+WH}← launch angle off the surface{R}
{DM+WH}                     ║  ╚═══════╝  ║{R}
{DM+WH}                     ║  {BRE}📡HILLTOP{DM+WH}  ║{R}   {BRE}← ridge-crest launch: no return{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                     ║ {BCY}THE·BULK ≋≋{DM+WH}  ║{R}   {BCY}← the higher void the sheet ripples through{R}
{DM+WH}                     ║ {GR}SHORTCUT▓▓  {DM+WH} ║{R}
{DM+WH}                     ╠══════════════╣{R}
{DM+WH}                    /║\\{DM+WH}            /║\\{R}
{DM+WH}                   / ║ \\{DM+WH}          / ║ \\{R}
{DM+WH}                  /  ║  \\{DM+WH}        /  ║  \\{R}
{DM+WH}═════════════════╧══╧══╧═════════════╧══╧══╧══════════{R}
"""
def entropy_well():
    return box_lines([
        f"{BYE}ENTROPY·WELL{R}",
        f"{BCY}≋ SLOW·WELL·GRADIENT ≋{R}",
        "",
        f"{YE}[ORDER]{R}{DM+WH}→{R}{BCY}[ANCHOR]{R}{DM+WH}→{R}{BL}[SHORTCUT]{R}",
        f"{BYE}battery  vault  network{R}",
        "",
        f"{BGR}FUTURE  ──→  GENTLE·SLOPE{R}",
        f"{BCY}PAST    ──→  STEEP·CLIMB{R}",
        "",
        f"{DM+WH}ANCHORS: 3  {R}{BGR}✓ HOLDS·OPEN{R}",
    ], color=DM+WH, style="ripple")
def sigma_forge():
    return box_lines([
        f"{BYE}Σ  THE·FORGE·OF·SHORTCUTS  Σ{R}",
        "",
        f"{BGR}RIDGE·CROSS{R}{DM+WH}→{R}{BYE}STRAIGHT·CUT{R}{DM+WH}→{R}{BMA}REJOIN{R}{DM+WH}→{R}{BCY}ARRIVAL{R}",
        "",
        f"{BRE}❌ PROPULSION{R}  {BGR}✓ NAVIGATION{R}",
        f"{BRE}❌ MORE·POWER{R}  {BGR}✓ RIGHT·PHASE·+·ANGLE{R}",
        f"{BRE}❌ RIDGE·TOP{R}   {BGR}✓ RIDGE·FLANK{R}",
        f"{BRE}❌ CHAOS{R}       {BGR}✓ ENTROPY·COUPLING{R}",
        "",
        f"{BCY}NODES:{R}{DM+WH} Arc-Length Time · Bulk Navigation{R}",
        f"{DM+WH}         Golden Windows · Anchors · Wells{R}",
        "",
        f"{BYE}PHASE 0{R}{DM+WH}: Proper time = arc length along τ{R}",
        f"{BYE}PHASE 1{R}{DM+WH}: Time-distance bridge (1s = 1 l-s){R}",
        f"{BYE}PHASE 2{R}{DM+WH}: Locate E_0 and φ — the Golden Window{R}",
        f"{BYE}PHASE 3{R}{DM+WH}: Launch off the flank, not the crest{R}",
        f"{BYE}PHASE 4{R}{DM+WH}: Kinematic rejoin — the straight cut{R}",
        f"{BYE}PHASE 5{R}{DM+WH}: Anchor the manifold — build, don't{R}",
        f"{DM+WH}         dissolve — keep the shortcuts open{R}",
        "",
        f"{DM+WH}FRAMEWORK: Sigma-Manifold · MEDIUM: The Bulk{R}",
    ], color=DM+WH, style="ripple", corners="╔╗╚╝", horiz="═")
def hilltop_art():
    return box_lines([
        f"{BGR}H·I·L·L·T·O·P{R}",
        f"{DM+WH}The Feeling You Get At A Ridge-Crest{R}",
        f"{DM+WH}Where The Normal Points Into The Void{R}",
        "",
        f"{BYE}∿{R} {DM+WH}The surface always had a slope to it.{R}",
        f"{BYE}γ{R} {DM+WH}The straight cut runs the shortest course.{R}",
        f"{BYE}φ{R} {DM+WH}Launch angle: intrinsic, unforgiving.{R}",
        f"{BMA}⊗{R} {DM+WH}Kinematic rejoin: no guarantee, ever.{R}",
        f"{DM+WH}∂ Ridge boundary: reluctant. One flank over.{R}",
        "",
        f"{BCY}PHASE→WINDOW · ANGLE→TRAJECTORY{R}",
        f"{BGR}ORDER→ANCHOR·OF·THE·MANIFOLD{R}",
        f"{BYE}CARRIER·WAVE · NEVER·GUARANTEED{R}",
    ], color=DM+WH, style="ripple")
def specs_banner():
    return box_lines([
        f"{BYE}Σ·MANIFOLD  OPEN·THEOREM·SPECS{R}",
        "__DIV__",
        f"{BGR}01{R} · {BWH}ARC·LENGTH·τ{R}     {DM+WH}proper time = distance along the sheet{R}",
        f"{BGR}02{R} · {BWH}GOLDEN·WINDOW{R}    {DM+WH}phase E_0 + angle φ, not raw power{R}",
        f"{BGR}03{R} · {BWH}HILLTOP·FEELING{R}  {DM+WH}ridge-crest launch, no rejoin, ever{R}",
        f"{BGR}04{R} · {BWH}ENTROPY·COUPLING{R} {DM+WH}order anchors the manifold's shortcuts{R}",
        f"{BGR}05{R} · {BWH}ENTROPY·WELL{R}     {DM+WH}gentle future slope, steep past climb{R}",
        "__DIV__",
        f"{DM+WH}ALL SPECS: proven curvature · wrong launch angle · now fixed{R}",
        f"{DM+WH}LICENSE: open · free · before breakfast · no permission{R}",
    ], color=BYE, style="ripple", corners="╔╗╚╝", horiz="═", divider_corners="╠╣")
PHILOSOPHY = [
    (BMA, "  ·  INVERSION·ENGINE  ·"),
    (BCY, "  See the tick. Imagine the arc length underneath it. Walk that."),
    (BYE, "  The gap between what a clock COUNTS and what the surface"),
    (BGR, "  actually COVERS is where every ripple of τ lives."),
    (BWH, ""),
    (BRE, "  You cannot skip the ridges by wishing for a shorter watch."),
    (BRE, "  You cannot launch from the crest and expect a rejoin."),
    (BRE, "  You cannot anchor a shortcut with a civilization in freefall."),
    (BWH, ""),
    (BGR, "  That is exactly why the flank is safer than the summit."),
    (BGR, "  That is exactly why we build instead of drifting."),
    (BWH, ""),
    (BYE, "  RIPPLE·TO·REJOIN"),
    (BYE, "  Given away free. Before breakfast. No permission required."),
    (BWH, ""),
    (BCY, "  The Bulk is enough."),
    (BCY, "  We just have to hold our anchor open."),
]
MANTRA = [
    "  BUILD·REALITY·BY·ANCHORING",
    "  LEARN·BY·NAVIGATING",
    "  LEAVE·EVERY·SHORTCUT·OPENER·THAN·YOU·FOUND·IT",
]
def keth_profile():
    return box_lines([
        f"{BMA}Σ'NAVIGATOR{R} {DM+WH}:: PHASE·ANGLE · PATTERN·RECOGNITION{R}",
        "",
        f"{BYE}~all yrs{R}{DM+WH}: geometry · thermodynamics · navigation{R}",
        f"{DM+WH}          organization theory · entropy · anchoring{R}",
        "",
        f"{BGR}METHOD{R}{DM+WH}: find the window, not the engine{R}",
        f"{DM+WH}        not brute force. ridge-flank seeing.{R}",
        "",
        f"{BCY}TOOLS{R}{DM+WH}: Arc-Length · Launch·Angles · Anchors{R}",
        f"{BCY}ARCHIVE{R}{DM+WH}: The Bulk · Σ-MANIFOLD·CANON{R}",
        f"{BCY}PLATFORM{R}{DM+WH}: porch · carrier wave · tea · the well{R}",
        "",
        f"{BMA}SIMULTANEOUSLY SILLY AND SERIOUS ABOUT IT.{R}",
        f"{BMA}THAT IS NOT A CONTRADICTION.{R}",
        f"{BMA}THAT IS THE WHOLE THING.{R}",
    ], color=DM+WH, style="ripple")
def golden_window_verse():
    return box_lines([
        f"{BMA}THE·GOLDEN·WINDOW  ::  NARROW{R}",
        "",
        f"{DM+WH}It opens for no reason but the ripple.{R}",
        f"{DM+WH}It admits no brute-force velocity.{R}",
        f"{DM+WH}It rewards no raw amount of thrust.{R}",
        f"{DM+WH}It forgives no wrong angle, ever.{R}",
        "",
        f"{BMA}It is simply geometric.{R}",
        f"{BMA}Precise. As is correct.{R}",
        "",
        f"{DM+WH}The Bulk stretches out everywhere.{R}",
        f"{DM+WH}One window does not need to.{R}",
    ], color=MA, style="ripple")
SONG_FRAGMENT = f"""
{DM+WH}  ── σ·MANIFOLD·THEORY (song) ──────────────────────────────
{BRE}  They told me a second's a tick on the wall,
{BRE}  I say a second's a road, and the road isn't small,
{BRE}  Every ridge that I walk, every valley I cross,
{BRE}  Is a mile that I'm paying — call it time, call it cost.
{BWH}
{BYE}  BUMPY ROAD — I'm not counting hours no more,
{BYE}  I'm counting the distance from ridge back to shore,
{BYE}  Cut through the Bulk and the wiggles unwind,
{BYE}  Same place on the sheet, less road left behind.
{BWH}
{BGR}  Find me the phase, find me the angle just right,
{BGR}  Golden window don't open on power or might,
{BMA}  Launch from the flank where the ridges run deep,
{BMA}  Launch from the crest and you're gone — for keeps.
{BWH}
{BCY}  Build me a battery, a vault, and a line,
{BCY}  Network holds steady, keeps the shortcut aligned,
{BCY}  Order's the anchor that holds the road true,
{BCY}  Let it dissolve, and the window closes on you.
{BWH}
{BGR}  Future's a gentle slope, easy to glide,
{BGR}  Past is a mountain — steeper the deeper you ride
{R}
  {DM+WH}── end fragment ──────────────────────────────────────────{R}
"""
def closing():
    return box_lines([
        f"{BCY}Σ·CANON  ::  TRANSMISSION·END{R}",
        "__DIV__",
        f"{DM+WH}Not a shorter clock. A straighter cut.{R}",
        f"{DM+WH}Proven geometry. Wrong launch angle. Now fixed.{R}",
        "",
        f"{BGR}The clock is an artifact.{R}",
        f"{BGR}The road is real.{R}",
        f"{BGR}The ridge-flank is forgiving.{R}",
        f"{BGR}The ridge-crest is not.{R}",
        f"{BGR}The anchor is us.{R}",
        "",
        f"{BYE}Σ·MANIFOLD  :: THE·BULK · OPEN · PERMANENT{R}",
        f"{BMA}🄯·Riverboatt::{R}          ·      ·",
        f"{DM}🙇·Keth'ar Molishé Nuvah'el:: always knew{R}",
        
    ], color=BCY, style="ripple", corners="╔╗╚╝", horiz="═", divider_corners="╠╣")
# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    cls()
    w = min(width(), 120)
    # ── HEADER ────────────────────────────────────────────────────────────────
    particle_burst(2, w)
    print()
    pulse("Σ · M A N I F O L D", cycles=5, colors=[BYE, BMA, BCY, BGR, BWH])
    pulse("THEORY  ·  CANON  ·  TRANSMISSION", cycles=3, colors=[BWH, BYE, BCY])
    print()
    wave_line("  ≋ ≋ ≋  TIME·IS·A·BUMPY·ROAD·NOT·A·CLOCK  ≋ ≋ ≋",
              [BYE, BMA, BCY, BGR, BWH, BCY, BMA])
    print()
    particle_burst(1, w)
    print()
    delay(0.3)
    # ── TRIPLE WAVE ──────────────────────────────────────────────────────────
    rule("═", BYE, w)
    print(c(DM+WH, "  SYSTEM·WAVEFORMS  ::  RIDGE · BULK · WELL"))
    rule("─", DM+WH, w)
    triple_wave(cycles=3)
    rule("═", BYE, w)
    print()
    delay(0.2)
    # ── PROFILE ───────────────────────────────────────────────────────────────
    scroll(keth_profile(), 0.015)
    print()
    delay(0.2)
    # ── SPECS ────────────────────────────────────────────────────────────────
    scroll(specs_banner(), 0.025)
    print()
    delay(0.3)
    # ── THE BULK ─────────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BYE, "  SPEC·01  ::  THE·SIGMA·MANIFOLD·&·THE·BULK"))
    rule("─", DM+WH, w)
    scroll(BULK_ART.split("\n"), 0.018)
    delay(0.2)
    # ── ENTROPY WELL ─────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BCY, "  SPEC·05  ::  ENTROPY·WELL"))
    rule("─", DM+WH, w)
    scroll(entropy_well(), 0.018)
    print()
    delay(0.2)
    # ── FORGE OF SHORTCUTS ───────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BYE, "  PROJECT  ::  THE·FORGE·OF·SHORTCUTS  ::  SMT·NAVIGATION"))
    rule("─", DM+WH, w)
    scroll(sigma_forge(), 0.018)
    print()
    delay(0.2)
    # ── HILLTOP ──────────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    print(bo(BGR, "  PROJECT  ::  H·I·L·L·T·O·P"))
    rule("─", DM+WH, w)
    scroll(hilltop_art(), 0.018)
    print(c(BRE, "  ⚠ STEAM!  ⚠ BASSQUAKE!  — telemetry ping off the ridge-flank sensors."))
    print()
    delay(0.2)
    # ── GOLDEN WINDOW VERSE ──────────────────────────────────────────────────
    particle_burst(1, w)
    scroll(golden_window_verse(), 0.04)
    particle_burst(1, w)
    print()
    delay(0.3)
    # ── PHILOSOPHY ───────────────────────────────────────────────────────────
    rule("═", BMA, w)
    print(bo(BMA, "  INVERSION·ENGINE  ::  Σ·MANIFOLD·DOCTRINE"))
    rule("─", DM+WH, w)
    for col, line in PHILOSOPHY:
        print(c(col, line))
        delay(0.04)
    print()
    delay(0.2)
    # ── SONG FRAGMENT ────────────────────────────────────────────────────────
    rule("─", DM+WH, w)
    scroll(SONG_FRAGMENT.split("\n"), 0.022)
    print()
    delay(0.2)
    # ── MANTRA ───────────────────────────────────────────────────────────────
    rule("═", BGR, w)
    for line in MANTRA:
        pulse(line, cycles=2, colors=[BGR, BWH, BYE, BGR])
    rule("═", BGR, w)
    print()
    delay(0.3)
    # ── PARTICLE FINALE ───────────────────────────────────────────────────────
    for i in range(4):
        spark_line(w)
        delay(0.06)
    # ── CLOSING ──────────────────────────────────────────────────────────────
    scroll(closing(), 0.03)
    # ── FINAL PULSE ──────────────────────────────────────────────────────────
    pulse("≋  Σ  ≋", cycles=6, colors=[BMA, BWH, BCY, BYE, BMA, BCY])
    print()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c(DM+WH, '  transmission interrupted. the anchor remains.')}\n")
