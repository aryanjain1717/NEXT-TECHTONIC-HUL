import json
from pathlib import Path
from datetime import datetime

import streamlit as st

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

st.set_page_config(
    page_title="NEXT Radar — Project NEXT",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open(DATA / "events.json", "r", encoding="utf-8") as f:
    EVENT_DATA = json.load(f)
with open(DATA / "brand_memory.json", "r", encoding="utf-8") as f:
    BRAND_MEMORY = json.load(f)

HERO = next(e for e in EVENT_DATA["events"] if e.get("hero"))
DEFAULT_W = {
    "Brand Relevance": 20,
    "Momentum": 30,
    "Novelty": 20,
    "Commercial Signal": 15,
    "Actionability": 15,
}
SCORE_KEYS = {
    "Brand Relevance": "brand_relevance",
    "Momentum": "momentum",
    "Novelty": "novelty",
    "Commercial Signal": "commercial_signal",
    "Actionability": "actionability",
}

if "page" not in st.session_state:
    st.session_state.page = "Radar Home"
if "decision" not in st.session_state:
    st.session_state.decision = None
if "audit" not in st.session_state:
    st.session_state.audit = [
        ("09 Jul 2024 · 11:20", "Opportunity snapshot scored with AXE-v1.0. ROS 84.30; Risk 25; OPS 78.05 → High Priority."),
        ("09 Jul 2024 · 11:19", "Opportunity & Risk Agent wrote Actionability 84 and Risk 25 with evidence pointers."),
        ("09 Jul 2024 · 11:19", "Momentum Engine = 95; Novelty Engine = 91; Commercial Signal Engine = 60."),
        ("09 Jul 2024 · 11:18", "Brand Intelligence Agent ranked Axe 80, Dove 46, Rexona 32, Knorr 14."),
        ("09 Jul 2024 · 11:18", "Signal Intelligence Agent updated event cluster CUL-240607-BRAT from new evidence."),
    ]

st.markdown(
    """
<style>
.stApp {background: linear-gradient(180deg,#06101d,#081522); color:#eef5fb;}
[data-testid="stSidebar"] {background:#07111f; border-right:1px solid #203650;}
[data-testid="stSidebar"] * {color:#dbe9f5;}
.block-container {padding-top:1.4rem; padding-bottom:3rem; max-width:1480px;}
h1,h2,h3 {letter-spacing:-0.02em;}
.smallcap {font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color:#5bd0ff; font-weight:800;}
.muted {color:#9fb0c4; font-size:.9rem;}
.panel {border:1px solid #203650; background:linear-gradient(180deg,#0d1c2f,#0a1727); border-radius:14px; padding:16px; margin-bottom:12px;}
.metricbox {border:1px solid #203650; background:#0d1c2f; border-radius:14px; padding:14px; min-height:106px;}
.metricbox .label {font-size:.68rem; color:#8ea2b7; text-transform:uppercase; letter-spacing:.08em;}
.metricbox .value {font-size:1.8rem; font-weight:900; margin:.15rem 0;}
.pill {display:inline-block; padding:4px 8px; margin-right:5px; margin-bottom:5px; border:1px solid #31506b; border-radius:999px; font-size:.65rem; color:#bdd0e1;}
.pill.high {border-color:#7a5734;color:#ffd09a;background:#281c11;}
.pill.public {border-color:#1c806b;color:#88ebcc;background:#0d2a28;}
.pill.demo {border-color:#8b6932;color:#ffd783;background:#2a2110;}
.pill.synthetic {border-color:#6b4f91;color:#d2b8ff;background:#21182c;}
.pill.ai {border-color:#436d9c;color:#9ed1ff;background:#10243b;}
.event {border:1px solid #203b55; background:#0b1b2c; border-radius:12px; padding:13px; margin-bottom:9px;}
.event h4 {margin:0 0 4px 0; font-size:1rem;}
.scorebig {font-size:2.8rem; font-weight:950; line-height:1;}
.successbox {border:1px solid #24735e;background:#0c2a23;color:#9df0d1;padding:13px;border-radius:11px;}
.warningbox {border:1px solid #705530;background:#251c0e;color:#ffcf8a;padding:11px;border-radius:10px;font-size:.8rem;}
hr {border-color:#203650 !important;}
</style>
""",
    unsafe_allow_html=True,
)


def calc_ops(weights):
    total = sum(weights.values())
    if total != 100:
        return None
    scores = HERO["scores"]
    ros = sum(weights[name] * scores[SCORE_KEYS[name]] for name in weights) / 100
    ops = ros - 0.25 * scores["risk"]
    return ros, ops


def route_band(v):
    if v >= 85:
        return "Critical"
    if v >= 70:
        return "High Priority"
    if v >= 55:
        return "Emerging"
    if v >= 40:
        return "Watch"
    return "Archive"


def ask_radar(q):
    t = q.lower()
    if "critical" in t:
        return (
            "Momentum is exceptionally strong at 95, but Radar does not equate virality with a Critical brand opportunity. "
            "Commercial Signal is 60 because direct India-specific fragrance/commercial corroboration is limited, and Risk is 25 due to authenticity and timing concerns. "
            "Those constraints reduce ROS 84.3 to OPS 78.1, which routes to High Priority."
        )
    if "axe" in t and "dove" in t:
        return (
            "Axe ranks higher because Brat overlaps more strongly with youth culture, music, playful self-expression and fragrance-led identity in the governed Axe Brand Memory. "
            "Dove has some identity/self-expression overlap, but the event is less directly connected to Dove's core beauty and self-esteem territory."
        )
    if "commercial" in t:
        return (
            "Commercial Signal is 60. Radar has strong cultural evidence, but only moderate controlled/synthetic evidence of India-specific search, e-commerce or category demand linked to Axe. "
            "The system therefore avoids turning cultural heat into an unsupported commercial claim."
        )
    if "risk" in t:
        return (
            "Risk is 25/100. The main concerns are forced or inauthentic participation, timing risk as the meme cycle saturates, and cultural/IP sensitivities. "
            "Risk is modeled separately and subtracts 6.25 points from ROS."
        )
    if "momentum" in t and "20" in t:
        alt = {"Brand Relevance": 25, "Momentum": 20, "Novelty": 25, "Commercial Signal": 15, "Actionability": 15}
        ros, ops = calc_ops(alt)
        return f"Simulation only: with a normalized 25/20/25/15/15 profile, OPS becomes {ops:.1f} ({route_band(ops)}). The live AXE-v1.0 profile remains unchanged until centrally approved."
    if "recent" in t or "changed" in t:
        return (
            "The latest meaningful change in the replay window is stronger cross-category cultural reuse and continued signal acceleration. "
            "That primarily lifts Momentum and supports Actionability, while Commercial Signal remains the weakest positive factor."
        )
    if "score" in t or "ops" in t:
        return (
            "The deterministic engine calculates ROS = 84.30 using the approved AXE-v1.0 weights. Risk 25 creates a 6.25-point penalty, producing OPS 78.05, displayed as 78.1. "
            "Ask Radar explains the score but cannot overwrite it."
        )
    return "I am grounded in the frozen Brat Summer dossier, governed Brand Memory and deterministic score outputs. Ask about the Critical threshold, brand routing, Commercial Signal, Risk, score drivers or a weight counterfactual."


st.sidebar.markdown("## 📡 NEXT RADAR")
st.sidebar.caption("PROJECT NEXT")
st.sidebar.markdown("**Historical Replay**  \\n09 Jul 2024")
st.sidebar.caption("Point-in-time evidence only")
st.sidebar.divider()
for page in ["Radar Home", "Opportunity Dossier", "Ask Radar", "Decision & Handoff"]:
    if st.sidebar.button(page, use_container_width=True, type="primary" if st.session_state.page == page else "secondary"):
        st.session_state.page = page
        st.rerun()
st.sidebar.divider()
st.sidebar.caption("Controlled competition prototype. Synthetic internal data is visibly labelled.")

page = st.session_state.page
st.markdown(f'<div class="smallcap">Project NEXT / {page}</div>', unsafe_allow_html=True)

if page == "Radar Home":
    st.title("Market signal command center")
    st.markdown('<div class="muted">Radar clusters noisy signals into evolving events, compares them across the portfolio, and only interrupts Brand Managers when an opportunity crosses a meaningful priority threshold.</div>', unsafe_allow_html=True)
    st.write("")
    cols = st.columns(4)
    stats = [("Signals scanned","18.4K","Controlled demo input"),("Event clusters","126","Deduplicated"),("Brand-relevant","14","Portfolio routing passed"),("Priority alerts","4","1 Critical · 3 High")]
    for c,(lab,val,sub) in zip(cols,stats):
        c.markdown(f'<div class="metricbox"><div class="label">{lab}</div><div class="value">{val}</div><div class="muted">{sub}</div></div>', unsafe_allow_html=True)
    st.write("")
    left,right = st.columns([1.5,.8])
    with left:
        st.subheader("Opportunity feed")
        feed = [
            ("Rexona × stoppage-time moment","Rexona",98,86.0,"Critical","Accidental on-camera brand moment accelerates through football meme culture."),
            ("Brat Summer","Axe",80,78.1,"High Priority","Music, meme and visual-language phenomenon spreads beyond the original fan community."),
            ("Girl Dinner","Knorr",82,79.7,"High Priority","Low-prep food behavior becomes a reusable social format and convenience conversation."),
            ("Barbie beauty discourse","Dove",85,73.9,"High Priority","Representation and beauty-standard conversation creates a purpose-linked opportunity."),
            ("UEFA Euro 2024 semi-final chatter","Rexona",74,64.2,"Emerging","High-volume sports discussion routed primarily toward movement/sport territories."),
            ("Inside Out 2 emotion-meme wave","Dove",46,48.7,"Watch","Broad entertainment signal with limited direct relevance to Axe."),
            ("Wimbledon fashion conversation","Axe",42,43.1,"Watch","Event-linked style chatter does not pass the high-priority threshold."),
            ("UK election visual meme cycle","Axe",18,28.0,"Archive","High visibility, low brand fit; retained for context but not promoted."),
        ]
        for title,brand,match,ops,band,desc in feed:
            st.markdown(f'<div class="event"><h4>{title}</h4><div class="muted">{desc}</div><br/><span class="pill">{brand} match {match}</span><span class="pill {"high" if band=="High Priority" else ""}">OPS {ops:.1f} · {band}</span></div>', unsafe_allow_html=True)
            if title == "Brat Summer" and st.button("Open Brat Summer dossier", key="open_brat"):
                st.session_state.page = "Opportunity Dossier"
                st.rerun()
    with right:
        st.subheader("Portfolio routing — Brat Summer")
        for brand,score in HERO["brand_matches"].items():
            st.write(f"**{brand}** · {score}/100")
            st.progress(score/100)
        st.markdown('<div class="warningbox">Portfolio-first routing happens before full opportunity scoring. Only sufficiently relevant brands advance.</div>', unsafe_allow_html=True)

elif page == "Opportunity Dossier":
    st.title("Opportunity dossier")
    st.markdown('<div class="muted">VERIFY → UNDERSTAND → SCORE · one evidence-grounded object for the event and its brand decision.</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><span class="pill public">As of 09 Jul 2024</span><span class="pill high">HIGH PRIORITY</span><span class="pill">Top match: AXE</span><h2 style="margin-bottom:0">Brat Summer</h2><div class="scorebig">78.1</div><div class="muted">Opportunity Priority Score</div></div>', unsafe_allow_html=True)
    a,b = st.columns([1.15,.85])
    with a:
        st.subheader("What happened")
        st.markdown('<div class="panel">A distinctive music-and-visual culture around Charli XCX\'s <i>Brat</i> accelerated through social platforms, memes and brand participation. Radar treats this as one evolving event rather than thousands of individual posts.</div>', unsafe_allow_html=True)
        st.subheader("Why Axe")
        st.markdown('<div class="panel"><b>Strong semantic overlap:</b> youth culture, music, self-expression, playful irreverence and fragrance-led identity. This is Brand Memory matching, not keyword detection.</div>', unsafe_allow_html=True)
        for brand,score in HERO["brand_matches"].items():
            st.write(f"**{brand}** · {score}")
            st.progress(score/100)
        st.subheader("Evidence ledger")
        ev = [
            ("PUBLIC FACT","Cross-platform cultural acceleration","Public reporting before the cutoff described rapid spread of Brat-associated visual language, memes and brand participation."),
            ("CONTROLLED DEMO INPUT","Signal velocity series","Frozen timestamped mention/search trajectory used by the deterministic Momentum Engine."),
            ("AI-DERIVED","Axe Brand Memory retrieval","Youth/young-adult fragrance, playful self-expression and culturally fluent brand behavior."),
            ("SYNTHETIC INTERNAL","India commercial proxy","Illustrative internal/search/e-commerce proxies provide moderate corroboration only."),
            ("AI-DERIVED","Actionability rationale","Highly remixable for fast social response, with authenticity and timing constraints."),
        ]
        for typ,title,text in ev:
            st.markdown(f'<div class="event"><span class="pill">{typ}</span><h4>{title}</h4><div class="muted">{text}</div></div>', unsafe_allow_html=True)
    with b:
        st.subheader("Score decomposition")
        for name,key in SCORE_KEYS.items():
            score=HERO["scores"][key]
            st.write(f"**{name}** · {score}")
            st.progress(score/100)
        st.write(f"**Risk** · {HERO['scores']['risk']}")
        st.progress(HERO["scores"]["risk"]/100)
        st.code("ROS = .20(80)+.30(95)+.20(91)+.15(60)+.15(84) = 84.30\nRisk penalty = .25(25) = 6.25\nOPS = 84.30 - 6.25 = 78.05 ≈ 78.1")
        st.subheader("Why not Critical?")
        st.info("Momentum is exceptional, but India-specific commercial corroboration is still limited and the cultural connection remains indirect. Radar therefore triggers immediate Brand Manager review without treating virality alone as sufficient for Critical.")
        if st.button("Ask Radar about this", use_container_width=True):
            st.session_state.page = "Ask Radar"
            st.rerun()

elif page == "Ask Radar":
    st.title("Ask Radar")
    st.markdown('<div class="muted">Grounded conversational interrogation. Deterministic services remain the source of truth for mathematics.</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><b>Brat Summer · Axe · OPS 78.1</b><br/><span class="pill ai">GROUNDED</span></div>', unsafe_allow_html=True)
    prompts = ["Why isn't this Critical?", "Why Axe over Dove?", "Show evidence behind Commercial Signal", "What if Momentum weight falls to 20%?", "What evidence changed most recently?"]
    cols = st.columns(len(prompts))
    clicked = None
    for c,p in zip(cols,prompts):
        if c.button(p, use_container_width=True):
            clicked = p
    q = st.chat_input("Ask a grounded question…")
    if clicked:
        q = clicked
    if q:
        st.chat_message("user").write(q)
        st.chat_message("assistant").write(ask_radar(q))
        st.caption("Grounding: Brat dossier · Brand Memory · scoring profile AXE-v1.0")
    st.subheader("What-if scoring simulation")
    st.caption("Simulation only; production profile changes require central approval.")
    wc = st.columns(5)
    sim_w = {}
    for c,(name,default) in zip(wc,DEFAULT_W.items()):
        sim_w[name] = c.number_input(name, min_value=0, max_value=50, value=default, step=5)
    total=sum(sim_w.values())
    if total != 100:
        st.warning(f"Weights currently total {total}%. They must total 100%.")
    else:
        ros,ops=calc_ops(sim_w)
        st.metric("Simulated OPS", f"{ops:.1f}", route_band(ops))
        st.caption(f"ROS {ros:.2f} · Risk penalty 6.25 · AXE-v1.0 remains unchanged")

elif page == "Decision & Handoff":
    st.title("Human decision & Strategist handoff")
    st.markdown('<div class="muted">Radar prepares the complete opportunity package, but the Brand Manager owns the decision.</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Brat Summer × Axe</h3><span class="pill high">OPS 78.1 · High Priority</span><span class="pill">Risk 25</span></div>', unsafe_allow_html=True)
    cols=st.columns(4)
    actions=[("Approve → Strategist","approve"),("Watch","watch"),("Reject","reject"),("Escalate","escalate")]
    for c,(label,key) in zip(cols,actions):
        if c.button(label,use_container_width=True,type="primary" if key=="approve" else "secondary"):
            st.session_state.decision=key
            st.session_state.audit.insert(0,("09 Jul 2024 · human action",f"Brand Manager selected {key.upper()} for Brat Summer × Axe."))
    if st.session_state.decision == "approve":
        st.markdown('<div class="successbox">✓ Opportunity #AXE-2024-071 transferred to NEXT Strategist · Human approval recorded · complete audit trail preserved</div>', unsafe_allow_html=True)
        st.subheader("Structured handoff package")
        handoff={
            "Opportunity":"Brat Summer — emerging culture opportunity",
            "Brand":"Axe · strongest portfolio match",
            "Priority":"OPS 78.1 · High Priority",
            "Opportunity window":"Fast-moving; cultural saturation risk rising",
            "Core evidence":"Momentum acceleration, cross-category cultural reuse, strong youth-expression fit",
            "Key uncertainty":"Limited direct India-specific fragrance/commercial corroboration",
            "Risk context":"Forced participation / cultural-authenticity / timing risk",
        }
        c1,c2=st.columns(2)
        for i,(k,v) in enumerate(handoff.items()):
            (c1 if i%2==0 else c2).markdown(f'<div class="panel"><div class="smallcap">{k}</div><div>{v}</div></div>', unsafe_allow_html=True)
    elif st.session_state.decision:
        st.info(f"Decision recorded: {st.session_state.decision.upper()}. Evidence, score and rationale remain in the audit trail.")
    st.divider()
    with st.expander("Audit trail"):
        for t,e in st.session_state.audit:
            st.write(f"**{t}** — {e}")

st.divider()
st.caption("NEXT Radar competition prototype · India · 4 brands · controlled/sandboxed data · no live HUL integrations")
