---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-05T06:31:05.402776
raw_file_updated: 2026-06-05T06:31:05.402776
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-05T06:31:05.402776
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection: A Comprehensive Guide

## Summary

This article provides a technical primer on how [[machine learning]] is applied to [[fraud detection]] in online payments, with a focus on [[Stripe Radar]], a machine learning-based fraud prevention solution. It explains fundamental ML concepts, evaluation metrics for fraud detection systems, and the trade-offs between catching fraudulent transactions and maintaining customer experience through minimizing false declines.

---

## Introduction

Online payment fraud costs businesses an estimated $20 billion annually, with the true cost to businesses being significantly higher when accounting for [[chargeback]] fees, network fees, and operational expenses. As fraudsters continuously evolve their tactics, traditional rule-based fraud prevention systems prove insufficient. This guide introduces how [[machine learning]] enables more sophisticated fraud detection by identifying nuanced patterns across vast payment networks, specifically examining [[Stripe Radar]] and the principles underlying modern fraud detection systems.

---

## Table of Contents

1. [Online Credit Card Fraud](#online-credit-card-fraud)
2. [Stripe Radar and Network Effects](#stripe-radar-and-network-effects)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Model Evaluation Metrics](#model-evaluation-metrics)
5. [Deploying ML Models in Production](#deploying-ml-models-in-production)
6. [Optimizing Fraud Prevention](#optimizing-fraud-prevention)

---

## Online Credit Card Fraud

### Definition and Process

A payment is considered [[fraud|fraudulent]] when the [[cardholder]] does not authorize the charge. In card-not-present transactions, if a fraudster uses a stolen card number that hasn't been reported, the payment may process successfully. When the legitimate cardholder discovers the unauthorized use, they file a [[dispute]] (also called a "[[chargeback]]") with their bank.

### Business Impact

When a chargeback is filed, businesses face multiple financial consequences:
- Loss of goods or services provided
- [[Chargeback]] fees levied by payment networks
- Increased network fees due to elevated dispute ratios
- Operational costs for reviewing and fighting disputes
- Risk of enrollment in chargeback monitoring programs, potentially leading to higher costs or payment processing restrictions

### The False Negative vs. False Positive Trade-off

Traditional fraud prevention relied on hard-coded rules (e.g., blocking all international transactions), which often resulted in blocking legitimate transactions. Machine learning enables more nuanced detection but introduces an important trade-off:

**[[False Negatives]]**: Fraudulent transactions that slip through detection
- Cost: Original transaction amount + chargeback fees + network fees + operational costs

**[[False Positives]]** (False Declines): Legitimate customers blocked from making purchases
- Cost: Lost gross profit + reputational damage
- Research shows 33% of consumers won't shop again after a false decline

### Business Context Matters

The optimal balance between false negatives and false positives depends on business characteristics:

- **Low-margin businesses** (e.g., food e-commerce): Each fraudulent transaction may require hundreds of legitimate sales to offset the loss, favoring aggressive fraud blocking
- **High-margin businesses** (e.g., SaaS): Lost revenue from one blocked legitimate customer may outweigh costs of increased fraud, favoring permissive blocking

---

## Stripe Radar and Network Effects

### Overview

[[Stripe Radar]] is an adaptive [[machine learning]]-based fraud prevention solution built directly into the Stripe payment platform. It evaluates every transaction for fraud risk and automatically blocks high-risk payments while providing tools for custom actions through [[Radar for Fraud Teams]].

### Network Advantages

Stripe's scale provides significant advantages for fraud detection:

- **Massive Dataset**: Stripe processes hundreds of billions in payments annually from millions of businesses
- **Early Signal Detection**: With such volume, Stripe can identify fraud patterns earlier than smaller networks
- **Card Recurrence**: 90% of cards used on the Stripe network have been seen multiple times, providing rich historical data for assessment
- **Network Signals**: Aggregate data including card issuance country, IP address origin, and cross-merchant patterns inform predictions

### Integration Advantages

Unlike third-party fraud solutions, Radar requires no additional engineering work:

- **Automatic Data Collection**: Ground truth information flows directly from Stripe's payment processing
- **Real-time Network Data**: Access to timely, accurate data from card networks and issuers
- **No Manual Labeling**: Eliminates error-prone manual transaction classification
- **Immediate Deployment**: Works out of the box without integration overhead

---

## Machine Learning Fundamentals

### Core Concepts

[[Machine learning]] refers to techniques that use large amounts of data to produce models that predict outcomes. In fraud detection, the goal is to predict whether a given transaction will result in a fraud dispute based on input features (also called [[features]]).

**Key Terminology:**
- **[[Feature]]**: An input variable used for prediction (e.g., card country, transaction amount)
- **[[Feature Vector]]**: The collection of all input features for a single transaction
- **[[Target]]** or **[[Label]]**: The output value being predicted (fraudulent or legitimate)
- **[[Training Data]]**: Historical records with both input features and known output values

### How Machine Learning Works

The machine learning process involves several key steps:

#### 1. Data Collection and Feature Engineering

Before building a model, you need training data with examples of both fraudulent and legitimate transactions. Each transaction requires:
- Multiple input features that could be predictive
- A known output label (was it actually fraudulent?)

Example training data structure:

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10.00 | US | 1 | No |
| $10.00 | CA | 2 | No |
| $30.00 | US | 1 | Yes |
| $99.00 | CA | 1 | Yes |

#### 2. Model Training

A [[machine learning algorithm]] learns patterns from training data to create a model that maps inputs to outputs. For example, a [[decision tree]] might ask sequential questions:
- "Is the amount > $25?"
- "Is the card country = US?"
- "How many countries used in 24h?"

The model outputs a probability that a transaction is fraudulent based on similar historical transactions.

#### 3. Feature Engineering in Practice

Feature engineering is one of the most involved aspects of industrial ML and consists of two parts:

**Formulation**: Data scientists develop intuition about which features predict fraud by examining thousands of fraud cases. Non-obvious predictive features include:
- Time difference between user device and UTC
- Count of countries where card was successfully authorized
- Most frequent IP addresses for a given card

**Implementation**: Once formulated, features must be computed:
- For all historical transactions (for model training)
- For all real-time transactions (for production inference)

This requires dedicated infrastructure, often using distributed systems like [[Hadoop]] for historical computation and optimized real-time systems for production.

### Advanced Techniques: Embeddings

Rather than manually defining features for categorical values (like merchant type or issuing bank), modern ML systems learn [[embeddings]] - numerical representations that capture similarity relationships.

**Example**: Merchant embeddings might place Uber and Lyft close together (similar merchants) while placing Slack far away, allowing the model to transfer learned fraud patterns between similar merchants.

Benefits of embeddings:
- Capture complex semantic relationships automatically
- Enable pattern transfer: A fraud pattern detected in Brazil can automatically apply to the US
- Scale efficiently to high-cardinality features
- Improve model generalization

**Advanced Architectures**: Stripe uses cutting-edge approaches including [[neural networks]] and [[deep learning]], which have achieved:
- 20%+ year-over-year performance improvements
- Better fraud detection while maintaining low false positives
- Ability to discover complex non-linear relationships

---

## Model Evaluation Metrics

### Key Terms

To evaluate fraud detection model performance, several metrics are essential:

#### Precision
The fraction of transactions flagged as fraudulent that actually are fraudulent.

**Formula**: True Positives / (True Positives + False Positives)

**Interpretation**: High precision means fewer false declines (blocked legitimate customers)

**Example**: If 6 transactions score > 0.7 (fraud probability threshold) and 4 are actually fraudulent:
- Precision = 4/6 = 0.67 (67%)

#### Recall
The fraction of all actual fraud that is caught by the model; also called [[sensitivity]] or [[true positive rate]].

**Formula**: True Positives / (True Positives + False Negatives)

**Interpretation**: High recall means fewer fraudulent transactions slip through

**Example**: If 5 transactions are actually fraudulent and 4 score > 0.7:
- Recall = 4/5 = 0.80 (80%)

#### False Positive Rate
The fraction of all