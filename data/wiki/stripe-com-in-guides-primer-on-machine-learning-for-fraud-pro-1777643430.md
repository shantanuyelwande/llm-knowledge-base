---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-08T04:59:13.096488
raw_file_updated: 2026-05-08T04:59:13.096488
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-08T04:59:13.096488
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Prevention: A Primer

## Summary

This article provides a comprehensive technical overview of how [[machine learning]] is applied to detect online payment fraud, with particular focus on [[Stripe Radar]], a fraud prevention solution built into the Stripe payment platform. It explains fundamental ML concepts, evaluation metrics, and practical implementation strategies for businesses seeking to balance fraud detection with customer experience.

---

## Introduction

The explosive growth of e-commerce has created a corresponding surge in online payment fraud, costing businesses an estimated **$20 billion annually** worldwide. Beyond direct losses, fraud imposes substantial indirect costs through operational expenses, network fees, and customer churn. Traditional rule-based fraud prevention systems, while straightforward to implement, often generate excessive false positives that damage customer relationships and revenue.

[[Stripe Radar]] represents a modern approach to this problem, leveraging [[machine learning]] algorithms trained on hundreds of billions of dollars in annual payment transactions across the Stripe network. This guide introduces the fundamental concepts behind machine learning-based fraud detection, explains how to evaluate model performance, and describes practical strategies for optimizing fraud prevention systems.

---

## Understanding Online Credit Card Fraud

### Fraud Definition and Consequences

A payment is considered fraudulent when the cardholder has not authorized the charge. Common scenarios include:

- **Unauthorized use of stolen card numbers** not yet reported to the card issuer
- **Successful processing** of fraudulent transactions that later result in chargebacks
- **Network disputes** when cardholders question transactions with their banks

### Financial Impact of Fraud

When fraud occurs, businesses face multiple costs:

- Loss of goods or services provided
- **Chargeback fees** levied by payment networks
- **Elevated network fees** resulting from dispute ratios
- **Operational costs** from manual review and dispute fighting
- **Enrollment in chargeback monitoring programs**, which can increase costs or restrict payment acceptance

### The Limitations of Rule-Based Systems

Traditional hard-coded rules (e.g., "block all cards used abroad") often create excessive false declines, blocking legitimate transactions. Research shows that **33% of consumers will not return to a retailer after experiencing a false decline**, making this approach costly despite its simplicity.

---

## The Precision-Recall Trade-off

Understanding fraud prevention requires recognizing a fundamental trade-off between two types of errors:

### False Negatives (Missed Fraud)

**Definition:** Fraudulent transactions that the system fails to detect

**Costs:**
- Original transaction amount
- Chargeback fees
- Elevated network fees
- Operational review costs
- Risk of chargeback monitoring program enrollment

### False Positives (False Declines)

**Definition:** Legitimate customer transactions incorrectly blocked by the system

**Costs:**
- Lost gross profit on the transaction
- Reputational damage
- Customer churn (up to 33% according to industry surveys)

### Business-Dependent Optimization

The optimal balance between these errors depends on business characteristics:

- **Low-margin businesses** (e.g., food e-commerce): Fraudulent transactions are expensive relative to profit, requiring aggressive fraud prevention even if it blocks more legitimate customers
- **High-margin businesses** (e.g., SaaS): Lost revenue from blocked legitimate customers may outweigh fraud costs, favoring permissive policies

---

## Stripe Radar and the Stripe Network

### Core Advantages

[[Stripe Radar]] is a machine learning-based fraud prevention system built directly into the Stripe payment platform. Key advantages include:

#### Network Scale

Stripe processes hundreds of billions in annual payments from millions of businesses. This scale provides significant advantages:

- **Early pattern detection:** Stripe often identifies fraud signals and patterns before smaller networks
- **Card reuse data:** 90% of cards on the Stripe network have been seen multiple times, enabling richer risk assessments
- **Aggregate signals:** Transaction data across the network provides contextual information unavailable to individual merchants

#### Seamless Integration

Unlike third-party fraud solutions, Radar requires no additional engineering:

