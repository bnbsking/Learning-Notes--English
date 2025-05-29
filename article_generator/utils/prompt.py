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
    **Task**: Below is a list of vocabulary words. Can you generate an article that uses all of these words?
    
    **Output Format:** output in markdown format and use **vocabulary** (bold in markdown) to highlight the vocabularies.
    
    **Vocabularies**: {{ vocabularies }}
"""
