---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:31:46.796894
raw_file_updated: 2026-06-07T06:31:46.796894
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:31:46.796894
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection: A Primer

## Summary

This comprehensive guide explains how [[Machine Learning]] is applied to detect and prevent online credit card [[Fraud|fraud]]. It covers the fundamentals of machine learning algorithms, feature engineering, model evaluation metrics, and operational deployment strategies. The guide uses [[Stripe Radar]] as a case study, demonstrating how machine learning models leverage network-wide transaction data to identify fraudulent patterns while balancing false positives and false negatives.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Online Credit Card Fraud](#online-credit-card-fraud)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Feature Engineering](#feature-engineering)
5. [Model Evaluation](#model-evaluation)
6. [Deployment and Operations](#deployment-and-operations)
7. [Practical Implementation](#practical-implementation)
8. [See Also](#see-also)

---

## Introduction

The rapid acceleration of e-commerce has created a corresponding surge in online payment fraud, costing businesses an estimated $20 billion annually. However, the true cost extends beyond direct losses—fraudulent transactions incur [[Chargeback|chargebacks]], network fees, operational expenses, and damage to customer relationships.

[[Stripe Radar]] represents a modern approach to fraud prevention, utilizing [[Adaptive Machine Learning|adaptive machine learning]] powered by transaction data from hundreds of billions of dollars in payments processed annually across the [[Stripe Network]]. This guide explores how machine learning techniques detect fraud patterns, evaluate model performance, and adapt to evolving fraudster tactics.

---

## Online Credit Card Fraud

### Definition and Mechanics

A payment is considered fraudulent when the cardholder has not authorized the charge. Common scenarios include:

- **Stolen card usage**: A fraudster uses a stolen card number that hasn't yet been reported to the issuing bank
- **Unauthorized transactions**: Charges that appear legitimate initially but are later disputed by the cardholder

### The Chargeback Process

When a cardholder discovers unauthorized use, they file a **dispute** (also called a "[[Chargeback]]") with their bank. Businesses can challenge chargebacks by submitting evidence of transaction validity. However, for [[Card-Not-Present Transactions|card-not-present transactions]], if the payment is deemed fraudulent by payment networks, the cardholder prevails and the business bears:

- Loss of goods/services provided
- Chargeback fees
- Elevated network fees
- Operational costs from dispute management

Excessive chargebacks can result in enrollment in [[Chargeback Monitoring Programs]], leading to higher costs or loss of payment processing capabilities.

### Historical Approaches vs. Machine Learning

**Traditional Rule-Based Systems**: Businesses historically used hard-coded rules to block suspected fraud (e.g., "block all cards used abroad"). While simple, these rules often block legitimate transactions, creating customer friction.

**Machine Learning Advantage**: Machine learning detects nuanced patterns that distinguish between legitimate and fraudulent transactions more accurately, maximizing revenue while managing fraud risk.

---

## Online Credit Card Fraud

### Understanding False Positives and False Negatives

Effective fraud detection requires balancing two types of errors:

#### False Negatives (Missed Fraud)
When the system fails to detect fraudulent transactions, businesses incur:
- Original transaction loss
- [[Chargeback]] fees
- Elevated network fees
- Operational costs
- Potential enrollment in chargeback monitoring programs

#### False Positives (False Declines)
When legitimate customers are prevented from purchasing:
- Direct revenue loss
- Reputational damage
- Customer attrition (research shows 33% of consumers won't return after a false decline)

### The Precision-Recall Trade-off

There is an inherent trade-off: reducing false negatives (catching more fraud) increases false positives (blocking legitimate customers), and vice versa. The optimal balance depends on business-specific factors:

**High-Margin Businesses** (e.g., SaaS): Can tolerate more fraud because the lost revenue from one blocked legitimate customer may exceed the cost of fraudulent transactions. These businesses should lean toward accepting more fraud risk.

**Low-Margin Businesses** (e.g., food delivery): Cannot afford fraud because each fraudulent transaction requires many legitimate sales to offset. These businesses should cast a wider net to prevent fraud.

---

## Machine Learning Fundamentals

### Overview

[[Machine Learning]] refers to techniques that extract patterns from large datasets to create predictive models. In fraud detection, the goal is to predict whether a transaction is fraudulent based on input features.

### Core Components

**Output Variable**: Binary classification—fraudulent (true) or legitimate (false)

**Input Variables (Features)**: Properties that inform predictions, such as:
- Card issuing country
- Number of distinct countries used from in past 24 hours
- Transaction amount
- IP address geolocation
- Merchant category

### How Machine Learning Works

The process involves several steps:

#### 1. Training Data Collection

Machine learning requires historical data with:
- **Features**: Input properties (card country, transaction amount, etc.)
- **Feature Vectors**: Collection of all features for a single transaction
- **Labels/Targets**: Known outcomes (fraudulent or legitimate)

Stripe's advantage: With 90% of cards seen multiple times on the network, models benefit from rich historical context.

#### 2. Model Training

Given training data, machine learning algorithms produce predictive models that assign **fraud probability scores** (e.g., 65% chance fraudulent, 35% chance legitimate) rather than binary classifications.

**Common Techniques**:
- Linear regression
- Decision trees
- Random forests
- [[Neural Networks]] and [[Deep Learning]] (increasingly common for large datasets)

**Stripe's Approach**: Leveraging massive network scale, Stripe employs sophisticated techniques like neural networks to achieve 20%+ year-over-year performance improvements.

#### 3. Decision Trees Example

A simplified decision tree illustrates how models work:

```
Does card amount > $25?
├─ Yes → Is card country = US?
│  ├─ Yes → 15% fraud probability
│  └─ No → 42% fraud probability
└─ No → Is card used from multiple countries?
   ├─ Yes → 8% fraud probability
   └─ No → 3% fraud probability
```

The model answers: "Of historical transactions similar to this one, what fraction was fraudulent?"

---

## Feature Engineering

### Definition

[[Feature Engineering]] is the process of:
1. Identifying features with predictive value based on domain expertise
2. Computing feature values for model training and production deployment

### Importance in Industrial ML

Feature engineering is often more impactful than algorithm selection. Examples of non-obvious predictive features include:

- Time zone difference between user device and UTC
- Count of countries where card was successfully authorized
- IP address consistency with historical patterns
- Merchant embedding similarity

### Implementation Challenges

Creating features requires:
- **Distributed computing**: Processing billions of historical transactions (e.g., using [[Hadoop]])
- **Infrastructure optimization**: Using probabilistic data structures to reduce memory/computation
- **Real-time availability**: Making feature values available during payment processing with low latency

### Advanced Technique: Embeddings

[[Embeddings]] are learned representations that capture semantic relationships between categorical values.

**Example**: Merchant embeddings based on transaction patterns
| Merchant | Dimension 1 | Dimension 2 | Dimension 3 |
|----------|-------------|-------------|-------------|
| Uber     | 2.34        | 1.1         | -3.5        |
| Lyft     | 2.1         | 1.2         | -2.0        |
| Slack    | 7.0         | -2.0        | 1.0         |

Similar merchants (Uber and Lyft) have similar embeddings, allowing models to transfer learnings across merchants. This approach also enables **geographic fraud pattern transfer**—if a fraud pattern is identified in Brazil, the system can automatically detect it in the US without retraining.

**Applications**: Embeddings are used for issuing banks, merchants, user countries, days of week, and other categorical features.

---

## Model Evaluation

### Key Metrics

#### Precision
The fraction of blocked transactions that are actually fraudulent.

**Formula**: `True Positives / (True Positives + False Positives)`

**Interpretation**: Higher precision = fewer false positives

**Example**: If 6 transactions score P(fraud) > 0.7 and 4 are actually fraudulent, precision = 4/6 = 0.67 (67%)

#### Recall (Sensitivity / True Positive Rate)
The fraction of all fraudulent transactions that are detected.

**Formula**: `True Positives / (True Positives + False Negatives)`

**Interpretation**: Higher recall = fewer false negatives

**Example**: If 5 transactions