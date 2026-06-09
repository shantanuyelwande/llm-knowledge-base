---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-09T06:17:08.260160
raw_file_updated: 2026-06-09T06:17:08.260160
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-09T06:17:08.260160
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection

## Summary

This article provides a comprehensive overview of how [[machine learning]] is applied to [[fraud detection]] in online payments, specifically through [[Stripe Radar]]. It covers the fundamentals of machine learning techniques, the trade-offs between [[false positives]] and [[false negatives]], methods for evaluating fraud detection models, and practical strategies for optimizing fraud prevention systems. The guide emphasizes that effective fraud detection requires balancing the prevention of fraudulent transactions with minimizing the blocking of legitimate customers.

---

## Overview

The rapid growth of e-commerce has led to a corresponding increase in online payment fraud, which costs businesses an estimated $20 billion annually. Beyond direct losses, fraud imposes additional costs through operational expenses, network fees, and customer churn. [[Stripe Radar]] is a machine learning-based fraud prevention solution that leverages data from hundreds of billions of dollars in payments processed across the Stripe network to detect fraud accurately and adapt to evolving fraud patterns.

---

## Table of Contents

1. [The Problem: Online Credit Card Fraud](#the-problem-online-credit-card-fraud)
2. [Stripe Radar and Network Advantages](#stripe-radar-and-network-advantages)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Feature Engineering](#feature-engineering)
5. [Model Evaluation Metrics](#model-evaluation-metrics)
6. [Deploying Models in Production](#deploying-models-in-production)
7. [Optimizing Fraud Prevention](#optimizing-fraud-prevention)
8. [Key Concepts and Trade-offs](#key-concepts-and-trade-offs)

---

## The Problem: Online Credit Card Fraud

### Understanding Fraudulent Transactions

A payment is considered fraudulent when the [[cardholder]] does not authorize the charge. Common scenarios include:

- A fraudster makes a purchase using a stolen [[credit card]] number that hasn't been reported to the card issuer
- The transaction initially processes successfully
- The cardholder later discovers the unauthorized use and files a [[dispute]] (also called a "[[chargeback]]") with their bank

### Liability and Consequences

When a chargeback occurs:
- Businesses can challenge the dispute by submitting evidence of validity
- For [[card-not-present transactions]], if the payment is deemed fraudulent by payment networks, the cardholder wins
- The business becomes liable for the loss of goods plus additional fees

### Historical Approaches vs. Machine Learning

**Traditional Rule-Based Approach:**
- Businesses used hard-coded rules (e.g., "block all cards used abroad")
- Results in blocking many legitimate transactions alongside fraudulent ones
- Inflexible and unable to adapt to new fraud patterns

**Machine Learning Approach:**
- Detects nuanced patterns in transaction data
- Maximizes legitimate transaction approval while catching fraud
- Adapts automatically to evolving fraud techniques

---

## Stripe Radar and Network Advantages

### What is Stripe Radar?

[[Stripe Radar]] is Stripe's adaptive [[machine learning]]-based fraud prevention solution that:
- Evaluates every transaction for fraud risk
- Blocks high-scoring payments automatically
- Provides tools through [[Radar for Fraud Teams]] for custom actions
- Integrates directly into the Stripe platform

### Network-Scale Advantages

Stripe processes hundreds of billions in payments annually from millions of businesses, providing significant advantages:

**Early Pattern Detection:** The scale of the Stripe network enables detection of fraud signals and patterns much earlier than smaller payment networks.

**Card Reuse Data:** Approximately 90% of cards used on the Stripe network have been seen more than once, providing rich historical data for accurate risk assessment.

**Network Signals:** Valuable signals include:
- Country in which the card was issued
- IP address from which the payment was made
- Historical transaction patterns for the card

### Built-In Integration

Unlike third-party fraud solutions, Radar:
- Works out of the box with no engineering integration required
- Automatically receives "ground truth" information from the standard Stripe payment flow
- Accesses timely and accurate data directly from card networks and issuers
- Requires no manual payment labeling or data transmission

---

## Machine Learning Fundamentals

### Core Concept

[[Machine learning]] refers to techniques for using large amounts of data to produce models that predict outcomes. In fraud detection, the goal is to predict whether a charge will result in a fraud dispute based on transaction characteristics.

### The Prediction Problem

**Output Variable:** Boolean value indicating whether a payment is fraudulent (true/false)

**Input Variables (Features):** Examples include:
- Country in which the card was issued
- Number of distinct countries where the card was used in the past 24 hours
- Transaction amount
- IP address of the transaction

**Training Data:** Historical records containing both input features and output labels

### How Machine Learning Models Work

Machine learning algorithms learn patterns from training data and create models that can make predictions on new data. A simple example is a [[decision tree]]:

```
Does the amount exceed $25?
├─ Yes → Is the card country the same as transaction country?
│        ├─ Yes → Probably legitimate
│        └─ No → Probably fraudulent
└─ No → Probably legitimate
```

The algorithm automatically determines:
- What questions to ask (which features matter)
- In what order to ask them
- How to combine the answers for predictions

### Modern Approaches

While simple models like decision trees are interpretable, modern fraud detection uses more sophisticated techniques:

- **[[Neural Networks]]:** Inspired by brain architecture, these models can capture complex relationships in data
- **[[Deep Learning]]:** Advanced neural network approaches that excel with large datasets
- **[[Random Forests]]:** Ensemble methods combining multiple decision trees

Stripe's scale enables use of cutting-edge neural network approaches, improving detection performance by over 20% year-over-year.

---

## Feature Engineering

### Overview

[[Feature engineering]] is one of the most involved aspects of industrial machine learning. It consists of two components:

1. **Formulation:** Creating features with predictive value based on domain knowledge
2. **Implementation:** Making feature values available for both model training and production deployment

### Feature Development Process

**Hypothesis Generation:** Data scientists develop hunches about useful features through analysis of thousands of fraud cases. Counterintuitive features often emerge, such as:
- Difference between device time and Coordinated Universal Time (UTC)
- Count of countries where the card was successfully authorized

**Historical Computation:** Once a feature is identified, its historical values must be computed for all transactions to train new models. This may involve:
- Distributed computing systems like [[Hadoop]]
- Space-saving probabilistic data structures for efficiency

**Production Availability:** Features must be computed in real-time as transactions occur, requiring dedicated infrastructure.

### Embeddings for Categorical Features

Not all features are manually engineered. Categorical features (like merchant type or country) can be represented as [[embeddings]]:

**What are Embeddings?** Learned vector representations where similar entities have similar coordinates. For example:

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|--------|-------------|-------------|-------------|
| Uber   | 2.34        | 1.1         | -3.5        |
| Lyft   | 2.1         | 1.2         | -2.0        |
| Slack  | 7.0         | -2.0        | 1.0         |

**Advantages:**
- Uber and Lyft have similar embeddings (related services)
- Slack has distinct embeddings (different industry)
- Models can transfer learnings between similar entities
- Enables geographic transfer of fraud patterns (e.g., Brazil to US)

**Applications at Stripe:** Embeddings are created for:
- Merchant types
- Issuing banks
- User countries
- Days of the week

---

## Model Evaluation Metrics

### Key Terminology

Understanding fraud detection performance requires clear definitions:

#### Precision

**Definition:** The fraction of transactions flagged as fraud that are actually fraudulent.

**Formula:** `Precision = True Positives / (True Positives + False Positives)`

**Example:** If 6 transactions score above the fraud threshold and 4 are actually fraudulent:
- Precision = 4/6 = 0.66 (66%)

**Interpretation:** Higher precision means fewer [[false positives]] (legitimate customers blocked).

#### Recall (Sensitivity)

**Definition:** The fraction of all fraudulent transactions that are caught by the system.

**Formula:** `Recall = True Positives / (True Positives + False Negatives)`

**Example:** If 5 transactions are actually fraudulent and the system catches 4:
- Recall = 4/5 = 0.80 (80%)

**Interpretation:** Higher recall means fewer [[false negatives]] (fraud that slips through).

#### False