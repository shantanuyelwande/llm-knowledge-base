---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:17:35.310995
raw_file_updated: 2026-05-02T05:17:35.310995
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:17:35.310995
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Prevention

## Summary

This comprehensive guide explains how [[Stripe Radar]], a machine learning-based fraud detection system, uses data from the Stripe network to identify and prevent online credit card fraud. It covers fundamental machine learning concepts, model evaluation techniques, and practical strategies for balancing fraud prevention with customer experience. The guide addresses the inherent trade-off between false negatives (missed fraud) and false positives (legitimate transactions blocked), and explains how businesses can optimize their fraud prevention strategies based on their specific margins and risk profiles.

---

## Table of Contents

1. [Overview](#overview)
2. [Online Credit Card Fraud](#online-credit-card-fraud)
3. [Stripe Radar and Network Effects](#stripe-radar-and-network-effects)
4. [Machine Learning Fundamentals](#machine-learning-fundamentals)
5. [Feature Engineering](#feature-engineering)
6. [Model Evaluation](#model-evaluation)
7. [Model Deployment](#model-deployment)
8. [Fraud Prevention Strategy](#fraud-prevention-strategy)

---

## Overview

The rapid growth of e-commerce has created a corresponding surge in online payment fraud, with global costs exceeding $20 billion annually. Beyond direct losses, fraud imposes substantial indirect costs through operational expenses, network fees, and customer churn. Traditional rule-based fraud detection systems, while straightforward to implement, often generate excessive false positives that damage customer experience and business revenue.

[[Machine Learning]] offers a more sophisticated alternative, enabling fraud detection systems to identify nuanced patterns and adapt to evolving fraud tactics. [[Stripe Radar]] represents a production-scale implementation of machine learning for fraud prevention, leveraging data from hundreds of billions of dollars in annual transactions processed across the Stripe network.

---

## Online Credit Card Fraud

### Definition and Mechanics

A payment is fraudulent when the cardholder has not authorized the charge. Common scenarios include:

- **Stolen card numbers**: Fraudsters use card credentials without the cardholder's knowledge
- **Chargeback disputes**: When cardholders discover unauthorized charges, they file disputes (chargebacks) with their banks
- **Liability**: For card-not-present transactions, businesses bear the loss if networks determine the charge was fraudulent

### Cost Structure of Fraud

When a fraudulent transaction is not prevented, businesses incur multiple costs:

- Original transaction amount
- Chargeback fees (bank processing costs)
- Elevated network fees due to dispute history
- Operational costs for dispute investigation
- Risk of enrollment in chargeback monitoring programs, which can increase costs or restrict payment acceptance

### The False Negative vs. False Positive Trade-off

Understanding two critical error types is essential for fraud prevention strategy:

**False Negatives (Missed Fraud)**
- Definition: Fraudulent transactions incorrectly classified as legitimate
- Business impact: Direct losses plus chargeback fees and elevated operational costs
- Risk: Excessive chargebacks can trigger network monitoring programs

**False Positives (False Declines)**
- Definition: Legitimate transactions incorrectly blocked
- Business impact: Lost revenue and customer dissatisfaction
- Research finding: 33% of consumers report they won't shop again after experiencing a false decline

### Business-Specific Trade-offs

The optimal balance between false negatives and false positives depends on business fundamentals:

**High-Margin Businesses** (e.g., SaaS)
- Can tolerate higher fraud rates
- Should minimize false positives to preserve revenue
- Cost of losing one legitimate customer may exceed fraud losses

**Low-Margin Businesses** (e.g., food delivery)
- Cannot absorb fraud losses across many transactions
- May justify stricter blocking policies
- May accept more false positives to prevent fraud

---

## Stripe Radar and Network Effects

### Overview

[[Stripe Radar]] is Stripe's integrated fraud prevention solution powered by adaptive machine learning. It evaluates every transaction for fraud risk and takes appropriate action, with high-risk payments blocked automatically and additional tools available through [[Radar for Fraud Teams]] for custom interventions.

### Network Advantages

Stripe's scale creates significant competitive advantages in fraud detection:

**Data Volume and Diversity**
- Processes hundreds of billions in annual payments from millions of businesses
- Interacts with thousands of partner banks globally
- Provides early visibility into emerging fraud patterns across diverse merchant categories

**Card History Intelligence**
- 90% of cards used on the Stripe network have been observed multiple times
- Enables rich historical context for fraud assessment
- Allows detection of patterns that single-merchant systems cannot identify

**Automatic Data Integration**
- Fraud labels derived directly from the Stripe payment flow
- Receives ground truth data from card networks and issuers
- Eliminates manual labeling and engineering integration work required by competing solutions

### Key Advantage: Works Out of the Box

Unlike competing fraud solutions, Radar requires no:
- Engineering integration to send payment events
- Manual transaction labeling
- Custom data pipeline development

This reduces implementation friction and ensures models benefit from accurate, timely fraud labels automatically.

---

## Machine Learning Fundamentals

### Core Concept

[[Machine Learning]] refers to techniques for extracting predictive patterns from large datasets. In fraud detection, the goal is to predict whether a transaction is fraudulent based on observable transaction properties.

### Basic Components

**Inputs (Features)**
- Observable transaction properties that may indicate fraud
- Examples: card issuing country, transaction amount, IP address, merchant category
- Modern fraud models use hundreds of features

**Output (Target/Label)**
- Binary classification: fraudulent (true) or legitimate (false)
- Represented as boolean values

**Training Data**
- Historical transactions with known fraud status
- Each record contains feature values and the fraud label
- Used to develop predictive models

### Simple Example

Consider a minimal dataset:

| Amount (USD) | Card Country | Countries Used (24h) | Fraud? |
|---|---|---|---|
| $10 | US | 1 | No |
| $10 | CA | 2 | No |
| $10 | CA | 1 | No |
| $10 | US | 1 | Yes |
| $30 | US | 1 | Yes |
| $99 | CA | 1 | Yes |

A decision tree model might learn rules like:
- If amount > $25 and card country = US → likely fraudulent
- If countries used in 24h > 1 → investigate further

### How Machine Learning Works

#### Step 1: Obtain Training Data

Assemble historical records with:
- **Feature vectors**: Collections of input properties for each transaction
- **Labels**: Known fraud outcomes for each transaction
- **Sufficient scale**: Hundreds of thousands to millions of examples

#### Step 2: Train a Model

Use machine learning algorithms to discover patterns in training data. The model learns to:
- Identify which features are predictive
- Determine how features combine to indicate fraud
- Assign probability scores rather than binary classifications

**Output**: A fraud probability score (e.g., 65% chance of fraud, 35% chance of legitimate)

#### Step 3: Evaluate Performance

Test the model on held-out data to measure effectiveness and identify performance trade-offs.

### Machine Learning Techniques

**Traditional Approaches** (suitable for most business applications)
- Linear regression
- Decision trees
- Random forests

**Advanced Techniques** (require very large datasets)
- [[Neural Networks]] and [[Deep Learning]]
- Inspired by brain architecture
- Responsible for recent breakthroughs (e.g., protein structure prediction)
- Stripe's scale enables effective use of these techniques
- Year-over-year performance improvements: >20%

---

## Feature Engineering

### Definition

Feature engineering consists of two interconnected activities:

1. **Conceptual Design**: Identifying properties that have predictive value based on domain expertise
2. **Implementation**: Making feature values available for both model training and real-time production inference

### The Art and Science of Feature Selection

#### Domain Expertise

Data scientists develop feature ideas through:
- Examination of thousands of fraud cases
- Understanding of payment system mechanics
- Intuition about cardholder behavior patterns

#### Surprising Effective Features

Not all useful features are intuitive. Examples of effective fraud indicators:
- Time zone difference between user device and UTC
- Count of distinct countries where card was successfully authorized
- Frequency of IP address usage for a specific card
- Merchant similarity patterns

#### Implementation Challenges

Creating a feature requires:
- Computing historical values for all training data
- Often using distributed computing systems (e.g., Hadoop)
- Optimizing for performance using specialized data structures
- Maintaining real-time availability for production inference

### Advanced Technique: Embeddings

#### Concept

[[Embeddings]] represent categorical values as vectors in multi-dimensional space, allowing models to capture similarity relationships between categories.

#### How Embeddings Work

Rather than treating categorical values (merchants, countries, banks) as isolated categories, embeddings place similar entities close together in vector space:

| Entity | Dimension 1 | Dimension