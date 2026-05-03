---
title: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430
source_file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
source_url: https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-03T05:37:25.492121
raw_file_updated: 2026-05-03T05:37:25.492121
version: 1
sources:
  - file: stripe-com-in-guides-primer-on-machine-learning-for-fraud-pro-1777643430.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-03T05:37:25.492121
tags: []
related_topics: []
backlinked_by: []
---
# Machine Learning for Fraud Detection

## Summary

This article provides a comprehensive guide to [[machine learning]] applications in [[fraud detection]], specifically focusing on [[Stripe Radar]], a machine learning-based fraud prevention solution. It covers the fundamentals of [[online credit card fraud]], [[machine learning]] techniques used in fraud prevention, methods for evaluating model performance, and best practices for deploying fraud detection systems in production environments.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Online Credit Card Fraud](#online-credit-card-fraud)
3. [Stripe Radar and Network Effects](#stripe-radar-and-network-effects)
4. [Machine Learning Fundamentals](#machine-learning-fundamentals)
5. [Model Evaluation](#model-evaluation)
6. [Deployment and Operations](#deployment-and-operations)
7. [Optimization Strategies](#optimization-strategies)
8. [Key Concepts](#key-concepts)

---

## Introduction

The rapid acceleration of [[e-commerce]] has created a corresponding surge in [[online fraud]]. Worldwide, fraud costs businesses an estimated $20 billion annually, with the true cost to businesses being substantially higher when accounting for operational expenses, network fees, and [[customer churn]]. Sophisticated fraudsters continuously develop new methods to exploit weaknesses in payment systems, making fraud detection increasingly challenging.

[[Stripe Radar]] is a machine learning-based [[fraud prevention]] solution fully integrated within the Stripe platform. By leveraging data from hundreds of billions of dollars in payments processed annually across the [[Stripe network]], Radar can accurately detect fraud and adapt to emerging trends, enabling businesses to grow while minimizing fraud losses.

---

## Online Credit Card Fraud

### Definition and Mechanics

A payment is considered fraudulent when the cardholder does not authorize the charge. Common scenarios include:

- A fraudster using a stolen [[credit card]] number that hasn't been reported
- Unauthorized charges that are later discovered by the cardholder
- [[Chargeback|Chargebacks]] filed when cardholders dispute unauthorized transactions

### Business Impact

When a [[chargeback]] occurs, businesses face multiple financial consequences:

- Loss of the original transaction amount
- [[Chargeback fees]] (costs associated with the bank reversing the card payment)
- Elevated [[network fees]] resulting from the dispute
- Increased operational costs for reviewing and disputing charges
- Risk of enrollment in [[chargeback monitoring programs]], which can lead to higher costs or payment processing restrictions

### The False Positive and False Negative Trade-off

Traditional [[rule-based fraud detection]] systems use hard-coded rules (such as blocking all cards used abroad), which often result in blocking many legitimate transactions. [[Machine learning]] can detect more nuanced patterns to help maximize revenue while managing fraud risk.

#### False Negatives

A **false negative** occurs when the system fails to detect fraud. In fraud detection, this means a fraudulent transaction is not flagged. The business is responsible for:

- Original transaction amount
- [[Chargeback fees]]
- Higher network fees
- Increased operational costs
- Potential enrollment in chargeback monitoring programs

#### False Positives

A **false positive** (or **false decline**) occurs when a legitimate customer is prevented from completing a purchase. Research indicates that 33% of consumers will not shop again at a business after experiencing a false decline, resulting in both immediate revenue loss and long-term reputational damage.

### Business Considerations

The optimal balance between [[false positives]] and [[false negatives]] depends on business characteristics:

- **Low-margin businesses** (e.g., food e-commerce): Small margins mean fraudulent transactions are expensive relative to revenue. These businesses may employ broader fraud prevention measures.
- **High-margin businesses** (e.g., [[SaaS]]): Higher margins mean the lost revenue from blocking one legitimate customer may exceed the cost of increased fraud.

---

## Stripe Radar and Network Effects

### Overview

[[Stripe Radar]] is Stripe's comprehensive [[fraud prevention]] solution powered by [[adaptive machine learning]]. The system evaluates every transaction for fraud risk and takes appropriate action, with high-scoring payments blocked and additional actions available through [[Radar for Fraud Teams]].

### Network Advantages

Stripe's massive scale provides significant advantages in fraud detection:

- **Scale**: Stripe processes hundreds of billions in payments annually from millions of businesses, interacting with thousands of partner banks globally
- **Early signal detection**: This scale allows Stripe to identify fraud signals and patterns earlier than smaller networks
- **Rich historical data**: 90% of cards used on the Stripe network have been seen more than once, providing substantially richer data for fraud assessment
- **Automatic data collection**: Aggregate fraud-relevant data is collected automatically through the payments flow without requiring merchant integration

### Integration Advantages

Unlike traditional [[fraud prevention]] solutions, Radar is built directly into Stripe and requires minimal setup:

- **No engineering integration required**: Radar receives "ground truth" information directly from the Stripe payment flow
- **Automatic data access**: The system accesses timely and accurate data directly from card networks and issuers
- **Reduced operational burden**: Merchants do not need to manually label payments or maintain separate integrations
- **Immediate functionality**: Radar works out of the box without substantial upfront or ongoing investment

---

## Machine Learning Fundamentals

### Core Concepts

[[Machine learning]] refers to techniques for taking large amounts of data and producing models that predict outcomes. In fraud detection, the goal is to predict the likelihood that a charge will result in a fraud dispute.

#### The Prediction Problem

Machine learning models predict an output variable based on input variables:

- **Output variable**: Boolean value indicating whether a payment is fraudulent (true/false)
- **Input variables** (features): Characteristics such as card issuing country, number of distinct countries where the card was used in the past 24 hours, transaction amount, etc.

#### Training Data

Models are trained on historical data containing:

- **Feature vectors**: Collections of input properties for each transaction
- **Labels** (targets): Known output values (whether each transaction was actually fraudulent)
- **Examples**: Historical records with both features and labels

### How Machine Learning Works

The machine learning process involves several key steps:

#### 1. Data Collection and Feature Definition

Before building a fraud detection model, practitioners must:

- Obtain historical data with examples of fraudulent and legitimate transactions
- Define **features**: Input properties that could be useful for predicting fraud
- Create **feature vectors**: Collections of features for each transaction

In practice, fraud detection models often use hundreds or thousands of features, with most being aggregates computed across the Stripe network.

#### 2. Model Training

Given training data, machine learning methods produce predictive models. Most classifiers output probabilities rather than simple class labels. For example, a fraud classifier might assess that a payment has a 65% probability of being fraudulent and 35% probability of being legitimate.

**Common techniques** include:

- [[Linear regression]]
- [[Decision trees]]
- [[Random forests]]
- [[Neural networks]] and [[deep learning]]

**Advanced approaches**: Sophisticated techniques like [[neural networks]] and [[deep learning]], inspired by neural architecture in the brain, have driven major advances in machine learning. These techniques show particular advantages when trained on very large datasets. Stripe's network scale enables effective use of these cutting-edge approaches, with new models improving Radar's performance by over 20% year-over-year.

### Feature Engineering

[[Feature engineering]] is one of the most involved aspects of industrial machine learning, consisting of two parts:

#### 1. Feature Formulation

Data scientists develop features with predictive value based on extensive domain knowledge. Examples include:

- Whether a card payment originates from a common IP address for that card
- The difference between device time and Coordinated Universal Time (UTC)
- The count of countries where the card was successfully authorized
- Historical IP address patterns for specific cards

#### 2. Feature Implementation

Once formulated, features must be computed for:

- **Historical data**: For model training
- **Production**: For real-time fraud scoring

This engineering work often requires:

- Distributed computing frameworks (e.g., [[Hadoop]])
- Optimization using [[probabilistic data structures]]
- Dedicated infrastructure and established workflows

### Embeddings

Not all features are manually engineered; some are learned by models through [[embeddings]].

#### Definition

[[Embeddings]] represent categorical values (such as merchant identity or card issuing country) as coordinates in a high-dimensional space. Similar entities have similar embeddings as measured by [[cosine distance]].

#### Example

| Entity | Coordinate 1 | Coordinate 2 | Coordinate 3 |
|--------|-------------|-------------|-------------|
| Uber | 2.34 | 1.1 | -3.5 |
| Lyft | 2.1 | 1.2 | -2.0 |
| Slack | 7.0 | -2.0 | 1.0 |

Uber and Lyft have similar embeddings (reflecting their similarity as ride-sharing services), while Slack differs