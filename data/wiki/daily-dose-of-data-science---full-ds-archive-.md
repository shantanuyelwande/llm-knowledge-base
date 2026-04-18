---
title: Daily Dose of Data Science - Full DS Archive 
source_file: Daily Dose of Data Science - Full DS Archive .pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:19:42.064073
raw_file_updated: 2026-04-17T20:19:42.064073
version: 1
sources:
  - file: Daily Dose of Data Science - Full DS Archive .pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:19:42.064073
tags: []
related_topics: []
backlinked_by: []
---
# Daily Dose of Data Science: Complete Archive

## Overview

The **Daily Dose of Data Science** is a comprehensive collection of machine learning, statistics, and data science concepts compiled by Avi Chawla. This archive covers fundamental and advanced topics spanning deep learning, classical machine learning, statistical inference, data engineering, visualization, and software engineering best practices relevant to data science professionals.

## Summary

This wiki documents over 200 distinct data science topics organized into major domains: [[Machine Learning Models and Algorithms]], [[Deep Learning and Neural Networks]], [[Statistical Methods and Inference]], [[Data Processing and Engineering]], [[Data Visualization]], [[Software Engineering for Data Science]], and [[Production ML Systems]]. The material emphasizes practical understanding, intuitive explanations, and real-world applications rather than purely theoretical treatment.

---

## Core Domains

### Machine Learning Fundamentals

#### Model Training and Optimization

- **[[Transfer Learning]]** - Training neural networks on related tasks to improve performance on tasks with limited data
- **[[Fine-tuning]]** - Updating weights of pre-trained models to adapt them to new tasks
- **[[Multi-task Learning]]** - Training models simultaneously on multiple related tasks with shared representations
- **[[Federated Learning]]** - Training models on distributed private data without centralizing it
- **[[Momentum Optimization]]** - Technique to speed up model training by considering moving averages of past gradients
- **[[Mixed Precision Training]]** - Using lower precision (float16) with float32 to accelerate training while maintaining accuracy
- **[[Gradient Checkpointing]]** - Reducing memory usage during training by recomputing activations instead of storing them
- **[[Gradient Accumulation]]** - Simulating larger batch sizes by accumulating gradients across multiple mini-batches

#### Regularization and Generalization

- **[[Label Smoothing]]** - Reducing model overconfidence by distributing probability mass across all classes
- **[[Dropout Regularization]]** - Preventing overfitting by randomly zeroing neurons during training with proper scaling
- **[[DropBlock]]** - Dropping contiguous regions of features in CNNs instead of individual pixels
- **[[L2 Regularization and Ridge Regression]]** - Adding penalty term to eliminate multicollinearity and reduce overfitting
- **[[Early Stopping]]** - Halting training when validation performance plateaus

#### Loss Functions and Metrics

- **[[Focal Loss]]** - Addressing class imbalance by downweighting easy examples in classification
- **[[Binary Cross Entropy]]** - Standard loss function for binary classification tasks
- **[[Squared Error Loss and Maximum Likelihood]]** - Theoretical foundation for linear regression loss functions
- **[[Top-k Accuracy]]** - Measuring if correct label appears in top k predictions for multiclass problems

### Classical Machine Learning

#### Tree-Based Models

- **[[Decision Trees]]** - Interpretable models that recursively split data based on feature thresholds
- **[[Decision Tree Pruning]]** - Preventing overfitting through cost-complexity pruning
- **[[Random Forests]]** - Ensemble of decision trees with bagging for improved generalization
- **[[Random Forests with Random Patches]]** - Training random forests on large datasets using data sampling
- **[[Out-of-Bag Validation]]** - Evaluating random forests using samples not used in bootstrap samples
- **[[Tree Compression to Single Tree]]** - Condensing random forest predictions into interpretable single decision tree
- **[[Decision Tree Matrix Operations]]** - Representing tree inference as matrix operations for GPU acceleration
- **[[AdaBoost]]** - Iterative boosting algorithm that reweights misclassified samples
- **[[Gradient Boosting]]** - Sequential ensemble learning where models learn from previous model mistakes

#### Regression Models

- **[[Linear Regression and OLS]]** - Ordinary least squares regression and why squared error is optimal
- **[[Poisson Regression]]** - Generalized linear model for count data following Poisson distributions
- **[[Generalized Linear Models]]** - Family of models extending linear regression to non-normal distributions
- **[[Zero-Inflated Regression]]** - Combining classification and regression for datasets with excess zeros
- **[[Huber Regression]]** - Robust regression less sensitive to outliers than standard linear regression

