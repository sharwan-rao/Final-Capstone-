# 7‑Day AI Final‑Exam Study Plan

**Target user:** Undergraduate AI student with 2–4 h/day to study.  
**Goal:** Cover core AI topics, reinforce with active‑learning methods, and finish with a final review.

---

## Day 1 – Foundations & Search

**Headline topic:** Search algorithms & problem formulation

### Sub‑topics
- State‑space representation, branching factor, depth/solution cost
- Uninformed search: BFS, DFS, Uniform‑Cost Search
- Informed search: Greedy, A* (heuristics, admissibility, consistency)

### Study Methods (≈ 2 h 45 m total)
- **Reading (45 m):** Chapter 3 of *Russell & Norvig* (search basics).
- **Video (30 m):** Intro to search (e.g., Stanford CS221 lecture).
- **Flashcards (15 m):** Key definitions & algorithm properties.
- **Summarise (15 m):** Write a one‑page comparison table of BFS/DFS/A*.
- **Active recall (30 m):** Solve 2 textbook problems tracing A* on a given graph.
- **Break (15 m).**
- **Mini‑coding (30 m):** Pseudocode implementation of A* (no language‑specific API).
- **Reflection (15 m):** Note where heuristics matter for later ML sections.

### Practice Activities
1. **Conceptual Q&A:** Explain why admissible heuristics guarantee optimality.
2. **Graph trace:** Given a 5‑node graph, manually expand nodes using A* and list the open/closed lists at each step.

### Justification
Search is the algorithmic backbone of classical AI and introduces the notion of state‑space that underpins later knowledge‑representation and reasoning topics. Mastering A* also builds intuition for heuristic‑driven approaches used in ML optimisation.

---

## Day 2 – Knowledge Representation & Logic

**Headline topic:** Representing knowledge & logical inference

### Sub‑topics
- Propositional logic (syntax, semantics, truth tables)
- First‑order logic (predicates, quantifiers, unification)
- Inference methods: resolution, forward/backward chaining

### Study Methods (≈ 3 h total)
- **Reading (45 m):** Chapter 7 of *Russell & Norvig* (logic).
- **Video (30 m):** Logic & inference basics (MIT OpenCourseWare).
- **Flashcards (15 m):** Symbols, quantifier rules.
- **Summarise (15 m):** Create a cheat‑sheet of inference rules.
- **Break (15 m).
- **Practice problems (45 m):** Convert English sentences to FOL; resolve a sample proof.
- **Mini‑coding (30 m):** Write a simple resolution engine in pseudocode.
- **Reflection (15 m):** Link logical inference to planning (next day).

### Practice Activities
1. **Translation exercise:** Encode “All students are learners and some learners are AI majors” in FOL.
2. **Resolution proof:** Prove a given set of clauses entails a target clause.

### Justification
Logical formalisms provide the precise language needed for reasoning and planning. Understanding them before moving to probabilistic reasoning ensures the student can differentiate deterministic vs. uncertain inference.

---

## Day 3 – Planning & Heuristic Search Revisited

**Headline topic:** Classical planning & heuristic search integration

### Sub‑topics
- Planning problem definition (states, actions, goal test)
- STRIPS representation & planning graphs
- Heuristic functions derived from relaxed planning problems

### Study Methods (≈ 3 h total)
- **Reading (45 m):** Section 3.3 of *Russell & Norvig* (planning).
- **Video (30 m):** Planning Graphs & Graphplan overview.
- **Flashcards (15 m):** Action schema components.
- **Break (15 m).
- **Hands‑on exercise (45 m):** Build a STRIPS model for the classic "blocks‑world".
- **Mini‑coding (30 m):** Implement a simple forward‑state‑space planner (pseudocode).
- **Reflection (15 m):** Compare planning heuristics to A* heuristics from Day 1.

### Practice Activities
1. **Modeling task:** Write the initial, goal, and action definitions for a 3‑block blocks‑world.
2. **Heuristic calculation:** Compute the relaxed‑plan heuristic for a given state.

### Justification
Planning ties together search (Day 1) and representation (Day 2). Revisiting heuristics in a planning context reinforces the earlier A* concepts while preparing the student for probabilistic planning later.

---

## Day 4 – Probabilistic Reasoning & Bayesian Networks

**Headline topic:** Reasoning under uncertainty

### Sub‑topics
- Probability basics (joint, conditional, Bayes rule)
- Bayesian networks: structure, d‑separation, inference (exact & approximate)
- Markov Decision Processes (MDP) overview (states, actions, rewards)

### Study Methods (≈ 3 h 15 m total)
- **Reading (45 m):** Chapter 13 of *Russell & Norvig* (probabilistic reasoning).
- **Video (30 m):** Intro to Bayesian networks (Khan Academy or Coursera).
- **Flashcards (15 m):** Key probability identities.
- **Break (15 m).
- **Worked example (45 m):** Perform exact inference on a small BN (e.g., medical diagnosis).
- **Mini‑coding (30 m):** Write pseudocode for variable elimination.
- **Reflection (15 m):** Note how uncertainty will appear in ML evaluation.
- **Practice quiz (15 m):** Multiple‑choice questions on d‑separation.

