import pandas as pd
import argparse
import json
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
from matplotlib import pyplot as plt


def preprocessing_data(categories, filename):
    df = pd.read_csv(filename)
    df_covid = df[df['Topics'].isin(categories)]
    df_covid["full_text"] = df_covid['full_text'].str.replace('[^\w\s]', ' ')
    return df_covid


def collect_words(category, df_covid):
    category_words = {}
    df_category = df_covid[df_covid['Topics'] == category]

    contents = df_category['full_text']
    for _, sentence in contents.items():
        words = sentence.split(' ')
        for word in words:
            if word.isalpha() and word not in stopwords.words() and word.lower() not in stopwords.words():
                if word not in category_words:
                    category_words[word] = 1
                else:
                    category_words[word] += 1
    category_words = dict(sorted(category_words.items(), key=lambda x: x[1], reverse=True))
    return category_words


def draw_bar_char(df_covid):
    df_covid.groupby(['Topics', "Sentiment"])["Sentiment"].count().unstack().plot.barh()
    plt.title("Distribution of Sentiment for each Salient Topic on 2021.11.25")
    plt.xlabel('Number of Tweets')
    plt.ylabel('Salient Topics')
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to read tweets")
    parser.add_argument("-o", "--output", help="Path to save tweets")

    args = parser.parse_args()

    inputFile = args.input
    outputFile = args.output

    categories = ["Covid stats", "Measure and management", "Covid social life", "Vaccine efficacy", "Covid variant",
                  "Covid politics", "Covid symptoms", "Economy"]
    covid_words = {}

    df_covid = preprocessing_data(categories, inputFile)
    for category in categories:
        covid_words[category] = collect_words(category, df_covid)

    with open(outputFile, 'w') as fp:
        json.dump(covid_words, fp, indent=4)

    draw_bar_char(df_covid)


if __name__ == '__main__':
    main()
