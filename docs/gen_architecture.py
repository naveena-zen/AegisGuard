"""
gen_architecture.py -- Generates AegisGuard architecture diagram as PNG.
Run: python docs/gen_architecture.py
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# ---------- Canvas ----------------------------------------------------------
W, H = 1800, 920
BG      = (8, 12, 28)
GRID    = (16, 24, 50)
CYAN    = (34, 211, 238)
BLUE    = (59, 130, 246)
GREEN   = (52, 211, 153)
RED     = (248, 113, 113)
AMBER   = (251, 191, 36)
PURPLE  = (167, 139, 250)
WHITE   = (255, 255, 255)
LGRAY   = (175, 190, 215)
DGRAY   = (75, 90, 120)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ---------- Fonts -----------------------------------------------------------
def font(size):
    for p in ("C:/Windows/Fonts/segoeui.ttf",
              "C:/Windows/Fonts/arial.ttf",
              "C:/Windows/Fonts/calibri.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

F22 = font(22); F16 = font(16); F14 = font(14)
F12 = font(12); F11 = font(11); F10 = font(10)

# ---------- Helpers ---------------------------------------------------------
def ctext(x, y, txt, fnt, col):
    bb = draw.textbbox((0,0), txt, font=fnt)
    tw = bb[2]-bb[0]; th = bb[3]-bb[1]
    draw.text((x-tw//2, y-th//2), txt, font=fnt, fill=col)

def rbox(x0,y0,x1,y1, fill, border, r=10):
    for i in range(3, 0, -1):
        gc = tuple(int(c*0.1*i) for c in border)
        draw.rounded_rectangle((x0-i*3,y0-i*3,x1+i*3,y1+i*3), radius=r+i*3, outline=gc, width=1)
    draw.rounded_rectangle((x0,y0,x1,y1), radius=r, fill=fill, outline=border, width=2)

def edge(box, s):
    x0,y0,x1,y1 = box
    cx,cy = (x0+x1)//2,(y0+y1)//2
    return {"r":(x1,cy),"l":(x0,cy),"t":(cx,y0),"b":(cx,y1)}[s]

def arr(p1,p2,col,w=2,hs=9,lbl="",lfnt=None,lox=0,loy=-13):
    x1,y1=p1; x2,y2=p2
    dx,dy=x2-x1,y2-y1
    if math.hypot(dx,dy)<1: return
    draw.line([p1,p2], fill=col, width=w)
    ang=math.atan2(dy,dx)
    for s in(-1,1):
        draw.line([(x2,y2),(x2-hs*math.cos(ang-s*math.pi/7),
                             y2-hs*math.sin(ang-s*math.pi/7))], fill=col, width=w+1)
    if lbl and lfnt:
        ctext((x1+x2)//2+lox,(y1+y2)//2+loy,lbl,lfnt,col)

# ---------- Grid & Title ----------------------------------------------------
for gx in range(0,W,70): draw.line([(gx,0),(gx,H)], fill=GRID, width=1)
for gy in range(0,H,70): draw.line([(0,gy),(W,gy)], fill=GRID, width=1)

draw.rectangle([(0,0),(W,55)], fill=(10,16,45))
draw.line([(0,55),(W,55)], fill=BLUE, width=2)
ctext(W//2, 28, "AegisGuard -- Autonomous Security Monitoring & Threat Investigation Agent", F22, WHITE)

# ---------- Legend (top-right) ----------------------------------------------
lx, ly = W-290, 68
for col, lbl in [(CYAN,"Telemetry / Data Flow"),(GREEN,"Auto-Containment"),
                 (RED,"Human Escalation"),(PURPLE,"LLM Interaction"),(AMBER,"Policy Decision")]:
    draw.line([(lx,ly+5),(lx+24,ly+5)], fill=col, width=3)
    draw.polygon([(lx+24,ly+5),(lx+17,ly+2),(lx+17,ly+8)], fill=col)
    draw.text((lx+30,ly), lbl, font=F11, fill=LGRAY)
    ly += 17

# ============================================================================
#  Layout
# ============================================================================
BW, BH = 252, 64
CX = [55, 345, 640, 965, 1290, 1550]
RY = [80, 245, 430, 615, 780]

def B(c,r): return (CX[c], RY[r], CX[c]+BW, RY[r]+BH)

boxes = {
    "frontend":  B(1,0),   # React frontend
    "backend":   B(2,0),   # FastAPI
    "telemetry": B(0,1),   # Telemetry Collector
    "detection": B(1,1),   # Detection Engine
    "phase1":    B(2,1),   # Phase 1 Agent
    "policy":    B(3,1),   # Policy Engine
    "autoact":   B(5,0),   # Auto-Containment  (top right)
    "escalate":  B(5,1),   # Human Escalation
    "db":        B(0,2),   # PostgreSQL
    "llm":       B(2,2),   # Groq LLM
    "smtp":      B(5,3),   # SMTP
}

STYLES = {
    "frontend":  ((8,28,58),  BLUE,   "React Security Console",       "Vite  |  JWT Auth"),
    "backend":   ((8,35,62),  BLUE,   "FastAPI Backend",               "REST API  |  Auth  |  JWT"),
    "telemetry": ((6,36,50),  CYAN,   "Telemetry Collector",          "psutil / Synthetic  (5s loop)"),
    "detection": ((6,36,65),  CYAN,   "Detection Engine",             "Rule-based threshold monitoring"),
    "phase1":    ((26,14,58), PURPLE, "Phase 1 Investigation Agent",  "LLM Read-Only Loop  (Groq)"),
    "policy":    ((50,36,8),  AMBER,  "Policy Engine",                "Deterministic Safety Gate"),
    "autoact":   ((6,42,26),  GREEN,  "Automated Containment",        "Restart / Rollback  (Simulated)"),
    "escalate":  ((50,12,18), RED,    "Human Analyst Escalation",     "Page SOC Engineer"),
    "db":        ((6,30,55),  BLUE,   "PostgreSQL + pgvector",        "Metrics  Logs  Incidents  RAG"),
    "llm":       ((26,12,58), PURPLE, "Groq LLM API",                 "llama-3.3-70b-versatile"),
    "smtp":      ((42,14,22), RED,    "SMTP / Pager",                 "Email alert to analyst"),
}

# --- Swimlane backgrounds ---------------------------------------------------
# Row 0: Client & API
draw.rounded_rectangle((CX[1]-12, RY[0]-18, CX[2]+BW+12, RY[0]+BH+18),
                        radius=14, fill=(10,25,52), outline=(30,50,90), width=1)
draw.text((CX[1]-8, RY[0]-16), "Client & Backend", font=F10, fill=DGRAY)

# Main pipeline row (row 1)
draw.rounded_rectangle((CX[0]-12, RY[1]-20, CX[3]+BW+12, RY[1]+BH+20),
                        radius=14, fill=(12,22,48), outline=(28,48,80), width=1)
draw.text((CX[0]-8, RY[1]-18), "Security Pipeline", font=F10, fill=DGRAY)

# Storage row (row 2)
draw.rounded_rectangle((CX[0]-12, RY[2]-18, CX[0]+BW+12, RY[2]+BH+18),
                        radius=14, fill=(8,25,48), outline=(22,42,72), width=1)
draw.text((CX[0]-8, RY[2]-16), "Storage Layer", font=F10, fill=DGRAY)

# LLM row (row 2, col 2)
draw.rounded_rectangle((CX[2]-12, RY[2]-18, CX[2]+BW+12, RY[2]+BH+18),
                        radius=14, fill=(22,10,52), outline=(45,25,80), width=1)
draw.text((CX[2]-8, RY[2]-16), "LLM Provider", font=F10, fill=DGRAY)

# Output column
draw.rounded_rectangle((CX[5]-12, RY[0]-18, CX[5]+BW+12, RY[3]+BH+18),
                        radius=14, fill=(35,10,38), outline=(60,22,60), width=1)
draw.text((CX[5]-8, RY[0]-16), "Output Actions", font=F10, fill=DGRAY)

# --- Draw boxes -------------------------------------------------------------
for key, box in boxes.items():
    fill, border, title, sub = STYLES[key]
    x0,y0,x1,y1 = box
    rbox(x0,y0,x1,y1, fill, border, r=10)
    ctext((x0+x1)//2, y0+20, title, F14, WHITE)
    ctext((x0+x1)//2, y0+44, sub,   F11, LGRAY)

# --- Phase step labels ------------------------------------------------------
PHASE = {
    "telemetry": (1,"DETECT",   CYAN),
    "detection": (1,"DETECT",   CYAN),
    "phase1":    (2,"INVESTIGATE", PURPLE),
    "policy":    (3,"GATE",    AMBER),
    "autoact":   ("4a","AUTO-CONTAIN", GREEN),
    "escalate":  ("4b","ESCALATE", RED),
}
for key,(n,ph,col) in PHASE.items():
    x0,y0,_,_ = boxes[key]
    draw.text((x0+2, y0-17), f"[{n}] {ph}", font=F10, fill=col)

# --- Read-Only Tools panel --------------------------------------------------
px0 = CX[2]
py0 = RY[1]+BH+14
draw.rounded_rectangle((px0, py0, px0+BW, py0+68), radius=7,
                        fill=(18,10,44), outline=PURPLE, width=1)
draw.text((px0+6, py0+4),  "Read-Only Tools (LLM cannot write):", font=F10, fill=PURPLE)
draw.text((px0+6, py0+20), "get_metrics()  |  get_logs()",         font=F10, fill=LGRAY)
draw.text((px0+6, py0+36), "get_recent_deploys()",                  font=F10, fill=LGRAY)
draw.text((px0+6, py0+52), "search_similar_incidents()  [pgvector]",font=F10, fill=LGRAY)

# --- Policy gate condition --------------------------------------------------
px = (boxes["policy"][0]+boxes["policy"][2])//2
py = boxes["policy"][3]+8
draw.text((px-145, py), "confidence >= 80  AND  allowlist  AND  != local-host",
          font=F10, fill=AMBER)

# ============================================================================
#  Arrows   (start far enough from box edge to not overlap glow)
# ============================================================================
LOFF = 12  # standard label y-offset above mid

# 1. Frontend -> Backend
arr(edge(boxes["frontend"],"r"), edge(boxes["backend"],"l"),
    BLUE, lbl="Login / API calls", lfnt=F10, loy=-LOFF)

# 2. Backend -> Telemetry (loop management, dashed look via thin line)
arr((boxes["backend"][0], boxes["backend"][3]),
    (boxes["telemetry"][2], boxes["telemetry"][1]),
    BLUE, w=1, hs=7, lbl="starts loop", lfnt=F10, loy=8)

# 3. Telemetry -> Detection Engine
arr(edge(boxes["telemetry"],"r"), edge(boxes["detection"],"l"),
    CYAN, lbl="anomaly check", lfnt=F10, loy=-LOFF)

# 4. Detection -> Phase 1
arr(edge(boxes["detection"],"r"), edge(boxes["phase1"],"l"),
    CYAN, lbl="anomaly trigger", lfnt=F10, loy=-LOFF)

# 5. Telemetry -> DB  (write telemetry)
arr(edge(boxes["telemetry"],"b"), edge(boxes["db"],"t"),
    CYAN, lbl="write telemetry", lfnt=F10, lox=-62, loy=0)

# 6. Phase1 -> LLM  (tool calls, offset left)
arr((boxes["phase1"][0]+50, boxes["phase1"][3]),
    (boxes["llm"][0]+50,    boxes["llm"][1]),
    PURPLE, lbl="tool calls -->", lfnt=F10, lox=-62, loy=0)

# 7. LLM -> Phase1  (completions, offset right)
arr((boxes["llm"][0]+160,   boxes["llm"][1]),
    (boxes["phase1"][0]+160, boxes["phase1"][3]),
    PURPLE, lbl="<-- completions", lfnt=F10, lox=66, loy=0)

# 8. Phase1 -> DB  (reads logs/metrics/deploys)
arr((boxes["phase1"][0]+30, boxes["phase1"][3]),
    (boxes["db"][2]-15,     boxes["db"][1]),
    BLUE, w=2, lbl="reads: logs / metrics / deploys", lfnt=F10, loy=-LOFF)

# 9. DB -> Phase1  (pgvector results, offset)
arr((boxes["db"][0]+20,      boxes["db"][1]),
    (boxes["phase1"][0]+5,   boxes["phase1"][3]),
    BLUE, w=1, hs=7, lbl="pgvector RAG results", lfnt=F10, loy=14)

# 10. Phase1 -> Policy  (terminal JSON)
arr(edge(boxes["phase1"],"r"), edge(boxes["policy"],"l"),
    AMBER, lbl="terminal JSON", lfnt=F10, loy=-LOFF)

# 11. Policy -> AutoAct  (pass)
arr(edge(boxes["policy"],"r"), edge(boxes["autoact"],"l"),
    GREEN, lbl="PASS: auto-act", lfnt=F10, loy=-LOFF)

# 12. Policy -> Escalate  (fail)
arr(edge(boxes["policy"],"r"), edge(boxes["escalate"],"l"),
    RED,   lbl="FAIL: page SOC", lfnt=F10, loy=14)

# 13. AutoAct -> DB  (add resolved to RAG)
arr((boxes["autoact"][0]+100, boxes["autoact"][3]),
    (boxes["db"][2],           boxes["db"][1]),
    GREEN, w=1, hs=7, lbl="add resolved to RAG", lfnt=F10, loy=-LOFF)

# 14. Escalate -> SMTP
arr(edge(boxes["escalate"],"b"), edge(boxes["smtp"],"t"),
    RED, lbl="SMTP email", lfnt=F10, lox=-48, loy=0)

# ============================================================================
#  Footer
# ============================================================================
draw.line([(0,H-28),(W,H-28)], fill=(22,34,65), width=1)
draw.text((16,H-20), "AegisGuard v1.0  |  github.com/naveena-zen/AegisGuard", font=F10, fill=DGRAY)
draw.text((W-580, H-20),
          "Phase 1: LLM read-only investigation   |   Phase 2: Deterministic policy gate (no LLM)",
          font=F10, fill=DGRAY)

# ============================================================================
#  Save
# ============================================================================
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "architecture.png")
img.save(out, "PNG", optimize=True)
print(f"[OK] Saved: {out}  ({W}x{H}px)")
