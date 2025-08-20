extract_vocabs = """
    ***Task**: Below is my vocabulary note. Can you extract all the vocabularies as a list of string.
    Do not include any explanation.

    [start of the vocabulary note]
    {{ vocabularies }}
    [end of the vocabulary note]

    **Response format:
    ```json
    [
        "vocabulary1",
        "vocabulary2",
        ...
    ]
    ```
"""  # 325 characters


generate_article = """
    **Task**: Below is a list of vocabulary words.
    Use these words to generate a short article in markdown format.
    You should follow these rules:
    
    1. If the vocabulary mis-spelled, please correct it.
    2. Make sure the grammar is correct and the article is coherent.
    3. Use medium-level language (roughly IELTS 6~7) suitable for English learners
    4. Highlight the **vocabulary** as bold in markdown
    5. Give the article a title
    
    **Vocabularies**: {{ vocabularies }}
"""


generate_article_qa = """
    **Task**: Below is an article.
    Generate 3 single choice questions based on the article and its corresponding answers.
    You should follow these rules:
    + The vocabularies in the question and answer are suggested to be diffrent from the vocabularies in the article, i.e. use synonyms if possible.
    + The choices should be A, B, C, D.
    + The probability of true answer for each choices should be roughly equal.
    
    **Article**: {{ article }}

    **Response format**:
    ```json
    [
        {
            "Question": [str],
            "Choice A": [str],
            "Choice B": [str],
            "Choice C": [str],
            "Choice D": [str],
            "Answer": [A/B/C/D],
            "Explanation": [str],
        },
        ...
    ]
    ```
"""


generate_vocab = """
    **Task**: Below is a list of vocabulary words.
    For each vocabulary, generate its:
    1. definition
    2. part of speech (noun, verb, adjective, adverb, etc.) 
    3. example sentence
    4. synonyms (if applicable otherwise leave it empty)
    5. antonyms (if applicable otherwise leave it empty)
    
    **Vocabularies**: {{ vocabularies }}

    **Response format**:
    ```json
    [
        {
            "vocabulary": "vocabulary1",
            "definition": "definition of vocabulary1",
            "part_of_speech": "noun/verb/adjective/adverb/...",
            "example_sentence": "example sentence using vocabulary1",
            "synonyms": ["synonym1", "synonym2"],
            "antonyms": ["antonym1", "antonym2"]
        },
        ...
    ]
    ```
"""