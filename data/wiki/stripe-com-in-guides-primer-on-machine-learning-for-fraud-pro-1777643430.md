---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-04T06:49:39.641848
raw_file_updated: 2026-06-04T06:49:39.641848
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-04T06:49:39.641848
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Protection

## Summary

This article provides a comprehensive guide to understanding how [[machine learning]] is applied to online payment fraud detection, with specific focus on [[Stripe Radar]], a fraud prevention solution that leverages data from hundreds of billions of dollars in payments processed annually. The guide covers the fundamentals of machine learning, model evaluation techniques, deployment strategies, and practical considerations for balancing fraud prevention against customer experience.

---

## Introduction

The exponential growth of [[e-commerce]] has created a corresponding surge in online payment fraud, costing businesses an estimated $20 billion annually. However, the true cost to businesses extends far beyond direct fraud losses, including operational costs, network fees, and customer churn. [[Stripe Radar]] represents a machine learning-based approach to fraud prevention that leverages the scale of the Stripe network to detect fraud patterns while maintaining low false positive rates.

This article serves as a primer on the machine learning techniques used in modern fraud detection systems, explaining both the technical foundations and the business considerations necessary for effective fraud prevention.

---

## Online Credit Card Fraud Fundamentals

### Definition and Mechanics

A payment is considered fraudulent when the [[cardholder]] does not authorize the charge. Fraudulent transactions typically occur when:

- A stolen [[credit card]] number is used before the cardholder detects the fraud
- The cardholder later disputes the transaction with their bank through a [[chargeback]]
- Businesses attempt to challenge the chargeback with supporting evidence

For card-not-present transactions, if networks determine the transaction was genuinely fraudulent, the cardholder prevails and the business becomes liable for the loss of goods plus associated fees.

### Traditional vs. Machine Learning Approaches

Historically, businesses relied on brute-force rules to prevent fraud—for example, blocking all transactions from certain geographic regions. While simple to implement, hard-coded rules often result in:

- **False positives**: Blocking legitimate customers (also called "false declines")
- Reduced revenue and customer dissatisfaction

[[Machine learning]] enables detection of more nuanced patterns, improving accuracy while reducing unnecessary transaction blocking.

### The False Negative vs. False Positive Trade-off

Understanding the cost structure of fraud prevention is critical:

**False Negatives (Missed Fraud)**
- Original transaction amount lost
- [[Chargeback]] fees from the issuing bank
- Elevated network fees due to dispute ratios
- Increased operational costs for reviewing and fighting disputes
- Risk of entering network chargeback monitoring programs

**False Positives (False Declines)**
- Lost revenue from legitimate transactions
- Significant reputational damage—33% of consumers report not shopping again at a retailer after a false decline
- Reduced customer lifetime value

### Margin-Based Decision Making

The optimal fraud prevention strategy depends on business economics:

- **Low-margin businesses** (e.g., food e-commerce): A fraudulent transaction may require hundreds of legitimate sales to offset the loss, making false negatives extremely expensive. These businesses may tolerate higher false positive rates.

- **High-margin businesses** (e.g., SaaS): The lost revenue from one blocked legitimate customer may exceed the cost of increased fraud, making false positives more costly than false negatives.

---

## Stripe Radar and Network Effects

### Core Capabilities

[[Stripe Radar]] is Stripe's machine learning-powered fraud prevention solution that:

- Evaluates every transaction for fraud risk using adaptive algorithms
- Automatically blocks high-scoring payments
- Provides tools through [[Radar for Fraud Teams]] for custom actions and manual reviews
- Integrates directly into the Stripe platform without additional engineering work

### Network Advantages

Stripe processes hundreds of billions in payments annually from millions of businesses, creating significant data advantages:

1. **Early Signal Detection**: The scale of the Stripe network enables detection of fraud patterns and signals earlier than smaller networks can observe them.

2. **Card Reuse Data**: 90% of cards used on the Stripe network have been seen more than once, providing rich historical data for risk assessment.

