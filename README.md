# Oct-2026-Claude-Community-Bhopal
October 2026 Hackathon Claude Community Bhopal

# Backend prompt 
Build the backend for “Jal Drishti,” an interactive dashboard that helps a Bhopal Municipal Corporation officer identify which idol-immersion ghats need attention before Durga visarjan.

Start by reading `PROBLEM-STATEMENT.md`, `data/DATA_DICTIONARY.md`, and the existing project files. Follow any `AGENTS.md` instructions. Inspect the current stack and integrate with it where practical. Avoid replacing working parts of the project without a clear reason.

## Backend goals

Provide reliable, documented endpoints that let the dashboard:
1. Retrieve Bhopal ghat readings and filter them by year, festival, phase, ghat, and parameter.
2. Compare readings with relevant CPCB water-quality criteria.
3. Show an explainable ghat risk ranking with the evidence behind each rank.
4. Report missing-data coverage clearly.
5. Generate a concise officer brief in Hindi and English from the available data.

Use `data/bhopal_ghats_2023_2025.csv` as the primary dataset and `data/cpcb_water_quality_criteria.csv` for criteria. Keep the CSVs as the source of truth unless the existing architecture calls for a small local database.

## Suggested API

Adapt endpoint names to the repository’s conventions, but provide equivalent functionality:

- `GET /api/health` — service status.
- `GET /api/ghats` — list ghats and available metadata.
- `GET /api/readings` — readings, with optional filters: `year`, `festival`, `phase`, `site`, and `parameter`.
- `GET /api/criteria` — applicable CPCB criteria and their source/class.
- `GET /api/summary` — overview counts and criterion comparisons for the selected filters.
- `GET /api/rankings` — ghats ranked by an explainable method, including reasons, criterion comparisons, sample counts, and missing-data counts.
- `GET /api/ghats/{site}/readings` — detailed readings and coverage for one ghat.
- `GET /api/brief` — short Hindi and English officer briefs, optionally based on the selected year, festival, and phase.

Use consistent JSON response shapes. Validate query parameters, return helpful 4xx errors for invalid filters, and use appropriate HTTP status codes. Include pagination only if it is useful for the dataset and dashboard.

## Interpretation rules

Use CPCB Class B (organised outdoor bathing) where criteria apply:
- Dissolved oxygen: at least 5 mg/L.
- BOD: at most 3 mg/L.
- pH: 6.5–8.5.

For BOD:
- A value at or below 3 mg/L meets the Class B BOD criterion.
- A value above 3 mg/L exceeds that criterion. Higher BOD indicates greater oxygen demand from organic matter.
- Do not call water “clean” or “safe” based on BOD alone. Report “meets” or “exceeds the selected criterion.”
- Apply equivalent direction-aware comparisons for dissolved oxygen and pH.

Make the ranking deterministic and explainable. For example, rank using the number and severity of observed criterion exceedances, while showing the readings that support the score. Document the exact scoring method in the README or API documentation. Do not treat missing readings as passing or failing, and disclose sample counts and coverage so ghats with sparse data are not misleadingly presented as low risk.

## Data integrity

- A blank or `not sampled` value is missing, never clean.
- BDL and ND mean below detection; do not convert them to zero.
- Preserve the original printed value, assumed unit, and source page.
- Units are assumed because the reports omit them.
- Coverage varies across site, year, festival, and phase.
- The “Rani Kamlapati ghat / Kamla Park kund” site mapping has medium confidence and may refer to two locations; expose that caveat in API responses.
- Only chromium, lead, zinc, and copper were tested among metals.
- Do not claim health effects or make unsupported safety recommendations.
- Do not invent data, limits, locations, or source references.

## Engineering requirements

- Keep the backend local and self-contained; do not connect to or write to live government systems.
- Add sensible separation between data loading, validation, criteria comparison, ranking, and HTTP routes.
- Handle malformed or missing input files gracefully with useful errors.
- Add tests for filtering, criterion comparisons (including BOD direction), missing values, BDL/ND handling, ranking determinism, and API error cases, following the repository’s existing test setup.
- Add API documentation with example requests and responses.
- Update README with setup/run instructions, endpoints, ranking method, and known limitations.
- Do not include API keys, secrets, or personal data.

First inspect the repository and report the backend stack and implementation approach briefly, then build it. When finished, summarize the endpoints, how to run the backend, and the tests or checks actually run.
