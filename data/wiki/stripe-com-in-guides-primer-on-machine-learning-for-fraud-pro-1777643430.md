---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-11T06:53:54.135617
raw_file_updated: 2026-06-11T06:53:54.135617
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-11T06:53:54.135617
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection

## Summary

This article provides a comprehensive technical overview of how [[machine learning]] is applied to [[fraud detection]] in online payments, with specific focus on [[Stripe Radar]]. It explains the fundamental concepts of machine learning, the challenges of evaluating fraud detection models, and the practical considerations for deploying and maintaining effective fraud prevention systems. The guide covers the trade-offs between [[false positives]] and [[false negatives]], feature engineering techniques, and how businesses can optimize their fraud prevention strategies.

---

## Introduction

The rapid acceleration of e-commerce has created a corresponding surge in online payment fraud, costing businesses over $20 billion annually. Beyond direct losses, fraud incurs additional operational costs, network fees, and customer churn. [[Stripe Radar]] is a machine learning-based fraud prevention solution that leverages data from hundreds of billions of dollars in payments processed across the Stripe network to detect fraud patterns and adapt to evolving threats.

This guide introduces the technical foundations of machine learning for fraud detection, explains model evaluation methodologies, and describes how businesses can optimize their fraud prevention strategies.

---

## Online Credit Card Fraud Fundamentals

### What Constitutes Fraud

A payment is fraudulent when the cardholder has not authorized the charge. Common scenarios include:

- **Stolen card numbers**: A fraudster uses a card number that hasn't been reported as compromised
- **Chargebacks**: When a cardholder discovers unauthorized use, they file a dispute with their bank
- **Network liability**: If networks determine a card-not-present transaction was fraudulent, the merchant bears the loss plus fees

### Traditional vs. Machine Learning Approaches

**Brute-force rules** (e.g., "block all international transactions") are simple but inefficient, blocking many legitimate transactions alongside fraudulent ones.

**Machine learning** detects nuanced patterns, allowing businesses to maximize revenue while maintaining fraud protection. However, this requires understanding critical trade-offs.

### The False Positive vs. False Negative Trade-off

#### False Negatives (Missed Fraud)
When the system fails to detect fraudulent transactions, merchants face:
- Original transaction amount loss
- Chargeback fees
- Elevated network fees
- Higher operational costs from dispute resolution
- Risk of entering chargeback monitoring programs

#### False Positives (False Declines)
When legitimate customers are blocked from purchasing:
- Gross profit loss
- Reputational damage
- Customer attrition (33% of consumers abandon retailers after false declines)

**Critical insight**: There is an inverse relationship between these metrics. Preventing more fraud increases false declines, while reducing false declines allows more fraud to slip through.

### Business-Specific Optimization

The optimal balance depends on business characteristics:

- **Low-margin businesses** (e.g., food retail): Each fraudulent transaction may require 100+ legitimate sales to offset. These businesses should prioritize fraud prevention over false positives.
- **High-margin businesses** (e.g., SaaS): Lost revenue from one blocked legitimate customer may exceed fraud costs. These businesses should prioritize reducing false declines.

---

## Stripe Radar and the Stripe Network

### Advantages of Network-Scale Fraud Detection

[[Stripe Radar]] operates at unprecedented scale, processing hundreds of billions in payments from millions of businesses annually. This scale provides critical advantages:

**Signal detection**: Stripe often observes fraud patterns earlier than smaller networks due to the volume of transactions processed.

**Card history**: 90% of cards used on the Stripe network have been seen more than once, providing rich historical data for risk assessment.

**Network signals**: Aggregate data from across the network—including card issuing country, payment IP addresses, and cross-merchant patterns—improves fraud prediction accuracy.

### Integrated Architecture

Unlike standalone fraud solutions, Radar is built directly into Stripe and requires:

- **No engineering integration**: Data flows automatically through the payment process
- **Accurate ground truth**: Chargeback and dispute information comes directly from card networks and payment processors
- **Real-time operation**: Works out of the box without manual labeling or custom data pipelines

