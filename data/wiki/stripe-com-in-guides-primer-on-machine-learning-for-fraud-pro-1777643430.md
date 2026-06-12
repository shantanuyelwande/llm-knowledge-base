---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-12T06:46:51.658422
raw_file_updated: 2026-06-12T06:46:51.658422
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-12T06:46:51.658422
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Prevention

## Summary

This article provides a comprehensive technical guide to understanding how [[machine learning]] is applied to [[online payment fraud]] detection, with particular focus on [[Stripe Radar]], a fraud prevention solution that leverages data from hundreds of billions of dollars in annual transactions. The guide covers fundamental machine learning concepts, model evaluation techniques, operational deployment strategies, and practical business considerations for optimizing fraud prevention systems.

---

## Introduction

The rapid acceleration of e-commerce has led to a corresponding surge in [[online fraud]], with businesses losing an estimated $20 billion annually to fraudulent transactions. Beyond direct losses, each dollar lost to fraud generates additional costs through operational expenses, network fees, and customer churn. 

[[Stripe Radar]] represents a modern approach to fraud prevention, utilizing [[adaptive machine learning]] algorithms that leverage patterns from the Stripe network—processing hundreds of billions of dollars in payments annually—to detect fraud with greater accuracy while minimizing false positives that block legitimate customers.

This guide introduces the technical foundations of machine learning in fraud detection, explains how models are evaluated and deployed, and discusses the trade-offs businesses must navigate between preventing fraud losses and avoiding customer friction.

---

## Understanding Online Credit Card Fraud

### Definition and Chargebacks

A payment is considered fraudulent when the [[cardholder]] does not authorize the charge. Common fraud scenarios include:

- Use of stolen card numbers not yet reported to the card issuer
- Successful processing of unauthorized transactions
- Subsequent [[chargeback]] (dispute) filed when the cardholder discovers fraudulent activity

### Business Impact of Fraud vs. False Declines

Businesses face two competing risks when implementing fraud prevention systems:

**False Negatives (Missed Fraud)**
- Original transaction amount loss
- [[Chargeback]] fees charged by payment networks
- Elevated [[network fees]] due to dispute ratios
- Increased operational costs for dispute resolution
- Risk of enrollment in [[chargeback monitoring programs]], potentially leading to higher costs or loss of payment processing privileges

**False Positives (False Declines)**
- Revenue loss from blocked legitimate transactions
- Reputational damage to the business
- Customer attrition: Research indicates 33% of consumers will not return to a business after experiencing a false decline

### The Precision-Recall Trade-off

Fraud prevention systems must balance these competing objectives. The fundamental trade-off is:
- **Stricter blocking policies** → fewer false negatives but more false positives
- **Lenient blocking policies** → fewer false positives but more false negatives

Business margins significantly influence optimal strategy. Low-margin businesses (e.g., online food sales) benefit from aggressive fraud blocking, as the cost of one fraudulent transaction may require hundreds of legitimate sales to offset. High-margin businesses (e.g., SaaS) may tolerate more fraud to avoid blocking high-value legitimate customers.

---

## Stripe Radar and the Stripe Network

### Overview

[[Stripe Radar]] is an integrated fraud prevention solution built directly into the Stripe platform. It uses [[adaptive machine learning]] to evaluate every transaction for fraud risk and take appropriate action, with high-risk payments automatically blocked and additional tools available through [[Radar for Fraud Teams]] for custom policy configuration.

### Network Advantages

Stripe's scale provides significant fraud detection advantages:

- **Early signal detection**: Processing hundreds of billions in payments annually across millions of businesses allows Stripe to identify fraud patterns before smaller networks
- **Rich historical data**: 90% of cards used on the Stripe network have been seen multiple times, providing substantial data for risk assessment
- **Automatic data collection**: Fraud-relevant signals (card issuance country, IP address, transaction patterns) are collected automatically through the payment flow
- **Network intelligence**: Direct access to timely, accurate data from card networks and issuers

### Integration Benefits

Unlike traditional fraud solutions, Radar requires minimal implementation effort:

