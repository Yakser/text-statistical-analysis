import string
import logging

from difflib import SequenceMatcher
from .models import Query, Synonym, ServiceWord

logger = logging.getLogger(__name__)

TRESHOLD = 0.75


def clean_text(text):
    """
    Удаляет знаки пунктуации из текста и разбивает на слова.
    """
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator).lower().split()


def find_synonyms(word: str) -> set[str]:
    return set(
        Synonym.objects.filter(word=word).values_list("synonym", flat=True)
    ) | set(Synonym.objects.filter(synonym=word).values_list("word", flat=True))


def generate_synonym_queries(query: list[str]) -> list[list[str]]:
    """
    Генерирует запросы из синонимов на основе списка слов.
    """

    synonym_queries = [query]
    for i, word in enumerate(query):
        synonyms = find_synonyms(word)
        for synonym in synonyms:
            new_query = query[:]
            new_query[i] = synonym
            synonym_queries.append(new_query)
    return [query for query in synonym_queries]


def join_queries(queries: list[list[str]]) -> list[str]:
    return [" ".join(query) for query in queries]


def compare_queries(user_query: str, query_from_db: str) -> float:
    """
    Сравнивает два запроса и возвращает процент соответствия.
    """
    return SequenceMatcher(None, user_query, query_from_db).ratio()


def save_differences_as_synonyms(user_query_words, db_query_words):
    """
    Сохраняет отличающиеся слова как контекстные синонимы.
    """
    for user_word, db_word in zip(user_query_words, db_query_words):
        if user_word != db_word:
            synonym_exists = (
                Synonym.objects.filter(word=user_word, synonym=db_word).exists()
                or Synonym.objects.filter(word=db_word, synonym=user_word).exists()
            )

            if not synonym_exists:
                Synonym.objects.create(word=user_word, synonym=db_word)
                logger.info(f"Added synonym: {user_word} -> {db_word}")


def process_user_query(user_input):
    logger.info(f"Processing query: {user_input}")

    words = clean_text(user_input)

    service_words = set(ServiceWord.objects.values_list("word", flat=True))
    words = [word for word in words if word not in service_words]

    potential_queries = generate_synonym_queries(words)

    queries_from_db = Query.objects.all()
    best_match = None
    best_score = 0

    for pq in join_queries(potential_queries):
        for query in queries_from_db:
            score = compare_queries(pq, query.text)
            if score > best_score:
                best_score = score
                best_match = query

    if best_match and best_score >= TRESHOLD:
        db_query_words = clean_text(best_match.text)

        if len(words) == len(db_query_words):
            save_differences_as_synonyms(words, db_query_words)

        return {"response": best_match.response, "score": best_score}

    return {"response": "Can't find query", "score": 0}