### Practice Activities
1. **Inference task:** Compute P(Disease|Symptom) given a provided BN.
2. **MDP sketch:** Define states, actions, and reward for a simple grid‑world.

### Justification
Uncertainty is a core pillar of modern AI, bridging symbolic methods with statistical learning. Mastery of Bayesian reasoning prepares the student for probabilistic models in machine learning (next day).

---

## Day 5 – Classical Machine Learning Foundations

**Headline topic:** Supervised learning & model evaluation

### Sub‑topics
- Linear models (perceptron, logistic regression)
- Decision trees & ensemble basics (bagging, boosting)
- Evaluation metrics: accuracy, precision, recall, ROC‑AUC, cross‑validation

### Study Methods (≈ 3 h total)
- **Reading (45 m):** Chapter 2 of *Mitchell* or relevant section in *Russell & Norvig*.
- **Video (30 m):** Supervised learning overview (Andrew Ng’s ML course).
- **Flashcards (15 m):** Loss functions & regularisation terms.
- **Break (15 m).
- **Mini‑coding (45 m):** Implement perceptron update rule in pseudocode; run a mental simulation on a tiny dataset.
- **Practice problems (30 m):** Compute confusion matrix and derived metrics for a given prediction set.
- **Reflection (15 m):** Relate overfitting to search heuristics (bias‑variance analogy).

### Practice Activities
1. **Hand‑calc:** Update perceptron weights for two training examples.
2. **Metric exercise:** Given TP, FP, FN, TN values, calculate precision, recall, F1.

### Justification
Supervised learning is the most heavily weighted part of AI finals. Introducing linear models before neural nets gives a solid foundation for understanding gradient‑based optimisation later.

---

## Day 6 – Neural Networks & Deep Learning

**Headline topic:** Deep learning fundamentals

### Sub‑topics
- Feed‑forward neural network architecture, activation functions
- Back‑propagation algorithm (derivatives, chain rule)
- Convolutional networks overview (basic intuition)

### Study Methods (≈ 3 h 30 m total)
- **Reading (45 m):** Chapter 6 of *Goodfellow, Bengio & Courville* (NN basics).
- **Video (30 m):** Back‑propagation walkthrough (3Blue1Brown).
- **Flashcards (15 m):** Activation functions, gradient‑descent variants.
- **Break (15 m).
- **Mini‑coding (60 m):** Write pseudocode for a single‑layer perceptron forward & backward pass; then extend to a 2‑layer network.
- **Conceptual exercise (30 m):** Sketch how a convolution filter slides over an image.
- **Reflection (15 m):** Compare optimisation in NN to A* heuristic search.

### Practice Activities
1. **Back‑prop step:** Compute gradients for a 2‑neuron network on a single data point.
2. **CNN intuition:** Explain why weight sharing reduces parameters.

### Justification
Neural networks represent the modern AI frontier and often appear as a distinct exam section. Placing them after classical ML ensures the student can see the evolution from linear models to deep, hierarchical representations.

---

## Day 7 – Ethics, Review, & Mock Exam

**Headline topic:** AI ethics, integration review, and timed mock

### Sub‑topics
- Ethical frameworks: fairness, accountability, transparency, privacy
- Societal impact & AI governance
- Integrated quick‑review of all prior topics

### Study Methods (≈ 3 h 45 m total)
- **Reading (30 m):** Selected sections from *AI Ethics* (e.g., Bostrom & Yudkowsky).
- **Video (20 m):** Ethics case‑study (e.g., autonomous vehicles).
- **Flashcards (10 m):** Key ethical principles.
- **Break (15 m).
- **Rapid review (60 m):** Skim each day’s cheat‑sheet; note any lingering questions.
- **Mock exam (90 m):** 5‑question timed test covering all topics (mix of MCQ, short answer, and a problem‑solving item).
- **Self‑check (20 m):** Compare answers to provided solutions; note weak areas.
- **Wrap‑up (10 m):** Set a 30‑minute pre‑exam routine for the next day.

### Practice Activities
1. **Ethics case analysis:** Write a 150‑word position on bias mitigation in facial‑recognition systems.
2. **Mock question example:** "Given a BN with nodes A→B←C, determine if A and C are independent given B."

### Justification
The final day consolidates knowledge, highlights the increasingly important ethical dimension, and provides a realistic rehearsal to build confidence and time‑management skills before the exam.

---

**How to use this plan**
- Treat each time block as a *focus session* (no multitasking).
- After each day, mark completed items; if a block exceeds the time limit, shift the overflow to the next day's break slot.
- Keep a separate flashcard deck (paper or app) and review it daily for spaced repetition.
- Use the suggested resources (textbook chapters, open‑access videos) – they are all freely available or part of typical course packs.

Good luck!
