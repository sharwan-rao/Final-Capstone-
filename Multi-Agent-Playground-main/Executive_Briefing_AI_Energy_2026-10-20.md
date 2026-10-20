# Executive Briefing – Power Demand Outlook for AI‑Focused Data Centers (2023‑2030) & Sustainable Computing Road‑Map

**Prepared for:** Senior Leadership & Sustainability Office

**Prepared by:** Research Analyst & Data & Logic Expert (synthesis)

**Date:** 20 October 2026

---

## 1. Snapshot of the Current Landscape (2023‑2024)

| Metric | Estimate | Source |
|--------|----------|--------|
| Global data‑center electricity use | **200 – 250 TWh / yr** | IEA *Data Centres and Energy* (2023) |
| Share of AI/ML workloads in data‑center power | **15 % – 25 %** | Nature (2022); OpenAI (2023) |
| **AI‑related electricity consumption** | **30 – 60 TWh / yr** | Derived from the share above |
| AI inference share of AI power | **5 % – 10 %** | Microsoft Sustainability Report (2023) |
| Annual growth rate (2022‑2027) | **≈ 15 % – 20 % yr⁻¹** | McKinsey *AI and the Energy Transition* (2023) |

*Key take‑aways*
- AI workloads already account for **≈ 15‑25 %** of total data‑center electricity – comparable to the annual power use of a medium‑size European nation.
- Training dominates (≈ 90 % of AI power), but inference is accelerating as LLM‑driven services proliferate.
- At a 15‑20 % CAGR, AI‑related demand could **more than double** by 2030.

---

## 2. Projection Methodology & Results (2023‑2030)

We apply a simple compound‑annual‑growth‑rate (CAGR) model:

```
Future Demand = Present Demand × (1 + g)^n
```
- **Present Demand (2023)**: low = 30 TWh, central = 45 TWh, high = 60 TWh
- **Growth Rate (g)**: low = 15 % (0.15), central = 17 % (0.17), high = 20 % (0.20)
- **Years (n)**: 7 (2023 → 2030)

| Scenario | Formula | 2030 Demand (TWh/yr) |
|----------|---------|----------------------|
| Low‑estimate | 30 × (1.15)^7 | **≈ 80 TWh** |
| Central‑estimate | 45 × (1.17)^7 | **≈ 135 TWh** |
| High‑estimate | 60 × (1.20)^7 | **≈ 215 TWh** |

**Interpretation** – Without efficiency interventions, AI‑related electricity could range from **80 – 215 TWh per year** by 2030 (central estimate ~135 TWh). For perspective, that is roughly the total consumption of Spain (≈ 250 TWh) or the combined output of several large nuclear plants.

---

## 3. Drivers Behind the Surge

1. **Model Scale‑up** – Foundation models are expanding from tens of billions to **hundreds of billions** of parameters, inflating compute‑hours dramatically.
2. **Inference Proliferation** – Real‑time AI services (chatbots, recommendation engines, autonomous systems) are moving from niche to ubiquitous, pushing inference from ~10 % to potentially **15‑20 %** of AI power.
3. **Hardware Refresh Cycle** – New GPUs/TPUs deliver **30‑50 %** better performance‑per‑watt, yet the sheer increase in workload volume outpaces these gains.
4. **Geographic Dispersion** – Edge deployments add modest but growing power draws in regions with limited renewable capacity.

---

## 4. Executive Recommendations – Turning the Tide

| # | Recommendation | Concrete Actions | Expected Impact |
|---|----------------|-------------------|-----------------|
| **1** | **Accelerate Renewable Energy Procurement** | • Negotiate long‑term **Power Purchase Agreements (PPAs)** for wind/solar covering **≥ 80 %** of AI‑data‑center electricity by 2028.<br>• Prioritize locations with high renewable capacity factors (e.g., Texas, Scandinavia, Australia).<br>• Embed renewable‑share targets into vendor contracts. | • Offsets up to **170 TWh** of projected demand (central scenario).<br>• Locks in price stability and supports corporate net‑zero pledges. |
| **2** | **Deploy Next‑Generation Energy‑Efficient Hardware & Advanced Cooling** | • Replace legacy GPUs with **2×‑performance‑per‑watt** successors (e.g., NVIDIA H100, Google TPU v5).<br>• Retrofit high‑density racks with **liquid‑cooling or immersion‑cooling** systems.<br>• Implement real‑time power‑capping and dynamic voltage/frequency scaling (DVFS). | • Improves data‑center PUE by **0.05‑0.1**, shaving **15‑30 TWh** off 2030 demand.<br>• Reduces OPEX via lower cooling costs. |
| **3** | **Implement AI‑Centric Software Optimizations** | • Mandate **model sparsification, pruning, and quantization** (e.g., 4‑bit inference) for all production models.<br>• Deploy **dynamic workload scheduling** that routes inference to regions with excess renewable generation.
• Adopt **knowledge‑distillation** pipelines to replace large models with lighter student models where feasible. | • Cuts compute energy per inference by **20‑40 %**, translating to **≈ 30‑50 TWh** reduction under the central forecast.<br>• Improves latency and cost efficiency. |

---

## 5. Outlook & Next Steps

- **Short‑term (12‑18 months):** Finalize PPA framework, begin pilot hardware upgrades in flagship data‑center.
- **Mid‑term (2‑3 years):** Scale software‑optimization mandates across the AI development lifecycle; integrate renewable‑aware scheduling.
- **Long‑term (by 2030):** Target **net‑zero AI‑related electricity** through a combination of renewable procurement, hardware efficiency, and software innovation.

*Prepared for senior leadership and sustainability officers.*
