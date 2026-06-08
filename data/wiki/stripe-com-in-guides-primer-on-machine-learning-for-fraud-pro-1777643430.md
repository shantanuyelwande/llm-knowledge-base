---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-08T06:51:26.277310
raw_file_updated: 2026-06-08T06:51:26.277310
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-08T06:51:26.277310
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Protection

## Summary

**Machine Learning for Fraud Protection** is a comprehensive guide to understanding how [[machine learning]] techniques are applied to detect and prevent online [[credit card fraud]]. The guide, published by [[Stripe]], explains the fundamentals of machine learning, the mechanics of fraud detection systems, and the trade-offs between preventing fraudulent transactions and maintaining legitimate customer experiences. It covers key concepts including [[feature engineering]], model evaluation metrics, and the operational challenges of deploying machine learning models in production fraud prevention systems.

---

## Overview

Online payment fraud costs businesses over $20 billion annually worldwide. Beyond direct losses, the true cost to businesses is substantially higher when accounting for [[chargeback]] fees, increased network fees, and customer churn. Traditional rule-based fraud prevention systems often block legitimate transactions while missing sophisticated fraud attempts. [[Machine learning]] offers a more nuanced approach to fraud detection by identifying complex patterns across large datasets.

This guide introduces how machine learning-based fraud prevention works, specifically through the lens of [[Stripe Radar]], and provides practical frameworks for understanding and evaluating fraud detection system performance.

---

## Table of Contents