- No engineering integration required for data transmission
- Automatic receipt of "ground truth" information from the standard Stripe payment flow
- No manual payment labeling required
- Real-time fraud scoring without additional infrastructure investment

---

## The Basics of Machine Learning

### Overview

[[Machine learning]] refers to techniques for processing large datasets to produce predictive models—in the fraud context, models that predict the likelihood a charge will result in a fraud dispute.

### Core Concept: Prediction

Machine learning models predict output values based on input values:

- **Output variable**: Boolean indicating whether a payment is fraudulent (true/false)
- **Input variables (features)**: Properties such as card issuance country, number of distinct countries where card was used in past 24 hours, transaction amount, etc.

Models learn patterns from historical data containing both inputs and outputs, then apply these patterns to new transactions.

### Training Data Example

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10.00 | US | 1 | No |
| $10.00 | CA | 2 | No |
| $10.00 | CA | 1 | No |
| $10.00 | US | 1 | Yes |
| $30.00 | US | 1 | Yes |
| $99.00 | CA | 1 | Yes |

### Model Types

**Decision Trees** (simple, interpretable)
- Traverse tree structure by answering sequential questions
- Leaf nodes contain probability estimates based on historical samples
- Easy to visualize but limited in complexity

**Advanced Models**
- [[Linear regression]], [[random forests]], and [[neural networks]]
- [[Deep learning]] approaches can capture complex patterns
- Require substantial training data to realize full potential
- Stripe leverages neural networks and deep learning, achieving 20%+ year-over-year performance improvements

### Real-World Example

A simplified decision tree for fraud detection might ask:
1. Is the card amount > $50?
2. Is the card being used from a new country?
3. Is the transaction amount unusual for this card?

Each path through the tree leads to a leaf containing fraud probability estimates based on similar historical transactions.

---

## Feature Engineering

### Definition

[[Feature engineering]] is the process of:
1. Formulating features with predictive value based on domain expertise
2. Engineering systems to compute feature values for both model training and production use

### Handcrafted Features

Data scientists develop features through:
- Analysis of thousands of fraud cases
- Intuitive domain knowledge
- Empirical testing of predictive value

Examples of effective fraud features:
- Whether payment originates from a common IP address for that card
- Time zone difference between user device and UTC
- Count of countries where card was successfully authorized
- Payment amount relative to historical patterns

### Implementation Challenges

Computing feature values at scale requires:
- Distributed computing infrastructure (e.g., [[Hadoop]])
- Optimization using probabilistic data structures
- Real-time computation for production scoring
- Dedicated infrastructure and established workflows

### Learned Embeddings

Rather than manually defining all features, machine learning models can learn [[embeddings]]—vector representations of categorical features that capture similarity relationships.

**Example: Merchant Embeddings**

| Merchant | Dimension 1 | Dimension 2 | Dimension 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

Similar merchants (Uber/Lyft) have similar embeddings, allowing models to:
- Transfer learning between similar merchants
- Identify patterns in new merchants based on similarity
- Adapt to geographic variations without explicit retraining

### Advantages of Embeddings

- Capture complex relationships without manual definition
- Enable automatic pattern recognition across similar entities
- Facilitate geographic generalization (e.g., Brazil fraud patterns → US patterns)
- Common in modern ML applications ([[Word2Vec]], [[BERT]], [[GPT-3]])

---

## Evaluating Machine Learning Models

### Key Evaluation Metrics

#### Precision

**Definition**: Fraction of flagged transactions that are actually fraudulent

**Formula**: True Positives / (True Positives + False Positives)

**Example**: If 6 transactions are flagged and 4 are actually fraudulent, precision = 4/6 = 0.66 (66%)

**Interpretation**: Higher precision means fewer false positives (fewer legitimate customers blocked)

#### Recall (Sensitivity, True Positive Rate)

**Definition**: Fraction of all fraudulent transactions that are caught by the policy

**Formula**: True Positives / (True Positives + False Negatives)

**Example**: If 5 transactions are actually fraudulent and 4 are flagged, recall = 4/5 = 0.80 (80%)

**Interpretation**: Higher recall means fewer false negatives (fewer fraud incidents missed)

#### False Positive