---

## The Basics of Machine Learning

### Overview

[[Machine learning]] refers to techniques for using large datasets to build models that predict outcomes. In fraud detection, the goal is to predict whether a payment is fraudulent based on input variables (features).

### Training Data Structure

Machine learning models are trained on historical data with known outcomes. A simplified example:

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10.00 | US | 1 | No |
| $10.00 | CA | 2 | No |
| $10.00 | CA | 1 | No |
| $10.00 | US | 1 | Yes |
| $30.00 | US | 1 | Yes |
| $99.00 | CA | 1 | Yes |

### Decision Trees as Models

Machine learning algorithms learn decision rules from training data. A simplified decision tree might ask:

1. Is the amount > $25?
2. Is the card country = US?
3. How many countries was the card used in?

The model traverses these questions for new transactions and outputs a probability of fraud based on similar historical cases.

**Key principle**: The model answers "Of transactions with properties similar to this one, what fraction was fraudulent?"

### Modern Approaches

While [[decision trees]] are intuitive, modern fraud detection uses sophisticated techniques:

- **[[Neural networks]] and [[deep learning]]**: Inspired by brain architecture, these approaches require massive datasets to realize advantages. Stripe's network scale enables effective deep learning deployment.
- **Performance gains**: Stripe's updated models have improved fraud detection by over 20% year-over-year

---

## Feature Engineering

### What is Feature Engineering?

[[Feature engineering]] is the process of:

1. **Formulation**: Creating features with predictive value based on domain expertise
2. **Implementation**: Making feature values available for both training and real-time production use

### Feature Examples

Data scientists develop features through extensive fraud analysis. Examples include:

- **IP address familiarity**: Whether payment originates from known IP addresses for the card
- **Geographic velocity**: Whether the card is being used across multiple countries in short timeframes
- **Time zone anomalies**: Difference between device time and UTC
- **Authorization history**: Count of countries where the card was successfully used

### Implementation Challenges

Even simple features require substantial infrastructure:

- Computing historical values across billions of transactions
- Maintaining up-to-date feature values in production systems
- Optimizing for latency (features must be computed in real-time as payments flow)

### Embeddings for Categorical Features

[[Embeddings]] are learned representations of categorical values (merchants, banks, countries) as multi-dimensional coordinates. Key advantages:

**Similarity capture**: Similar entities have similar embeddings. Uber and Lyft embeddings are closer than either to Slack.

**Fraud pattern transfer**: If a fraud pattern is identified in Brazil, the system can recognize it in the US without retraining.

**Scalability**: Embeddings handle high-cardinality categorical features (thousands of unique merchants) efficiently.

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

---

## Evaluating Machine Learning Models

### Key Metrics

Understanding model performance requires precise definitions:

#### Precision
**Definition**: Fraction of blocked transactions that are actually fraudulent

**Formula**: True Positives / (True Positives + False Positives)

**Example**: If 6 transactions are blocked and 4 are actually fraudulent, precision = 4/6 = 0.66

**Interpretation**: Higher precision means fewer false positives

#### Recall (Sensitivity / True Positive Rate)
**Definition**: Fraction of all fraudulent transactions that are caught

**Formula**: True Positives / (True Positives + False Negatives)

**Example**: If 5 transactions are actually fraudulent and 4 are caught, recall = 4/5 = 0.80

**Interpretation**: Higher recall means fewer false negatives

#### False Positive Rate
**Definition**: Fraction of legitimate payments incorrectly blocked

**Formula**: False Positives / (False Positives + True Negatives)

**Example**: If 5 transactions are legitimate and 2 are incorrectly blocked, FPR = 2/5 = 0.40

### Precision-Recall Curves

The relationship between precision and recall is inverse: increasing one typically decreases the other.

**Precision-recall curve**: Shows this trade-off as the decision threshold varies

- **Threshold increases** (