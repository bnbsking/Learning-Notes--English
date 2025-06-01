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
