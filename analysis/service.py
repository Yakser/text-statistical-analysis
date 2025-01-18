import string
import logging

from difflib import SequenceMatcher
from .models import Query, ServiceWord, Word, SynonymGroup

logger = logging.getLogger(__name__)

THRESHOLD = 0.5


def clean_text(text: str) -> list[str]:
    """
    Удаляет знаки пунктуации из текста и разбивает на слова.
    """

    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator).lower().split()


def find_synonyms(word: str) -> set[str]:
    try:
        group = Word.objects.get(text=word).group
        synonyms = set(group.words.values_list("text", flat=True))
        return synonyms - {word}
    except Word.DoesNotExist:
        return set()


def add_word_to_group(word: str, group_name: str) -> None:
    group, created = SynonymGroup.objects.get_or_create(name=group_name)

    if not Word.objects.filter(text=word).exists():
        Word.objects.create(text=word, group=group)


def generate_synonym_queries(query: list[str]) -> list[list[str]]:
    synonym_queries = [query]
    for i, word in enumerate(query):
        synonyms = find_synonyms(word)
        for synonym in synonyms:
            new_query = query[:]
            new_query[i] = synonym
            synonym_queries.append(new_query)
    return [query for query in synonym_queries]


def compare_queries(user_query: list[str], query_from_db: list[str]) -> float:
    return SequenceMatcher(None, " ".join(user_query), " ".join(query_from_db)).ratio()


def save_differences_as_synonyms(user_query_words, db_query_words):
    """
    Находит отличия между словами запросов и добавляет их в общую группу синонимов.
    """

    for user_word, db_word in zip(user_query_words, db_query_words):
        if user_word != db_word:
            try:
                # Проверяем, есть ли одно из слов в существующей группе
                user_word_obj = Word.objects.filter(text=user_word).first()
                db_word_obj = Word.objects.filter(text=db_word).first()

                if user_word_obj and db_word_obj:
                    if user_word_obj.group == db_word_obj.group:
                        continue
                    else:
                        # Если слова в разных группах, сливаем их группы
                        db_group = db_word_obj.group
                        user_group = user_word_obj.group

                        for word in db_group.words.all():
                            word.group = user_group
                            word.save()

                        db_group.delete()
                        logger.info(
                            f"Merged synonym groups for words '{user_word}' and '{db_word}'"
                        )
                elif user_word_obj:
                    Word.objects.create(text=db_word, group=user_word_obj.group)
                elif db_word_obj:
                    Word.objects.create(text=user_word, group=db_word_obj.group)
                else:
                    group = SynonymGroup.objects.create(
                        name=f"Group for {user_word} and {db_word}"
                    )
                    Word.objects.create(text=user_word, group=group)
                    Word.objects.create(text=db_word, group=group)

                    logger.info(
                        f"Created new group for words '{user_word}' and '{db_word}'"
                    )
            except Exception as e:
                logger.error(
                    f"Error saving synonyms for '{user_word}' and '{db_word}': {e}"
                )


def remove_service_words(words: list[str]) -> list[str]:
    service_words = set(ServiceWord.objects.values_list("word", flat=True))
    return [word for word in words if word not in service_words]


def process_user_query(user_input):
    logger.info(f"Processing query: {user_input}")

    cleaned_words = clean_text(user_input)
    logger.info(f"Cleaned words: {cleaned_words}")
    words_wo_service = remove_service_words(cleaned_words)
    logger.info(f"Remove service words: {words_wo_service}")
    original_words_count = len(words_wo_service)
    potential_queries = generate_synonym_queries(words_wo_service)
    logger.info(f"Generate potentional queries: {potential_queries}")

    queries_from_db = Query.objects.all()
    best_match = None
    best_score = 0

    for pq in potential_queries:
        for query in queries_from_db:
            cleaned_db_query = remove_service_words(clean_text(query.text))

            if len(cleaned_db_query) == original_words_count:
                score = compare_queries(pq, cleaned_db_query)
                if score > best_score:
                    best_score = score
                    best_match = query

    if best_match and best_score >= THRESHOLD:
        db_query_words = remove_service_words(clean_text(best_match.text))

        if len(words_wo_service) == len(db_query_words):
            save_differences_as_synonyms(words_wo_service, db_query_words)

        return {"response": best_match.response, "score": best_score}

    return {"response": "Can't find query", "score": 0}
