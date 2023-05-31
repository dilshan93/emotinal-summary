# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from os import listdir, makedirs
from os.path import isfile, join, exists

from Book_Summarizer.extractive_summarizer import find_relevant_quote
from data import process_book, get_results_filename


def summarize_book(book_id, num_chapters):

    if not exists('results/summaries'):
        makedirs('results/summaries')
    summary_filename = get_results_filename(book_id)
    if not (isfile(summary_filename)):
        with open(summary_filename, 'w') as complete_summary:
            # for each chapter
            for chapter in range(num_chapters):
                line = "Chapter " + str(chapter)
                complete_summary.write(line + '\n')
                # find quote using extractive summary techniques
                quote = find_relevant_quote(book_id, chapter, 2, 'luhn')
                # Print quote from chapter
                if len(quote) == 1:
                    complete_summary.write('Quote: ')
                else:
                    complete_summary.write('Quotes:\n')
                for q in quote:
                    line = '"' + str(q) + '"'
                    complete_summary.write(line + '\n')
                complete_summary.write('\n')





def main():
    book_files = [f for f in listdir('data/raw_books') if isfile(join('data/raw_books', f))]
    for f in book_files:
        book_id = (f.strip('.txt'))
        # break down into chapters / segments, then summarize book
        book_id, num_chapters = process_book(book_id)
        if (book_id != ""):
            summarize_book(book_id, num_chapters)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
