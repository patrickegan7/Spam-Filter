# spam-filter

This repository uses a pre-processed set of emails from the following link:
http://nlp.cs.aueb.gr/software_and_datasets/Enron-Spam/index.html

The goal of this code was to use Python to make an email spam filter with a Naive Bayes Classifier. I use 6-fold cross validation to find the best set of training data from the dataset which was 89% effective at classifying the holdout set.

I believe that this project could be improved upon by including a more diverse set of spam/ham emails, refining what strings are considered words, and by extending the cross validation to be more granular than the dividing the set into its 6 pre-established subsets.

This is my first project in Python and it was largely a foray in learning how to use the language and about the vast number of libraries Python has to offer (even though I avoided many of them). I also learned the importance of choosing and pre-processing a dataset, as well as learning some patience by waiting for my classifier to learn from that data.
