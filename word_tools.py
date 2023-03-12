from words import WORDS
from collections import Counter

if __name__ == '__main__':
    all_letters = ''.join(WORDS)
    letter_counts = Counter(all_letters)

    total_letter_count = 0
    for letter, count in letter_counts.items():
        total_letter_count += count

    letter_distribution = []
    for letter, count in letter_counts.items():
        out_of_100ish_count = max(count*100//total_letter_count, 1)
        letter_distribution.extend([letter]*out_of_100ish_count)

    print(sorted(letter_distribution))
