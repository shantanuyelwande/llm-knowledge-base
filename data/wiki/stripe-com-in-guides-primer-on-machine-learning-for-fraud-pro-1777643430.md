---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-05T05:21:00.002267
raw_file_updated: 2026-05-05T05:21:00.002267
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-05T05:21:00.002267
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Prevention

## Summary

This comprehensive guide explains how [[Stripe Radar]], a machine learning-based fraud prevention solution, detects and prevents online credit card fraud by leveraging data from the Stripe network. It covers fundamental [[machine learning]] concepts, model evaluation techniques, and practical strategies for balancing fraud detection with customer experience.

---

## Overview

Online [[payment fraud]] costs businesses over $20 billion annually worldwide. Beyond direct losses, fraud creates additional costs through chargebacks, network fees, and operational expenses. [[Stripe Radar]] addresses this challenge through adaptive machine learning that evaluates every transaction for fraud risk using patterns identified across hundreds of billions of dollars in annual Stripe network transactions.

Unlike traditional rule-based fraud prevention systems, machine learning can detect nuanced fraud patterns while minimizing false declines—rejected legitimate transactions that damage customer relationships and business revenue.

---

## Table of Contents

1. [Understanding Online Credit Card Fraud](#understanding-online-credit-card-fraud)
2. [Stripe Radar and the Stripe Network](#stripe-radar-and-the-stripe-network)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Model Evaluation Metrics](#model-evaluation-metrics)
5. [Deploying Models Safely](#deploying-models-safely)
6. [Optimizing Fraud Prevention](#optimizing-fraud-prevention)

---

## Understanding Online Credit Card Fraud

### What Constitutes Fraud

A transaction is fraudulent when the [[cardholder]] does not authorize the charge. Common scenarios include:

- Stolen card numbers used before being reported
- Card-not-present transactions processed without authorization
- Fraudulent charges discovered later by the cardholder

### The Chargeback Process

When cardholders discover unauthorized charges, they file disputes (chargebacks) with their banks. While businesses can challenge chargebacks with evidence, card-not-present fraudulent transactions typically result in:

- Full loss of goods and services
- Chargeback fees (bank reversal costs)
- Elevated network fees due to disputes
- Increased operational costs for dispute resolution

### The False Positive vs. False Negative Trade-off

Traditional rule-based systems (such as blocking all international transactions) create significant problems:

**False Negatives** (Missed Fraud):
- Fraudulent transactions that bypass detection
- Cost: transaction amount + chargeback fees + elevated network fees

**False Positives** (False Declines):
- Legitimate transactions incorrectly blocked
- Impact: 33% of consumers don't return after a false decline
- Cost: lost revenue and customer lifetime value

#### Business-Specific Considerations

The optimal fraud prevention strategy depends on business economics:

- **Low-margin businesses** (e.g., food delivery): Can afford fewer false negatives; one fraudulent transaction costs the profit of 18+ legitimate sales
- **High-margin businesses** (e.g., [[SaaS]]): Can afford more fraud; one blocked customer may cost more than multiple fraudulent transactions

---

## Stripe Radar and the Stripe Network

### How Radar Works

[[Stripe Radar]] is a machine learning-powered fraud prevention system fully integrated into the Stripe platform. It:

- Evaluates every transaction for fraud risk
- Automatically blocks high-risk payments
- Provides tools for custom rules and manual review through [[Radar for Fraud Teams]]
- Requires no engineering integration or manual labeling

### Network Advantages

Stripe's scale provides significant competitive advantages:

**Data Scale**: Processes hundreds of billions in annual payments from millions of businesses across thousands of partner banks globally

**Early Signal Detection**: Often identifies fraud patterns earlier than smaller networks

**Card History**: 90% of cards used on Stripe have been seen multiple times, providing rich historical data for risk assessment

**Integrated Ground Truth**: Receives fraud labels directly from the payment flow and card networks—no manual labeling required

### Key Features

- **Automatic Integration**: Works immediately upon activation; no coding required
- **Real-time Evaluation**: Processes transaction features with minimal latency
- **Network Learning**: Improves continuously as Stripe processes more transactions
- **Performance Gains**: Recent models improved fraud detection by over 20% year-over-year

---

## Machine Learning Fundamentals

### Core Concepts

[[Machine learning]] is a set of techniques for using large datasets to create models that predict outcomes. In fraud detection, models predict whether a transaction is fraudulent based on input features.

**Key Terms**:

- **Features**: Input variables (e.g., card country, transaction amount, IP address)
- **Feature Vector**: Collection of all features for a single transaction
- **Target/Label**: Output value (fraudulent or legitimate)
- **Training Data**: Historical transactions with known fraud outcomes
- **Model**: Algorithm that maps features to fraud probability

### How Machine Learning Works

#### Step 1: Obtain Training Data

Machine learning requires historical examples with:
- Known outcomes (fraudulent or legitimate)
- Relevant input features for prediction

Example simplified dataset:

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10 | US | 1 | No |
| $10 | CA | 2 | No |
| $30 | US | 1 | Yes |
| $99 | CA | 1 | Yes |

#### Step 2: Train a Model

The machine learning algorithm learns patterns from training data. A simple example is a [[decision tree]] that asks sequential questions to classify transactions:

```
Is Amount > $25?
├─ Yes → Is Card Country = US?
│        ├─ Yes → Likely Fraudulent
│        └─ No → Legitimate
└─ No → Likely Legitimate
```

The model outputs a probability (e.g., 65% likely fraudulent, 35% likely legitimate) rather than a binary classification.

#### Step 3: Select an Algorithm

Common approaches include:

- **Linear Regression**: Simple, interpretable relationships
- **Decision Trees**: Easy to visualize and understand
- **Random Forests**: Multiple decision trees for improved accuracy
- **Neural Networks & Deep Learning**: Sophisticated pattern recognition for large datasets

**Stripe's Approach**: Leverages [[neural networks]] and deep learning due to the massive scale of Stripe's dataset, achieving superior fraud detection performance.

### Feature Engineering

Feature engineering—creating predictive input variables—is one of the most critical aspects of industrial machine learning.

#### Formulating Features

Data scientists develop features based on:
- Domain expertise in fraud patterns
- Analysis of thousands of fraud cases
- Intuition about what signals indicate fraud

**Example features**:
- Whether payment originates from a previously-seen IP address
- Difference between device time and UTC
- Count of countries where card was successfully authorized
- Number of distinct merchants used in past 24 hours

#### Computing Features

Once formulated, historical feature values must be computed for model training. This requires:
- Processing entire Stripe transaction history
- Distributed computing (e.g., [[Hadoop]] jobs)
- Optimization for speed and memory efficiency
- Real-time computation infrastructure for production

#### Embeddings for Categorical Features

Rather than manually encoding categorical variables (country, merchant, bank), Stripe uses [[embeddings]]—learned numerical representations that capture similarity relationships.

**Example**:

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

Similar merchants (Uber/Lyft) have similar embeddings; the model learns that fraud patterns in one region transfer to similar merchants in other regions without explicit retraining.

---

## Model Evaluation Metrics

### Key Terms

#### Precision

The fraction of blocked transactions that are actually fraudulent.

**Formula**: True Positives / (True Positives + False Positives)

**Example**: If 6 transactions are blocked and 4 are actually fraudulent, precision = 4/6 = 66.7%

**Interpretation**: Higher precision means fewer false declines

#### Recall (Sensitivity/True Positive Rate)

The fraction of all fraudulent transactions that are caught.

**Formula**: True Positives / (True Positives + False Negatives)

**Example**: If 5 transactions are fraudulent and 4 are caught, recall = 4/5 = 80%

**Interpretation**: Higher recall means less fraud slips through

#### False Positive Rate

The fraction of legitimate transactions incorrectly blocked.

**Formula**: False Positives / (False Positives + True Negatives)

**Example**: If 5 transactions are legitimate and 2 are blocked, false positive rate = 2