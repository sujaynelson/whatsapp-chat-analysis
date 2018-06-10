import sys
import re
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()

def cleanText(filename):

    chat = open(filename)
    chatText = chat.read()

    # 01/09/17, 11:34 PM - Innaya:
    pattern = "(\d+\/\d+\/\d+)(,)(\s)(\d+:\d+)(\s)(\w+)(\s)(-)(\s\w+)*(:)"

    mediaPattern = "(\<Media omitted\>)"
    regexMedia = re.compile(mediaPattern, flags=re.M)
    regex = re.compile(pattern, flags=re.M)

    clean = regex.sub("", chatText)
    clean = regexMedia.sub("", clean)
    lines = []

    for line in clean.splitlines():
        if line.strip() is not "":
            lines.append(line.strip())

    return lines

negative_sentences = [];
def analyze(name):
    linesList = cleanText(name + '.txt')
    neutral, negative, positive = 0, 0, 0

    for index, sentence in enumerate(linesList):
        print("Processing {0}%".format(str((index * 100) / len(linesList))))

        scores = sentiment_analyzer.polarity_scores(sentence)
        scores.pop('compound', None)

        maxAttribute = max(scores, key=lambda k: scores[k])

        if maxAttribute == "neu":
            neutral += 1
        elif maxAttribute == "neg":
            # Remove EMOJIS
            if re.match(r'^[\w]', sentence):
                negative_sentences.append(sentence)
                negative += 1
        else:
            positive += 1

    total = neutral + negative + positive
    print("Negative: {0}% | Neutral: {1}% | Positive: {2}%".format(
        negative*100/total, neutral*100/total, positive*100/total))

    labels = 'Neutral', 'Negative', 'Positive'
    sizes = [neutral, negative, positive]
    colors = ['#00bcd7', '#F57C00', '#CDDC39']

    # Plot
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=140)

    plt.axis('equal')
    plt.title("Sentiment Analysis - Chat with {0}".format(name.capitalize()))
    plt.show()

analyze(sys.argv[1])
negative_sentences_file = open('negative_sentences - {0}.txt'.format(sys.argv[1]), 'w')

for item in negative_sentences:
  negative_sentences_file.write("%s\n" % item)