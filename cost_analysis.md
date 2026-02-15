# Cost Analysis: Course Companion FTE

**Current Phase:** Phase 3 (Full Web App + Hybrid Intelligence)
**User Scale Estimate:** 10,000 Active Users

## 1. Zero-Backend-LLM Components (Deterministic)

These costs are fixed or scale linearly with traffic, independent of AI usage.

| Component | Service | Cost Model | Monthly Est. (10k Users) |
| :--- | :--- | :--- | :--- |
| **Content Storage** | Cloudflare R2 | $0.015/GB + $0.36/M reads | ~$5.00 |
| **Database** | Neon (Serverless Postgres) | Compute hours + Storage | ~$25.00 |
| **Backend Hosting** | Fly.io / Railway | RAM + CPU usage | ~$20.00 |
| **Frontend Hosting** | Vercel / Netlify | Bandwidth | ~$20.00 |
| **Domain & SSL** | Namecheap / Cloudflare | Fixed yearly | ~$1.00 |
| **Total Standard Ops** | | | **~$71.00** |

**Cost per User (Ops): $0.007**

---

## 2. Hybrid Intelligence Options (AI Features)

These features use the **Gemini 2.0 Flash** API (via OpenAI compatibility layer).

*Model Cost Basis (Gemini 2.0 Flash):*
*   Input: $0.00 / 1M tokens (Free Tier for Hackathon) / ~$0.10 / 1M (Paid)
*   Output: $0.00 / 1M tokens (Free Tier for Hackathon) / ~$0.30 / 1M (Paid)

| Feature | Est. Tokens / Interaction | Interactions / User / Mo | Cost / User / Mo (Paid Rate) |
| :--- | :--- | :--- | :--- |
| **Concept Explainer** | 500 (in) + 300 (out) | 5 | $0.001 |
| **Socratic Tutor** | 800 (in) + 200 (out) | 2 | $0.0005 |
| **Quiz Master** | 400 (in) + 100 (out) | 5 | $0.0005 |
| **Progress Motivator** | 200 (in) + 100 (out) | 2 | $0.0002 |
| **Total AI Cost** | | | **~$0.0022** |

## 3. Total Projected Cost

| Scenario | Monthly Cost (10k Users) | Cost per User |
| :--- | :--- | :--- |
| **Infrastructure Only** | $71.00 | $0.007 |
| **Infra + AI (Paid Rates)** | $71.00 + $22.00 = $93.00 | ~$0.009 |

**Efficiency Verdict:**
The "Zero-Backend-Default" architecture keeps the baseline cost extremely low ($0.007/user). Even with active AI tutoring (Phase 2/3 Hybrid), the cost per user remains under $0.01/month, meeting the "99% cost reduction" goal compared to human tutoring ($200+/month).
