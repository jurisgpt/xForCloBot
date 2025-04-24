# State of Georgia Wrongful Foreclosure Court Cases – Ground Truth Benchmarking

This folder contains structured summaries of real-world wrongful foreclosure cases that serve as **ground truth anchors** for xForCloBot's decision modeling engine.

Each `.md` file in this folder includes:
- Case title, jurisdiction, and legal category
- Summary of facts and legal findings
- Outcome and implications for wrongful foreclosure law
- Tags and linkage to structured intake criteria


## 🔍 Purpose

These case files:
- Provide **real legal precedents** for grounding MCDM criteria
- Enable **prompt scaffolding** by offering examples for few-shot learning
- Support **evaluation** of LLM-generated outputs against actual court logic

## 🧠 How They Are Used

- **Structured Intake Mapping**: Legal Signals in each case (e.g., lack of notice, improper advertisement) map to one or more of the 90+ MCDM intake criteria.
- **Few-Shot Prompt Construction**: Each case can be converted into a prompt for GPT-style models, showing correct legal reasoning steps.
- **Evaluation & Scoring**: Used as “gold standard” references to test AI-generated outcomes against known case results.

## 🧾 Example Usage

A case like `Babalola_v_HSBC_Bank.md` shows how a missed notice leads to a sustainable wrongful foreclosure claim. This aligns with MCDM features like:

- `Notice Not Sent` → weight 0.8
- `Improper Advertisement` → weight 0.6

Used in prompting:
```plaintext
User: A borrower did not receive notice of foreclosure and the sale was improperly advertised. Is this wrongful foreclosure?
LLM: Based on legal precedent (e.g., Babalola v. HSBC), this scenario supports a wrongful foreclosure claim due to notice and ad violations.
```

---
