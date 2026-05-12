---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-12T05:45:01.544908
raw_file_updated: 2026-05-12T05:45:01.544908
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-12T05:45:01.544908
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection

## Summary

This comprehensive guide explains how [[Stripe Radar]], a machine learning-based fraud prevention solution, leverages the [[Stripe network]] to detect and prevent online credit card fraud. It covers fundamental concepts of [[machine learning]], evaluation metrics for fraud detection systems, and practical approaches to balancing false positives and false negatives in fraud prevention strategies.

---

## Overview

Online payment fraud costs businesses over $20 billion annually, with the true cost to businesses significantly higher when accounting for operational expenses, network fees, and customer churn. [[Stripe Radar]] is a machine learning solution fully integrated within the Stripe platform that uses data from hundreds of billions of dollars in payments processed across the Stripe network each year to accurately detect fraud and adapt to emerging trends.

This guide provides:
- An introduction to online credit card fraud mechanisms
- An explanation of how machine learning techniques apply to fraud detection
- Methods for evaluating fraud detection model performance
- Practical strategies for deploying and maintaining machine learning models
- Tools and approaches for optimizing fraud prevention outcomes

---

## Table of Contents

1. [Online Credit Card Fraud](#online-credit-card-fraud)
2. [Stripe Radar and the Stripe Network](#stripe-radar-and-the-stripe-network)
3. [Machine Learning Fundamentals](#machine-learning-fundamentals)
4. [Feature Engineering](#feature-engineering)
5. [Model Evaluation](#model-evaluation)
6. [Model Deployment and Operations](#model-deployment-and-operations)
7. [Fraud Prevention Strategy](#fraud-prevention-strategy)

---

## Online Credit Card Fraud

### Definition and Mechanisms

A payment is considered fraudulent when the cardholder has not authorized the charge. When a fraudster uses a stolen card number that hasn't been reported, the payment may process successfully. The cardholder later discovers the unauthorized transaction and files a dispute (also called a "chargeback") with their bank.

Businesses can challenge chargebacks by submitting evidence of valid payment, but for [[card-not-present transactions]], if networks determine the transaction was genuinely fraudulent, the cardholder wins and the business bears the loss of goods plus associated fees.

### False Positives vs. False Negatives

The core challenge in fraud prevention involves managing two competing risks:

**False Negatives (Missed Fraud)**
- Occur when the system fails to detect fraudulent transactions
- Cost to business: original transaction amount + chargeback fees + elevated network fees + operational costs for dispute review
- Excessive chargebacks can result in network monitoring programs, leading to higher costs or payment processing restrictions

**False Positives (False Declines)**
- Occur when legitimate customers are prevented from making purchases
- Cost to business: lost revenue + reputational damage
- Research shows 33% of consumers won't return to a retailer after experiencing a false decline

### Trade-Off Analysis

There is an inherent trade-off between preventing fraud (reducing false negatives) and approving legitimate transactions (reducing false positives). Businesses must balance these based on:

- **Profit margins**: Low-margin businesses (e.g., food sales) require stricter fraud prevention because each fraudulent transaction costs many legitimate sales to offset. High-margin businesses (e.g., SaaS) may tolerate more fraud to avoid blocking legitimate customers.
- **Growth profile**: Different business models have different sensitivities to fraud costs vs. customer friction
- **Industry factors**: Vertical and operational considerations specific to the business type

---

## Stripe Radar and the Stripe Network

### How Stripe Radar Works

[[Stripe Radar]] is Stripe's fraud prevention solution powered by [[adaptive machine learning]], developed through years of data science and infrastructure work. The system:

- Evaluates every transaction for fraud risk
- Blocks high-scoring payments automatically
- Provides [[Radar for Fraud Teams]] tools for custom actions and manual intervention

### Network Effects and Data Advantages

Stripe's position as a payment processor creates significant advantages for fraud detection:

**Scale and Pattern Recognition**
- Processes hundreds of billions in payments annually from millions of businesses
- Interacts with thousands of partner banks globally
- Can identify fraud signals and patterns earlier than smaller networks

**Card History Data**
- 90% of cards used on the Stripe network have been seen multiple times
- Provides rich historical data for assessing legitimate vs. fraudulent use patterns
- Enables learning from previous encounters across the entire network

**Integrated Data Flow**
- Receives "ground truth" data directly from the Stripe payment flow—no separate integration required
- Accesses timely, accurate data from card networks and issuers
- Eliminates engineering overhead and manual labeling that traditional fraud solutions require

### Advantages Over Traditional Solutions

Unlike external fraud prevention services, Radar:
- Requires no engineering integration or data transmission setup
- Eliminates the need for payment labeling workflows
- Works immediately upon activation
- Continuously improves from network data without additional merchant effort

---

## Machine Learning Fundamentals

### What is Machine Learning?

[[Machine learning]] refers to techniques for processing large datasets to produce predictive models. In fraud detection, machine learning predicts whether a transaction will result in a fraud dispute based on transaction features.

### The Prediction Problem

Machine learning models predict an **output variable** (fraudulent: yes/no) based on **input variables** (features), such as:
- Country where card was issued
- Number of distinct countries card was used from in past 24 hours
- Transaction amount
- IP address location
- Time zone of device vs. UTC

### Training Data and Models

Models are trained on historical records containing both input features and actual outcomes. A simplified example:

| Amount (USD) | Card Country | Countries Used (24h) | Fraudulent? |
|---|---|---|---|
| $10.00 | US | 1 | No |
| $10.00 | CA | 2 | No |
| $30.00 | US | 1 | Yes |
| $99.00 | CA | 1 | Yes |

The machine learning algorithm produces a model—such as a [[decision tree]]—that learns patterns from this data. When a new transaction arrives, the model traverses the decision tree based on transaction features to reach a "leaf" containing similar historical transactions. The probability of fraud is calculated as: (fraudulent transactions in leaf) / (total transactions in leaf).

### Model Complexity and Techniques

While [[decision trees]] are intuitive and easy to visualize, industrial fraud detection uses more sophisticated approaches:

**Traditional Methods**
- [[Linear regression]]
- [[Random forests]]
- Effective for most business applications

**Advanced Techniques**
- [[Neural networks]] and [[deep learning]]
- Inspired by brain neuron architecture
- Require large datasets to realize full advantages
- Responsible for breakthroughs like AlphaFold protein folding predictions

Stripe leverages its network scale to employ cutting-edge neural network approaches, improving Radar's machine learning performance by over 20% year-over-year while maintaining low false positive rates.

---

## Feature Engineering

### What is Feature Engineering?

[[Feature engineering]] is one of the most involved aspects of industrial machine learning. It consists of:

1. **Feature formulation**: Creating features with predictive value based on domain knowledge of fraud patterns
2. **Feature engineering**: Making feature values available for both model training and real-time production evaluation

### Developing Predictive Features

Data scientists develop feature ideas through:
- Intuition about fraud patterns
- Analysis of thousands of fraud cases
- Domain expertise in payment systems

Examples of effective features:
- Whether payment originates from previously seen IP addresses for that card
- Difference between device time and Coordinated Universal Time (UTC)
- Count of countries where card was successfully authorized
- IP address commonality with historical card usage patterns

### Computing Features at Scale

Once a feature is identified, its historical values must be computed for all training data. For example, computing "two most frequent IP addresses from preceding payments" requires:

- Processing all historical Stripe payments
- Using distributed computing systems like [[Hadoop]]
- Optimizing with space-saving probabilistic data structures
- Managing memory and computational constraints

### Embeddings for Categorical Features

[[Embeddings]] are learned representations for categorical variables (merchant, issuing bank, country, etc.). Rather than hard-coding feature values, embeddings allow models to learn coordinates for each category:

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|---|---|---|---|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

**Advantages of Embeddings:**
- Similar merchants have similar embeddings (measured by [[cosine distance]])
- Models transfer learnings between similar merchants
- Fraud patterns learned in one geography automatically apply to similar geographies
- Enables pattern recognition