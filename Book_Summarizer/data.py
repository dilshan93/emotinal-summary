import os


def get_text_filename(book_id, chapter_num=-1):
    """ Get the filename for a text document with the book identifier and chapter number. """
    if chapter_num != -1:
        filename = book_id + '-' + str(chapter_num) + '.txt'
    else:
        filename = book_id + ".txt"
    return filename


def get_data_filename(book_id, foldername, chapter_num=-1):
    """
    Get the filename for a data file with the book identifier and chapter number in foldername.
    """
    return 'data/' + foldername + '/' + get_text_filename(book_id, chapter_num)

def get_results_filename(book_id):
    """
    Get the filename for a results file with the book identifier and tags specified in args.
    """
    return 'results/summaries/' + book_id +'-all.txt'


def save_clean_book(pg_index):
    """
    Saves a clean version of the book to the ../data/books directory.
    Removes the Project Gutenberg license and book information where possible.

    Parameters:
    pg_index: the project gutenberg book index

    Outputs:
    Saves the clean book.
    """
    if not os.path.exists('data/books'):
        os.makedirs('data/books')
    text_filename = get_text_filename(pg_index)
    book_filename = get_data_filename(pg_index, 'raw_books')
    clean_book_filename = get_data_filename(pg_index, 'books')
    with open(book_filename, 'r', encoding='latin-1') as book:
        with open(clean_book_filename, 'w') as clean_book:
            write_lines = False
            for l in book:
                if (l[:12] == '*** START OF') or (l[:11] == '***START OF') or (l[:11] == '*END*THE SM'):
                    write_lines = True
                elif (l[:10] == '*** END OF') or (l[:9] == '***END OF'):
                    write_lines = False
                elif write_lines:
                    clean_book.write(l)
    # if the formatting didn't match the above, just use the complete
    # book with project gutenberg information
    if os.stat(clean_book_filename).st_size == 0:
        with open(book_filename, 'r', encoding='latin-1') as book:
            with open(clean_book_filename, 'w') as clean_book:
                for l in book:
                    clean_book.write(l)

def save_chapter(filename, lines):
    """ Saves chapter lines to filename. """
    with open(filename, 'w') as chapter:
        for l in lines:
            chapter.write(l)


def divide_book_into_chapters(book_id):
    """
    Divides the book file into separate chapter files.
    Assumes chapter breaks occur when there are two empty lines in a row
    Makes chapters at least 20 lines long as there are often two double spaces
    at the start of a chapter
    Limits chapters to the end of the next paragraph after 3000 lines

    Parameters:
    book_id: (str) the book identifier

    Outputs:
    The chapter files are saved in the data/book_chapters folder.
    """
    if not os.path.exists('data/book_chapters'):
        os.makedirs('data/book_chapters')
    book_filename = get_data_filename(book_id, 'books')
    count_chapters = 0
    count_lines_in_chapter = 0
    previous_blank_line = False
    with open(book_filename, 'r', encoding='latin-1') as book:
        lines = []
        for l in book:
            if (count_lines_in_chapter < 3000) and ((len(l) > 1) or (count_lines_in_chapter < 20)):
                previous_blank_line = False
                count_lines_in_chapter += 1
                lines.append(l)
            elif (len(l) == 1) and ((previous_blank_line == True) or (count_lines_in_chapter >= 3000)):
                count_lines_in_chapter = 0
                save_chapter(get_data_filename(
                    book_id, 'book_chapters', count_chapters), lines)
                count_chapters += 1
                lines = []
            elif (len(l) == 1):
                count_lines_in_chapter += 1
                previous_blank_line = True
                lines.append(l)
            else:
                count_lines_in_chapter += 1
                lines.append(l)
        save_chapter(get_data_filename(
            book_id, 'book_chapters', count_chapters), lines)
        count_chapters += 1
    return count_chapters

def process_book(book_id):
    """
    Processes the book book_id into a clean book and divides it into chapters.

    Parameters:
    book_id: (str) the book identifier

    Returns:
    int book_id to confirm that the file has been successfully found
    int num_chapters the number of chapters the book has been divided into
    """
    num_chapters = 0
    if not os.path.isfile(get_data_filename(book_id, 'raw_books')):
        book_id = ""
    if book_id != "":
        save_clean_book(book_id)
        num_chapters = divide_book_into_chapters(book_id)
    return book_id, num_chapters