#### Distance and Similarity

- **[[k-Nearest Neighbors]]** - Instance-based learning using nearest neighbors for prediction
- **[[Distance-Weighted kNN]]** - Weighting neighbors by distance for more robust predictions
- **[[Dynamic k Selection for kNN]]** - Adapting k parameter based on class representation in neighbors
- **[[Approximate Nearest Neighbors Search]]** - Using inverted file indices to speed up neighbor search
- **[[Kernel Methods and the Kernel Trick]]** - Computing dot products in high-dimensional spaces without explicit projection
- **[[Polynomial Kernel]]** - Computing dot products for polynomial feature expansions
- **[[RBF Kernel]]** - Mapping data to infinite-dimensional space for complex decision boundaries
- **[[Support Vector Machines]]** - Maximum margin classifiers using kernel methods

#### Clustering

- **[[k-Means Clustering]]** - Partitioning data into k clusters by minimizing within-cluster variance
- **[[Breathing k-Means]]** - Enhanced k-means with dynamic centroid addition and removal
- **[[Mini-Batch k-Means]]** - Scalable k-means for large datasets using mini-batch updates
- **[[Gaussian Mixture Models]]** - Probabilistic clustering using mixture of Gaussian distributions
- **[[DBSCAN]]** - Density-based clustering robust to arbitrary cluster shapes
- **[[DBSCAN++]]** - Faster DBSCAN using subset density estimation
- **[[HDBSCAN]]** - Hierarchical DBSCAN handling varying cluster densities
- **[[Clustering Evaluation Metrics]]** - Silhouette coefficient, Calinski-Harabasz index, DBCV

#### Dimensionality Reduction

- **[[Principal Component Analysis (PCA)]]** - Linear dimensionality reduction preserving maximum variance
- **[[Kernel PCA]]** - Non-linear dimensionality reduction using kernel trick
- **[[PCA for Visualization]]** - Proper use of PCA for 2D visualization with cumulative explained variance
- **[[t-SNE]]** - Non-linear visualization technique using Student t-distribution for well-separated clusters
- **[[t-SNE Hyperparameters]]** - Understanding perplexity and avoiding misinterpretation of t-SNE results
- **[[SNE vs t-SNE]]** - Differences between standard SNE and improved t-SNE algorithm
- **[[Accelerated t-SNE Implementations]]** - GPU-accelerated tSNE-CUDA and multi-threaded openTSNE
- **[[PCA vs t-SNE]]** - Comparing linear (PCA) and non-linear (t-SNE) dimensionality reduction

### Deep Learning and Neural Networks

#### Architectures and Components

- **[[Neural Network Layers]]** - Understanding linear transformations and activation functions
- **[[Activation Functions]]** - ReLU, Sigmoid, Tanh enabling non-linear learning
- **[[Batch Normalization]]** - Normalizing layer inputs for faster training and better generalization
- **[[Convolutional Neural Networks]]** - Specialized architecture for image data using local connectivity
- **[[Recurrent Neural Networks]]** - Sequential models with memory for time-series data
- **[[Transformers]]** - Attention-based architecture dominant in NLP and multimodal models

#### Knowledge Transfer and Compression

- **[[Knowledge Distillation]]** - Training smaller student models to mimic larger teacher models
- **[[Model Pruning]]** - Removing neurons contributing minimally to predictions
- **[[LoRA Fine-tuning]]** - Efficient fine-tuning of large models using low-rank decomposition
- **[[LoRA Variants]]** - LoRA-FA, VeRA, Delta-LoRA, LoRA+ improvements
- **[[Retrieval Augmented Generation (RAG)]]** - Augmenting LLM knowledge with external document retrieval

#### Training Techniques

- **[[Multi-GPU Training Strategies]]** - Data parallelism, model parallelism, tensor parallelism, pipeline parallelism
- **[[Distributed Training with PyTorch]]** - Scaling training across multiple GPUs and nodes
- **[[Hyperparameter Optimization]]** - Bayesian optimization for efficient hyperparameter tuning

#### Specific Challenges

- **[[Data Shuffling in Training]]** - Importance of shuffling mini-batches to prevent pattern learning from order
- **[[Neural Network Linear Separability]]** - How networks transform data to become linearly separable
- **[[Double