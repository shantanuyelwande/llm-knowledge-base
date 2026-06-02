---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-02T06:49:08.975113
raw_file_updated: 2026-06-02T06:49:08.975113
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-02T06:49:08.975113
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection

## Summary

This article provides a comprehensive guide to understanding how [[machine learning]] is applied to online payment fraud detection, with a focus on [[Stripe Radar]], Stripe's machine learning-based fraud prevention solution. It covers the fundamentals of machine learning, evaluation metrics for fraud detection systems, deployment challenges, and practical strategies for optimizing fraud prevention performance.

---

## Introduction

The rapid acceleration of e-commerce has created a corresponding surge in online payment fraud, costing businesses an estimated $20 billion annually. Beyond direct losses, fraud imposes significant indirect costs through operational expenses, network fees, and customer churn. [[Stripe Radar]] represents a modern approach to this challenge—a machine learning system that leverages data from hundreds of billions of dollars in payments processed across the Stripe network to detect fraud accurately and adapt to emerging threats.

This guide explains the machine learning techniques used in fraud prevention, how to evaluate the effectiveness of fraud detection systems, and how businesses can optimize their fraud prevention strategies through a combination of automated models, custom rules, and manual review processes.

---

## Understanding Online Credit Card Fraud

### What Constitutes Fraud

A payment is considered fraudulent when the cardholder has not authorized the charge. Common scenarios include:

- A fraudster making a purchase with a stolen card number that hasn't been reported
- The cardholder later disputing the transaction with their bank through a [[chargeback]]

### The Chargeback Process

When a cardholder disputes a transaction, the business can challenge the chargeback by submitting evidence of validity. However, for [[card-not-present transactions]], if networks determine the payment was genuinely fraudulent, the cardholder wins and the business bears the loss of goods plus associated fees.

### Historical Approaches vs. Machine Learning

Historically, businesses relied on hard-coded rules (e.g., "block all cards used abroad") to prevent fraud. While simple to implement, these approaches often block many legitimate transactions, resulting in poor customer experience. [[Machine learning]] enables detection of more nuanced patterns that better distinguish between legitimate and fraudulent activity while maximizing revenue.

---

## The Trade-off Between False Positives and False Negatives

Understanding the cost-benefit analysis of fraud prevention is crucial for optimization.

### False Negatives (Missed Fraud)

A false negative occurs when the system fails to detect fraudulent activity. Costs include:

- Original transaction amount plus [[chargeback]] fees
- Higher network fees resulting from disputes
- Increased operational costs for reviewing and fighting disputes
- Risk of entering a network chargeback monitoring program, leading to higher costs or payment processing restrictions

### False Positives (False Declines)

A false positive occurs when a legitimate customer is incorrectly blocked from making a purchase. Consequences include:

- Immediate loss of gross profit on that transaction
- Reputational damage to the business
- Customer churn—research shows 33% of consumers won't shop again after a false decline

### Business-Specific Trade-offs

The optimal balance between false positives and false negatives depends on business characteristics:

- **Low-margin businesses** (e.g., food e-commerce): Each fraudulent transaction is expensive relative to profit per sale. These businesses may tolerate more false positives to prevent fraud.
- **High-margin businesses** (e.g., SaaS): Lost revenue from blocking legitimate customers may outweigh fraud losses. These businesses may accept more fraud to reduce false declines.

---

## Stripe Radar and the Stripe Network

### Overview

[[Stripe Radar]] is Stripe's adaptive machine learning-based fraud prevention solution. It evaluates every transaction for fraud risk and takes appropriate action—blocking high-risk payments while enabling [[Radar for Fraud Teams]] to specify custom interventions.

### Network Advantages

Stripe's position as a payment processor provides significant advantages:

- **Scale**: Processing hundreds of billions in payments annually from millions of businesses
- **Early signal detection**: Stripe often identifies fraud patterns before smaller networks
- **Rich data**: Aggregate data from all Stripe transactions automatically improves fraud detection
- **Card history**: 90% of cards used on Stripe have been seen more than once, providing rich data for risk assessment

### Key Features

