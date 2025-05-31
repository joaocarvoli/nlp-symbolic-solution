import matplotlib.pyplot as plt
import pandas as pd

def plot_sentiment_distribution(df: pd.DataFrame, sentiment_col: str, output_file: str = None):
    counts = df[sentiment_col].value_counts().reindex([-1, 0, 1], fill_value=0)
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(['Negative', 'Neutral', 'Positive'], counts, color=['red', 'gray', 'green'])
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.title('Sentiment Distribution')
    plt.ylabel('Count')
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    
    plt.close()

def plot_accuracy_metrics(overall: float, positive: float, negative: float, output_file: str = None):
    """
    Plot accuracy metrics.
    
    Args:
        overall: Overall accuracy percentage
        positive: Positive reviews accuracy percentage
        negative: Negative reviews accuracy percentage
        output_file: Path to save the plot. If None, shows the plot instead.
    """
    plt.figure(figsize=(8, 5))
    bars = plt.bar(['Overall', 'Positive', 'Negative'], [overall, positive, negative], 
                  color=['blue', 'green', 'red'])
    
    # Add percentage labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.title('Sentiment Analysis Accuracy')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    
    plt.close()