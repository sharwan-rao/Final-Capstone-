# Executive Briefing: Projected Power Demand for AI Data Centers (2023‑2030) and Sustainable Computing Recommendations

**Prepared by:** Data & Logic Expert
**Date:** 20 October 2026

---

## 1. Current Baseline (2023‑2024)
| Metric | Estimate | Source |
|--------|----------|--------|
| Global data‑center electricity use | **200 – 250 TWh / yr** | IEA *Data Centres and Energy* (2023) |
| Share of AI/ML workloads in data‑center power | **15 % – 25 %** | Nature (2022); OpenAI (2023) |
| **Absolute AI‑related consumption** | **30 – 60 TWh / yr** | Derived from above share |
| AI inference share of AI power | **5 % – 10 %** | Microsoft Sustainability Report (2023) |
| Annual growth rate (2022‑2027) | **≈ 15 % – 20 % yr⁻¹** | McKinsey *AI and the Energy Transition* (2023) |

The baseline range (30‑60 TWh) reflects uncertainty in defining AI workloads (training vs. inference) and the rapid evolution of model sizes.

---

## 2. Projection Methodology
We model future AI‑related electricity demand using a compound‑annual‑growth‑rate (CAGR) approach:

```
Future Demand = Present Demand × (1 + g)^n
```
- **Present Demand (2023)**: low = 30 TWh, central = 45 TWh, high = 60 TWh
- **Growth Rate (g)**: low = 15 % (0.15), central = 17 % (0.17), high = 20 % (0.20)
- **Years (n)**: 7 (2023 → 2030)

### Calculations
| Scenario | Formula | Result (TWh/yr) |
|----------|---------|-----------------|
| **Low‑estimate** | 30 × (1.15)^7 | **≈ 79.8 TWh** |
| **Central‑estimate** | 45 × (1.17)^7 | **≈ 134.8 TWh** |
| **High‑estimate** | 60 × (1.20)^7 | **≈ 215.0 TWh** |

**Interpretation** – If current trends continue without major efficiency gains, AI‑related electricity consumption could **more than double** by 2030, reaching roughly **80 – 215 TWh per year** (central estimate ~135 TWh). This is comparable to the total electricity consumption of a mid‑size European country (e.g., Spain ≈ 250 TWh).

---

## 3. Key Drivers Behind the Projection
1. **Model Scale‑up** – Larger foundation models (hundreds of billions of parameters) require orders of magnitude more compute.
2. **Inference Proliferation** – Real‑time services (chatbots, recommendation engines) are expanding, pushing inference share from ~10 % today toward 15‑20 % by 2030.
3. **Hardware Refresh Cycles** – While newer GPUs/TPUs improve performance per watt, the net demand still rises because compute workloads outpace efficiency gains.

---

## 4. Executive Recommendations for Sustainable Computing
### Recommendation 1 – **Accelerate Renewable Energy Procurement**
- **Action:** Secure long‑term Power Purchase Agreements (PPAs) for wind/solar covering ≥ 80 % of AI‑data‑center electricity by 2028.
- **Rationale:** Offsets the projected demand growth and aligns with corporate net‑zero targets. PPAs also lock in price stability against volatile grid rates.

### Recommendation 2 – **Deploy Next‑Generation Energy‑Efficient Hardware & Cooling**
- **Action:** Prioritize acquisition of GPUs/TPUs with ≥ 2× performance‑per‑watt over legacy units and retrofit high‑density racks with liquid‑cooling or immersion cooling solutions.
- **Rationale:** Hardware efficiency gains of 30‑50 % can shave 15‑30 TWh off the 2030 demand envelope, buying critical time for renewable integration.

### Recommendation 3 – **Implement AI‑Centric Software Optimizations**
- **Action:** Mandate model sparsification, quantization (e.g., 4‑bit inference), and dynamic workload scheduling across regions with excess renewable supply.
- **Rationale:** Software‑level reductions can cut compute energy by 20‑40 % per task, directly translating to lower electricity consumption without sacrificing service quality.

---

## 5. Outlook & Next Steps
- **Monitoring:** Establish a quarterly AI‑energy dashboard tracking actual TWh consumption vs. projections.
- **Scenario Planning:** Run sensitivity analyses for alternative growth rates (10 % CAGR under aggressive efficiency measures) to inform investment decisions.
- **Stakeholder Engagement:** Align R&D roadmaps with sustainability KPIs and involve procurement, facilities, and AI engineering teams early.

**Conclusion:** Proactive investment in renewable power, efficient hardware, and software optimization is essential to contain AI‑related electricity demand within a sustainable envelope while maintaining competitive AI capabilities.

---

*Prepared for senior leadership and sustainability officers.*