**Built-in integration**: Unlike third-party fraud solutions, Radar is integrated directly into Stripe and requires:
- No engineering work to send payment event data
- No manual labeling of transactions as fraudulent or legitimate
- Automatic access to timely, accurate data from card networks and issuers

---

## The Basics of Machine Learning

### What is Machine Learning?

[[Machine learning]] refers to techniques for using large amounts of historical data to produce models that predict outcomes. In fraud detection, the goal is to predict whether a payment will result in a fraud dispute based on input variables such as:

- Card issuing country
- Number of distinct countries where the card was used in the past 24 hours
- Transaction amount
- IP address of the transaction
- Merchant category

### Training Data and Features

Machine learning models are trained on historical records containing:

- **Input values** (called [[features]]): Properties of transactions that may predict fraud
- **Output values** (called [[labels]] or [[targets]]): Whether each transaction was actually fraudulent

A collection of input values for a given transaction is called a [[feature vector]]. While the example in this guide uses three features, production models typically use hundreds or thousands of features, with most being aggregates computed across the Stripe network.

### Model Output

Rather than outputting a simple yes/no classification, machine learning classifiers assign probabilities. For example, a fraud classifier might output: "This payment has a 65% chance of being fraudulent and a 35% chance of being legitimate."

### Machine Learning Techniques

Various techniques can be used to train models:

- **Traditional approaches**: [[Linear regression]], [[decision trees]], [[random forests]]
- **Advanced techniques**: [[Neural networks]] and [[deep learning]], inspired by brain architecture

While advanced techniques require very large datasets to show advantages, Stripe's network scale enables use of cutting-edge approaches. Recent model improvements have increased Radar's detection performance by over 20% year-over-year.

### Decision Trees Example

A simple decision tree might ask sequential questions:
1. Is the transaction amount > $25?
2. Is the card's country the same as the transaction country?
3. How many distinct countries used this card in the past day?

The model traverses these questions until reaching a leaf node, where the probability of fraud is calculated as: (fraudulent transactions in this leaf) / (total transactions in this leaf).

---

## Feature Engineering

### Overview

[[Feature engineering]] is one of the most involved aspects of industrial machine learning. It consists of two parts:

1. **Formulation**: Developing features with predictive value based on domain expertise
2. **Engineering**: Making feature values available for both model training and real-time production evaluation

### Developing Features

Data scientists develop feature ideas through:

- Domain knowledge of fraud patterns
- Examination of thousands of fraud cases
- Hypothesis testing about transaction properties

Examples of useful features include:
- Whether a payment originates from an IP address commonly associated with the card
- Difference between device time and UTC
- Count of countries where the card was successfully authorized

### Computing Feature Values

Once a feature is conceived, its historical values must be computed for all transactions in Stripe's history. This process:

- May require distributed computing (e.g., [[Hadoop]] jobs)
- Can be optimized using probabilistic data structures
- Requires dedicated infrastructure and established workflows

### Embeddings for Categorical Features

For categorical features (e.g., merchant, issuing bank, country), Stripe uses [[embeddings]]—learned numerical representations that capture similarity relationships.

**How embeddings work:**
- Each category (e.g., merchant) is represented as coordinates in a multi-dimensional space
- Similar merchants have similar embeddings (measured by [[cosine distance]])
- Models can transfer learnings from one merchant to similar merchants

**Example:**
| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|--------|-------------|-------------|-------------|
| Uber   | 2.34        | 1.1         | -3.5        |
| Lyft   | 2.1         | 1.2         | -2.0        |
| Slack  | 7.0         | -2.0        | 1.0         |

Uber and Lyft have similar embeddings, reflecting their business similarity, while Slack differs significantly.

**Advantages:**
- Fraud patterns identified in one geography can automatically be detected in similar geographies
- The system adapts to new fraud patterns without explicit retraining
- Enables algorithmic advances that stay ahead of shifting fraud patterns

---

## Evaluating Machine Learning Models

### Key Evaluation Metrics

#### Precision

**Definition**: The fraction of transactions flagged as fraud that are actually fraudulent.

**Formula**: Precision = (True Positives) / (True Positives + False Positives)

**Example**: If 6 transactions are flagged with P(fraud) > 