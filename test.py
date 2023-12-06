import numpy as np

def sigmoid(x, alpha=1):
    return 1 / (1 + np.exp(-alpha * x))

# 示例得分
scores = np.array([0.2, 0.5, 0.8])

# 调整参数 alpha，控制拉大程度
alpha = 5

# 对得分进行变换
transformed_scores = sigmoid(scores, alpha)

print("Original Scores:", scores)
print("Transformed Scores:", transformed_scores)