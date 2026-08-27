# Verification Retrofit — founding pilot

Fix My Tests is read-only diagnosis. Verification Retrofit is the bounded implementation job that follows when the diagnosis is right and the remaining burden is rebuilding evidence.

## Job

> Take a completed Fix My Tests verification map and implement the 1–3 risk rows that control the next release or trust decision.

## Deliverables

```text
risk → claim → failure mechanism → method → drive → oracle → receipt → cadence
```

For the selected rows, the pilot may include:

- production/test changes at the required seam;
- property, fuzz, fault-injection, concurrency, live-contract, or statistical evidence when that mechanism requires it;
- hermetic runner or environment repair;
- revision-bound execution receipts;
- merge, release, nightly, manual, or live binding where cadence matters;
- removal or downgrade of displaced evidence only when unique coverage loss is established as none;
- a closeout listing implemented, still uncovered, deferred, and unavailable evidence.

## Acceptance

Each selected risk row must have a named positive claim, a method capable of exposing its failure mechanism, an authoritative oracle, current revision-bound execution, and a demonstrated red path or qualified negative control where falsifiability is not otherwise structural.

## Not included

- repository-wide safety certification;
- generic CI modernization;
- permanent PR adjudication;
- test-count or coverage targets;
- invented defect-rate, time-savings, or ROI claims;
- a requirement to adopt Moat, Arq, or any other product.

## Founding commercial test

The current hypothesis is one fixed engagement in the **$5k–10k** calibration band for a mature consequential repository. Scope and price are quoted against the selected risk rows and acceptance receipts, not hours or promised savings. This is a demand experiment, not validated pricing.

To discuss a pilot, open an issue titled `Verification Retrofit inquiry` with a Fix My Tests report or the repository question that should produce one. Do not post private source, secrets, or vulnerability details in a public issue.
