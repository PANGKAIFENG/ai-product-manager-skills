# Planning Rubric

This rubric produces a discussion draft, not a delivery promise. Use evidence first and avoid false numeric precision.

## 1. Evidence levels

| Level | Evidence | Allowed conclusion |
| --- | --- | --- |
| Confirmed | Exported field, requirement detail, user clarification, explicit commitment | State as fact. |
| Supported inference | Clear title plus consistent neighboring requirements or dependency evidence | Use for a provisional recommendation and name the assumption. |
| Weak inference | Ambiguous title with little supporting context | Classify tentatively, keep confidence low, and list the smallest missing fact. |

Never infer a named customer commitment, deadline, revenue, user count, compliance obligation, or finished technical design from a title alone.

## 2. Theme clustering

Create themes dynamically. Useful theme shapes include:

- end-user interaction and experience;
- document/file understanding and output;
- Skill, tool, connector, automation, or marketplace capability;
- memory, retrieval, model, runtime, storage, reliability, or other platform foundations;
- business Agent or domain workflow;
- enterprise governance, audit, permissions, versioning, or risk control;
- desktop performance and operational stability.

Themes are not a fixed taxonomy. A requirement may have one primary theme and one dependency theme. Avoid a miscellaneous bucket larger than a meaningful theme; split it or state that titles are too vague.

## 3. Duplicate and dependency judgment

Label candidates rather than mutating data:

- `duplicate-candidate`: likely same outcome and same user flow;
- `overlap`: shared capability but different acceptance boundary;
- `dependency`: B cannot deliver its expected outcome before A exists;
- `shared-foundation`: one capability enables three or more downstream items;
- `sequence-only`: parallel implementation is possible, but validation or rollout should be ordered;
- `needs-clarification`: title does not reveal enough to distinguish the above.

State the evidence and the consequence of being wrong.

## 4. Priority labels

Keep the team's operational labels: `紧急`、`高`、`中`、`低`.

### 紧急

Use only for a verified hard constraint: production/security incident, legal or compliance deadline, contractual customer commitment, or fixed leadership milestone whose miss has immediate material impact. An urgent label requires evidence; do not infer it from emphatic wording.

### 高

Use for a top-stage outcome, key customer value, shared foundation that unblocks multiple committed items, or high-impact reliability issue. It should enter an early feasible iteration, subject to dependency order.

### 中

Use for meaningful product improvement with no verified immediate hard constraint, or an item whose value is real but localized.

### 低

Use for optional polish, exploratory ideas without a current decision target, redundant work pending merge, or work whose value remains too unclear to displace better-evidenced items. Low confidence alone does not force low priority; it can instead justify an early validation task.

## 5. Iteration placement

Apply in this order:

1. Place verified deadlines and incidents in the earliest feasible iteration.
2. Place shared foundations before their downstream consumers.
3. Keep a coherent iteration goal; avoid distributing tightly coupled pieces across distant weeks without reason.
4. For high-value high-difficulty work, split discovery/technical validation from delivery when possible.
5. Consider owner concentration and obvious work-in-progress overload. Without estimates or capacity data, call this a load signal, not a capacity proof.
6. Leave room for integration and validation; do not fill every week as if titles were estimates.

For `YY.M.W`, interpret `W` as the team's week number within that month unless the user supplies a different calendar.

## 6. Technical difficulty

Technical difficulty affects risk, lead time, sequencing and whether to split work. It must not be used as a proxy for business value. Explicitly call out:

- unknown integration or third-party dependency;
- foundation changes with broad blast radius;
- data migration/storage/security risk;
- cross-team or owner dependency;
- validation cost or unclear acceptance criteria.

## 7. Sparse-data behavior

When only titles and basic fields exist:

- complete the theme map;
- give a provisional priority and iteration when a reasonable inference exists;
- use low or medium confidence honestly;
- list one smallest missing fact for the highest-impact uncertain items;
- ask at most 1-3 batch-level questions;
- do not stop the whole analysis or require a bulk intake form.

## 8. Recommendation test

Before finalizing each changed item, answer:

- What evidence supports moving it?
- Which dependency or outcome improves?
- What is the consequence if the inference is wrong?
- What single missing fact would most change the recommendation?
- Is the recommendation a priority judgment, a sequencing judgment, or both?
