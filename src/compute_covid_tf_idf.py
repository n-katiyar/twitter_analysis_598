import json
import argparse
import math


def tf_idf(w, category, pdict):
    return calculate_tf(w, category, pdict) * calculate_idf(w, pdict)


def calculate_tf(w, category, pdict):
    words = pdict[category]
    if w in words:
        counts = words[w]
    else:
        counts = 0
    return counts


def calculate_idf(w, pdict):
    numOfCovid = len(pdict)
    numOfCovidUsed = 0
    for _, words in pdict.items():
        for word, _ in words.items():
            if w == word:
                numOfCovidUsed += 1

    if numOfCovidUsed == 0:
        return 0
    return math.log(numOfCovid / numOfCovidUsed)


def calculate_covid_td_idf(category, pdict):
    covid_dict = {}
    words = pdict[category]
    for word in words:
        covid_dict[word] = tf_idf(word, category, pdict)
    sorted_covid_dict = sorted(covid_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_covid_dict = dict(sorted_covid_dict)

    return dict(list(sorted_covid_dict.items())[:10])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    counts_file = args.counts
    output = args.output

    covid_td_idf = {}
    categories = ["Covid stats", "Measure and management", "Covid social life", "Vaccine efficacy", "Covid variant",
                  "Covid politics", "Covid symptoms", "Economy"]

    with open(counts_file, 'r') as fh:
        covid_dict = json.load(fh)

    for category in categories:
        covid_words = calculate_covid_td_idf(category, covid_dict)
        covid_td_idf[category] = covid_words

    with open(output, 'w') as fh:
        json.dump(covid_td_idf, fh, indent=4)


if __name__ == '__main__':
    main()
