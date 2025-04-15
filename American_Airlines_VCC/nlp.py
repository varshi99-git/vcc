import os
import mysql.connector
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from collections import Counter

class feedback_analytics:

    @staticmethod
    def analyze():
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Varshith@30',
            database='americanairlines'
        )
        cursor = db.cursor()
        cursor.execute('SELECT message FROM feedback')
        outs = cursor.fetchall()
        feedbacks = [item[0] for item in outs]

        sia = SentimentIntensityAnalyzer()
        sentiment_list = []
        for feedback in feedbacks:
            sentiment_score = sia.polarity_scores(feedback)
            sentiment_label = feedback_analytics.get_sentiment_label(sentiment_score)
            sentiment_list.append(sentiment_label)

        return feedback_analytics.plot_pie_chart(sentiment_list)

    @staticmethod
    def get_sentiment_label(sentiment_score):
        compound_score = sentiment_score['compound']
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    @staticmethod
    def plot_pie_chart(sentiment):
        sentiment_counts = Counter(sentiment)
        pos_count = sentiment_counts.get('Positive', 0)
        neg_count = sentiment_counts.get('Negative', 0)
        neutral_count = sentiment_counts.get('Neutral', 0)
        total_count = pos_count + neutral_count + neg_count

        labels = ['Positive feedbacks', 'Negative feedbacks', 'Neutral feedbacks']
        sizes = [pos_count, neg_count, neutral_count]
        colors = ['green', 'red', 'gray']

        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')

        # Ensure the static directory exists
        static_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        output_path = os.path.join(static_dir, 'sentiment.png')
        plt.savefig(output_path)
        plt.close()

        return output_path
