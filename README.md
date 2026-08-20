# NEXT Radar — Project NEXT prototype

This package contains two runnable versions of the frozen NEXT Radar prototype:

1. **`index.html`** — zero-install interactive browser prototype. Open it directly in Chrome/Edge/Safari.
2. **`app.py`** — Streamlit implementation intended for public deployment later.

## Fastest way to review
Open `index.html` directly. It contains the four frozen primary screens:

1. Radar Home
2. Opportunity Dossier
3. Ask Radar
4. Decision & Strategist Handoff

The hero replay is **Axe × Brat Summer as of 09 Jul 2024** with the frozen score:

- Brand Relevance 80
- Momentum 95
- Novelty 91
- Commercial Signal 60
- Actionability 84
- Risk 25
- ROS 84.30
- Risk penalty 6.25
- OPS 78.05 / 78.1 — High Priority

The app also includes Rexona × stoppage-time moment, Dove × Barbie discourse, Knorr × Girl Dinner, and background/noise events.

## Streamlit run instructions

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Data / governance rules represented

- Historical replay / point-in-time cutoff to prevent hindsight leakage.
- Event clustering rather than one alert per post/article.
- Portfolio-first brand routing across Axe, Dove, Rexona and Knorr.
- Deterministic OPS formula with separate risk penalty.
- Evidence labels: PUBLIC FACT / CONTROLLED DEMO INPUT / SYNTHETIC INTERNAL / AI-DERIVED.
- Ask Radar is grounded in the dossier and Brand Memory and cannot overwrite deterministic scores.
- Weight changes are simulations unless centrally approved and versioned.
- Human Brand Manager owns Approve / Watch / Reject / Escalate.
- Approve creates a structured NEXT Strategist handoff, not a campaign execution.

## Prototype boundary

This is a competition PoC using controlled/sandboxed data. It does not claim live HUL system integrations or production readiness.
