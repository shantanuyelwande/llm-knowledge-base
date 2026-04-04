from pathlib import Path

# Example raw document for testing
EXAMPLE_AI_PAPER = """# Attention is All You Need

## Overview
The Transformer architecture represents a significant shift in deep learning, moving away from recurrent neural networks toward a purely attention-based approach.

## Key Concepts

### Self-Attention Mechanism
The self-attention mechanism allows the model to relate different positions of a single sequence. This computed attention output is a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function.

### Multi-Head Attention
Instead of performing a single attention function with d_model-dimensional keys, values and queries, it is benefitial to linearly project the queries, keys and values h times with different learned linear projections to d_k, d_k and d_v dimensions respectively.

### Position-wise Feed-Forward Networks
In addition to attention sub-layers, each of the layers contains a fully connected feed-forward network, which is applied to each position separately and identically.

## Architecture Details

The Transformer consists of an encoder and decoder. The encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence of continuous representations z = (z1, ..., zn).

Given z, the decoder then generates an output sequence of symbols (y1, ..., ym) one element at a time.

## Results

The Transformer model significantly outperformed recurrent neural networks (RNNs) on several benchmarks:
- WMT 2014 English-to-German translation
- WMT 2014 English-to-French translation
- English constituency parsing

## Impact

This architecture has become foundational for modern large language models, including BERT, GPT, and Claude.

## References

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). 
Attention is all you need. Advances in neural information processing systems, 30.
"""

EXAMPLE_ML_BASICS = """# Machine Learning Fundamentals

## What is Machine Learning?

Machine learning is a subset of artificial intelligence (AI) that enables systems to learn and improve from experience without being explicitly programmed.

## Types of Machine Learning

### Supervised Learning
In supervised learning, the model is trained on labeled data. The training data includes both input features and target labels.

Examples:
- Regression: predicting continuous values
- Classification: predicting discrete categories

### Unsupervised Learning
Unsupervised learning works with unlabeled data, finding hidden patterns or structures.

Examples:
- Clustering: grouping similar data points
- Dimensionality reduction: finding lower-dimensional representations

### Reinforcement Learning
The model learns through interaction with an environment, receiving rewards or penalties for actions.

## Key Concepts

### Training and Testing
Data is typically split into training and testing sets to evaluate model performance on unseen data.

### Feature Engineering
The process of selecting and transforming raw data into meaningful features for machine learning models.

### Model Evaluation
Common metrics include accuracy, precision, recall, F1-score, and AUC-ROC for classification tasks.

## Common Algorithms

- Linear Regression
- Logistic Regression  
- Decision Trees
- Random Forests
- Support Vector Machines (SVM)
- Neural Networks
- K-Means Clustering

## Best Practices

1. Start with simple models
2. Use cross-validation for robust evaluation
3. Feature scaling and normalization
4. Monitor for overfitting and underfitting
5. Document your experiments
"""

def create_example_data():
    """Create example data files for testing"""
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Create example files
    (raw_dir / "attention-is-all-you-need.md").write_text(EXAMPLE_AI_PAPER)
    (raw_dir / "ml-fundamentals.md").write_text(EXAMPLE_ML_BASICS)
    
    print(f"✓ Created example data in {raw_dir}")
    print(f"  - attention-is-all-you-need.md")
    print(f"  - ml-fundamentals.md")
    
    return raw_dir


if __name__ == "__main__":
    create_example_data()