3. **Network Features**: Aggregate signals across the network—such as card issuance country, IP address geography, and historical card usage patterns—inform fraud predictions.

### Operational Advantages

Unlike traditional fraud solutions, Radar requires minimal integration effort:

- No additional engineering work needed to send transaction data
- No manual labeling of transactions as fraudulent or legitimate
- Automatic access to accurate ground truth data from the Stripe payment flow
- Direct integration with card network and issuer data

---

## Machine Learning Fundamentals

### Core Concept

[[Machine learning]] refers to techniques for processing large datasets to produce models that predict outcomes—in this case, the likelihood a payment will result in a fraud dispute. The process involves:

1. **Input variables** (features): Properties like card issuance country, transaction amount, IP address geography
2. **Output variable** (label/target): Boolean indicating whether the transaction was fraudulent
3. **Model**: A learned function mapping inputs to fraud probability predictions

### Example: Decision Trees

A simplified example demonstrates how machine learning models work:

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10.00 | US | 1 | No |
| $10.00 | CA | 2 | No |
| $10.00 | CA | 1 | No |
| $10.00 | US | 1 | Yes |
| $30.00 | US | 1 | Yes |
| $99.00 | CA | 1 | Yes |

A decision tree model learned from this data answers: "Of transactions in our dataset with properties similar to this one, what fraction was actually fraudulent?" The model traverses a series of decision rules until reaching a leaf node containing the probability estimate.

While [[decision trees]] are intuitive, modern fraud detection employs more sophisticated approaches including [[neural networks]] and [[deep learning]], which Stripe leverages due to the scale of its training data.

### Machine Learning Algorithms in Practice

Common industrial approaches include:

- **Linear regression**: Simple, interpretable, often effective
- **Decision trees and random forests**: Ensemble methods with good performance
- **Neural networks and deep learning**: Advanced techniques requiring large datasets; responsible for major breakthroughs in AI
- **Embeddings**: Learned representations capturing similarity relationships

Stripe's models have improved fraud detection performance by over 20% year-over-year through sophisticated techniques enabled by network scale.

---

## Feature Engineering

### Definition and Importance

[[Feature engineering]] is one of the most critical aspects of industrial machine learning, consisting of two components:

1. **Formulation**: Creating features with predictive value based on domain expertise and analysis of fraud patterns
2. **Implementation**: Engineering systems to compute feature values both for model training and real-time production deployment

### Examples of Effective Features

Data scientists at Stripe discovered that numerous features predict fraud, including:

- Whether a payment originates from an IP address commonly associated with that card
- Difference between device time and UTC (Coordinated Universal Time)
- Count of distinct countries where the card was successfully authorized
- Historical patterns of card usage across the Stripe network

### Embedding Representations

For categorical features (such as merchant type, issuing bank, or user country), Stripe employs [[embeddings]]—learned numerical representations capturing similarity relationships.

**Example Embedding Space:**

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

Embeddings enable:

- **Transfer learning**: Fraud patterns identified in one geographic region automatically apply to similar regions
- **Semantic relationships**: Similar merchants receive similar embeddings measured by [[cosine distance]]
- **Scalability**: Effective representation of high-cardinality categorical features

This approach mirrors techniques used in [[natural language processing]] (Word2Vec, BERT, GPT-3) but applies them to entities within the Stripe network.

---

## Evaluating Machine Learning Models

### Key Performance Metrics

#### Precision

The fraction of transactions flagged as fraud that are actually fraudulent.

**Formula**: True Positives / (True Positives + False Positives)

**Example**: If 6 transactions exceed the fraud threshold and 4 are actually fraudulent, precision = 4/6 = 0.66 (66%)

**Interpretation**: Higher precision means fewer false positives (legitimate transactions incorrectly blocked)

#### Recall

The fraction of all fraudulent transactions that the model successfully identifies. Also called sensitivity or true positive rate.

**Formula**: True Positives / (True Positives + False Negatives)

**Example**: If 5 transactions are actually fraudulent and the model catches 4, recall = 4/5 = 0