1. [Online Credit Card Fraud](#online-credit-card-fraud)
2. [The Stripe Network Advantage](#the-stripe-network-advantage)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Feature Engineering](#feature-engineering)
5. [Model Evaluation](#model-evaluation)
6. [Deployment and Operations](#deployment-and-operations)
7. [Optimization Strategies](#optimization-strategies)

---

## Online Credit Card Fraud

### Definition and Mechanics

A transaction is classified as fraudulent when the [[cardholder]] does not authorize the charge. Common fraud scenarios include:

- Unauthorized use of stolen card numbers that haven't yet been reported
- Card-not-present transactions where the fraudster gains access to card details
- Fraudulent transactions that proceed successfully until the cardholder discovers them and files a [[dispute]] (also called a "[[chargeback]]")

### The Chargeback Process

When a cardholder disputes a transaction, the card network may reverse the payment and return funds to the cardholder. Businesses can challenge chargebacks by submitting evidence of transaction validity. However, for card-not-present transactions, if the networks determine the transaction was truly fraudulent, the business bears the liability including:

- Loss of goods or services provided
- Chargeback fees
- Increased network fees due to dispute history
- Higher operational costs for dispute management

Excessive chargebacks can result in placement in network chargeback monitoring programs, potentially leading to higher processing costs or inability to accept card payments.

### False Positives vs. False Negatives

Fraud prevention systems must navigate a critical trade-off:

**False Negatives** occur when the system fails to detect actual fraud:
- Business loses the transaction amount plus chargeback fees
- Increased network fees result from dispute history
- Higher operational costs from dispute management
- Risk of chargeback monitoring program enrollment

**False Positives** occur when legitimate customers are incorrectly blocked:
- Direct loss of transaction revenue
- Reputational damage to the business
- Customer attrition (33% of consumers report they won't return after a false decline)

### Business-Specific Trade-offs

The optimal balance between false positives and false negatives depends on business characteristics:

**Low-Margin Businesses** (e.g., food e-commerce):
- Each fraudulent transaction requires hundreds of legitimate sales to offset
- False negatives are extremely costly
- May justify aggressive fraud blocking strategies

**High-Margin Businesses** (e.g., SaaS):
- Lost revenue from one blocked legitimate customer may exceed fraud losses
- False positives are more costly than false negatives
- May tolerate higher fraud rates to avoid blocking customers

---

## The Stripe Network Advantage

### Scale and Data Access

[[Stripe]] processes hundreds of billions of dollars in payments annually from millions of businesses across thousands of partner banks globally. This scale provides significant advantages:

- **Early pattern detection**: Stripe often identifies fraud signals and patterns earlier than smaller networks
- **Rich historical data**: 90% of cards used on the Stripe network have been seen multiple times, enabling more informed risk assessments
- **Network-wide signals**: Aggregate data from all Stripe transactions (collected automatically through the payment flow) improves fraud detection accuracy

### Integrated Data Collection

Unlike standalone fraud prevention services, [[Stripe Radar]] is built directly into the Stripe platform and offers several advantages:

- **Automatic data collection**: Ground truth information (whether transactions were actually fraudulent) flows directly from the normal Stripe payment process
- **Network and issuer data**: Real-time access to data from card networks and issuing banks
- **No engineering overhead**: Businesses don't need to build custom integrations or manually label transactions
- **Reduced operational burden**: No need for custom engineering work to send event data or payment labels to external services

---

## Machine Learning Fundamentals

### Core Concepts

[[Machine learning]] refers to techniques for taking large amounts of data and producing models that predict outcomes. In fraud detection, the goal is to predict whether a given transaction is likely to result in a fraud dispute.

**Key Components:**

- **Input variables (features)**: Observable transaction properties such as card country, transaction amount, or IP address geolocation
- **Output variable (target/label)**: Whether the transaction was actually fraudulent (boolean: true/false)
- **Training data**: Historical records containing both input features and output labels
- **Model**: A learned algorithm that maps input features to predicted fraud probability

### The Training Process

The machine learning workflow consists of several steps:

1. **Data collection**: Gather historical transactions with known fraud outcomes
2. **Feature selection**: Identify which input properties are predictive of fraud
3. **Model training**: Use a machine learning algorithm to learn relationships between features and fraud outcomes
4. **Model validation**: Test the model on held-out data to assess performance
5. **Deployment**: Put the validated model into production
6. **Monitoring**: Track model performance and identify drift

### Example: Decision Trees

A simple machine learning model might be represented as a decision tree:

```
Is the transaction amount > $50?
├─ Yes: Is the card country = US?
│   ├─ Yes: Fraud probability = 10%
│   └─ No: Fraud probability = 35%
└─ No: Fraud probability = 5%
```

The model answers: "Of transactions in our training data with properties similar to this one, what fraction was actually fraudulent?"

### Advanced Approaches

Modern fraud detection uses sophisticated techniques including:

- **[[Neural networks]] and [[deep learning]]**: Brain-inspired architectures that excel with large datasets
- **Random forests**: Ensemble methods that combine multiple decision trees
- **Linear models**: Simple but effective approaches for many applications

[[Stripe]] leverages the scale of its network to employ cutting-edge deep learning approaches, achieving over 20% year-over-year improvements in fraud detection performance.

---

## Feature Engineering

### Overview

[[Feature engineering]] is one of the most critical and labor-intensive aspects of industrial machine learning. It consists of two parts:

1. **Formulation**: Identifying features with predictive value based on domain expertise
2. **Implementation**: Engineering systems to compute feature values both for model training and real-time production use

### Feature Examples

Data scientists at Stripe identify predictive features through extensive analysis of fraud patterns:

- **IP address history**: Whether a payment originates from IP addresses previously associated with the card
- **Geographic patterns**: Difference between device time and UTC, or count of countries where card was used in past 24 hours
- **Transaction patterns**: Merchant category, transaction amount relative to historical norms
- **Network velocity**: Frequency of card use across the Stripe network

### Categorical Features and Embeddings

Many features are categorical rather than numerical (e.g., merchant, card issuing bank, user country). For these features, [[embeddings]] provide a powerful approach:

**Embeddings** represent categorical values as vectors of coordinates, capturing similarity relationships:

| Entity | Dimension 1 | Dimension 2 | Dimension 3 |
|--------|-------------|-------------|-------------|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

**Advantages of embeddings:**
- Similar merchants have similar embeddings (measured by [[cosine distance]])
- Models can transfer learnings across similar entities
- Fraud patterns identified in one geographic region can be automatically applied to similar regions
- Enables models to adapt to new merchants without explicit retraining

### Infrastructure Requirements

Even conceptually simple features require substantial infrastructure:

- **Distributed computing**: [[Hadoop]] jobs to compute historical feature values
- **Optimization**: Probabilistic data structures to handle memory constraints
- **Real