# Project Execution Rules

## Investment Analysis Is Resource-First

For any stock, fund, holding, market, sector, add/reduce position, rebound, drawdown, or portfolio question in this project, do not answer from memory first.

Before giving a conclusion or action:

1. Read `data/holdings.json` if the question involves the user's positions, portfolio exposure, or position sizing.
2. Read every Markdown file under `resource/`, including nested folders.
3. Read `resource/links.md`; open relevant links when current market/news context is needed.
4. Apply the user's local rules before giving the final answer.
5. State which local files and external sources were used.
6. Keep wording as auxiliary decision support, not as a promise of return or a guarantee.

## Risk First, Trend Second

When analyzing a held stock, fund, sector, or theme:

1. Evaluate position concentration, correlated exposure, and recent drawdown before judging whether the market is "over" or "only a pullback".
2. If a high-volatility theme or highly correlated group is a large part of the portfolio, do not wait for confirmed trend failure before discussing risk reduction.
3. If a theme falls sharply from a recent high, provide defensive actions as well as trend interpretation.
4. Do not use "still above the 20-day moving average" as the only reason to avoid reducing risk.
5. Always give explicit triggers for three cases: hold, reduce, and add.

## High-Volatility Theme Rule

For semiconductor, AI, technology, robotics, new energy, or other crowded growth themes:

1. If related holdings exceed roughly 20% of identifiable portfolio value and the theme drops sharply from a recent high, recommend at least considering partial risk reduction.
2. If the theme drops more than 10% from a recent high, explain whether partial reduction is appropriate even if the trend is not confirmed broken.
3. If the theme drops more than 15% from a recent high, switch from an optimistic pullback frame to a defensive risk-control frame unless there is strong recovery evidence.
4. Prefer phased actions over all-or-nothing advice.