- **Automatic data collection:** Fraud-relevant signals are collected automatically through normal payment flows
- **Ground truth information:** Dispute and chargeback data flows directly from Stripe's payment processing
- **Real-time network data:** Card network and issuer information is accessed directly without manual integration
- **Zero engineering overhead:** No custom coding required to send event data or payment labels

### How the Network Improves Detection

Radar leverages network data to identify patterns such as:

- Card country of origin
- IP address geographic location
- IP address reputation (frequency of use with specific cards)
- Cross-border transaction patterns
- Merchant category patterns
- Temporal patterns in card usage

---

## The Basics of Machine Learning

### Core Concept

[[Machine learning]] refers to techniques that use large datasets to produce predictive models. In fraud detection, the goal is to predict whether a payment is fraudulent based on observable input features.

### Training Data Structure

Machine learning models are trained on historical data containing:

- **Features:** Input variables that may predict fraud (e.g., transaction amount, card country, IP address)
- **Labels:** Ground truth outcomes (fraudulent or legitimate)
- **Feature vectors:** Collections of features for each transaction

Example training data:

| Amount (USD) | Card Country | Countries Used (24h) | Fraud? |
|---|---|---|---|
| $10 | US | 1 | No |
| $10 | CA | 2 | No |
| $30 | US | 1 | Yes |
| $99 | CA | 1 | Yes |

### Model Output

Rather than simple binary classifications, modern fraud models assign **probability scores** indicating likelihood of fraud. For example, a model might assess a transaction as having a 65% probability of being fraudulent and 35% probability of being legitimate.

### Example: Decision Trees

A simplified model might be represented as a decision tree:

```
Is amount > $25?
├─ Yes: Is card country = US?
│   ├─ Yes: 70% fraud probability
│   └─ No: 30% fraud probability
└─ No: 10% fraud probability
```

The model answers: "Of transactions similar to this one in our historical data, what fraction were actually fraudulent?"

### Modern Approaches

While traditional methods (linear regression, decision trees, random forests) work well for many applications, [[Stripe Radar]] employs more sophisticated techniques:

- **[[Neural networks]] and [[deep learning]]:** Brain-inspired architectures capable of learning complex patterns
- **[[Large-scale machine learning]]:** Practical advantages emerge only with massive datasets; Stripe's network scale enables cutting-edge approaches
- **Performance improvements:** Stripe's updated models have improved fraud detection by over 20% year-over-year

---

## Feature Engineering

### Overview

[[Feature engineering]] is one of the most involved aspects of industrial machine learning, consisting of two parts:

1. **Formulation:** Creating features with predictive value based on domain expertise
2. **Implementation:** Making feature values available for both training and real-time production scoring

### Feature Discovery Process

Data scientists develop features through:

- **Domain expertise:** Understanding fraud patterns from extensive case analysis
- **Empirical testing:** Examining thousands of fraud cases to identify useful patterns
- **Intuition refinement:** Features may seem non-obvious (e.g., time zone differences, multi-country authorization counts)

### Example Feature: IP Address Reputation

A useful feature might capture whether a payment originates from an IP address commonly associated with a specific card:

- **Low-risk:** IP addresses seen before (home, workplace)
- **High-risk:** IP addresses from different states or countries

### Production Implementation Challenges

Making features available in production requires substantial infrastructure:

- **Historical computation:** Computing feature values for all historical transactions
- **Distributed processing:** Using tools like [[Hadoop]] for large-scale computation
- **Optimization:** Implementing space-saving data structures for complex features
- **Real-time updates:** Maintaining current feature values during payment processing

### Categorical Features and Embeddings

[[Categorical features]] (e.g., merchant, country, bank) present unique challenges due to their high cardinality. Stripe uses **[[embeddings]]** to represent these features:

#### What Are Embeddings?

Embeddings represent categorical values as coordinates in multi-dimensional space, capturing similarity relationships:

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

**Key properties:**
- Similar entities (Uber, Lyft) have similar embeddings
- Similarity is measured by [[cosine distance]]
- Models can transfer learning between similar entities
- Fraud patterns can generalize across geographies

#### Benefits

- **Transfer