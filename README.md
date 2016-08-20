# Tokenizer and Sentence Generator
A simple Twitter tokenizer and a Sentence Generator that generates sentences using n-grams.

It reads data from 'twitter.en.txt' and saves the tokenized data in 'TokenizedOutput' file.

It also prints 10 sentences each generated using previous n-grams (n <= 6).
The code chooses a random n-gram as the starting token and then predicts the next token by calculating probability of each token given the previous n-grams.
