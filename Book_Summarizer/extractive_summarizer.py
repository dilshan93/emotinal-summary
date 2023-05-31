"""
This file has the functions for the extractive summarizer.
Create an extractive summary from chapters of a large document.
"""
import requests
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

from Book_Summarizer.data import get_data_filename


def find_relevant_quote(book_id, chapter, num_sentences=1, technique='luhn'):
    """
    Create an extractive summary for a chapter of the book.

    Parameters:
    book_id: (str) the book identifier
    chapter: is the chapter number to summarize
    num_sentences: how many sentences to extract

    Returns:
    sentences: the extracted sentences
    """
    chapter_filename = get_data_filename(book_id, 'book_chapters', chapter)
    parser = PlaintextParser.from_file(chapter_filename, Tokenizer("english"))
    emotion_analysis(open(chapter_filename, 'r').read())
    if technique=='lsa':
        summarizer = LsaSummarizer()
    elif technique=='lexrank':
        summarizer = LexRankSummarizer()
    elif technique=='textrank':
        summarizer = TextRankSummarizer()
    elif technique=='kl':
        summarizer = KLSummarizer()
    elif technique=='random':
        summarizer = RandomSummarizer()
    elif technique=='reduction':
        summarizer = ReductionSummarizer()
    elif technique=='sumbasic':
        summarizer = SumBasicSummarizer()
    else:
        summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return summary


def emotion_analysis(summary):

    url = "https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/"
    headers = {
        'x-rapidapi-host': "twinword-emotion-analysis-v1.p.rapidapi.com",
        'x-rapidapi-key': "7a97cfe53bmsh897262587233fb1p11136ajsn83b45ef57a13"
    }
    emo = []

    querystring = {"text": summary}
    response = requests.request("GET", url, headers=headers, params=querystring)
    text_dic = response.text
    emo.append(text_dic)

    #
    return emo