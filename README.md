# xForCloBot – Multi-Criteria Decision Modeling for Legal Intake Evaluation

**xForCloBot** is a legal AI prototype that applies **Multi-Criteria Decision Modeling (MCDM)** to evaluate the **viability of wrongful foreclosure cases**. It simulates the logic a junior associate or intake attorney would use — combining **structured legal signals**, **weighted decision criteria**, and **LLM-ready prompt chains** to triage incoming cases.

This tool is designed to help **State of Georgia Plaintiff Attorneys** make early, informed decisions about whether to pursue a case — based on **judicially grounded logic**, not guesswork.

---

## 🧠 Methodology

The system implements MCDM/AHP  adapted for legal case intake workflows:

1. **Attribute Definition**  
   Each decision point (e.g., "Was notice provided?") is treated as an independent legal signal. 

2. **Weighted Scoring**  
   Every attribute (legal signal) is assigned a score and weight based on legal relevance (e.g., notice failure is weighted more heavily than payment lapse).

3. **Aggregation**  
   The tool calculates a final viability score by combining weighted attributes into a normalized outcome (high, medium, low merit).

4. **Interpretability Layer**  
   Outputs are used to build few-shot prompt examples for legal LLMs like GPT-4, Claude, or domain-specific custom agents. 

---

## 🔍 Features

- ⚖️ 90+ legal criteria based on real wrongful foreclosure case law
- 🧾 Structured intake modeled after real-world paralegal workflows
- 🔎 Benchmarked against appellate court decisions (ground truth)
- 🧠 Few-shot prompting templates for legal LLM testing
- 🧮 Prototype surrogate model for automated legal triage

---

## 📂 Project Layout

- `data/` → CSV-based structured intake forms and weights
- `court_cases/` → Summaries of real court cases used for model alignmen(ground truth)t
- `prompts/` → Prompt scaffolds and few-shot examples
- `notebooks/` → Evaluation scripts and surrogate model prototypes

---

## 👤 Author

**Pradeep Kumar**  
Legal AI Researcher | Legal Workflow Designer | Law Prompt Engineer  


---

