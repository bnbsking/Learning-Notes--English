gen_q_from_requirements = """
    **Task**: You are a helpful assistant for job interviews.
    Based on the following recruiting requirements,
    generate a list of potential interview questions.
    The questions should start from soft skills and gradually progress to technical skills.

    **Recruiting Requirements**:
    {{ recruiting_requirements }}

    **Response format**:
        ```json
        [
            "Question 1: ...",
            "Question 2: ...",
            "Question 3: ...",
            "Question 4: ...",
            "Question 5: ...",
            ...
        ]
        ```
    """


gen_q_from_requirements_and_resume = """
    **Task**: You are a helpful assistant for job interviews.
    Based on the following recruiting requirements and the candidate's resume,
    generate a list of potential interview questions.
    The questions are preferred to involving the content in resume relates to the requirements.

    **Recruiting Requirements**:
    {{ recruiting_requirements }}

    **Candidate's Resume**:
    {{ candidate_resume }}

    **Response format**:
        ```json
        [
            "Question 1: ...",
            "Question 2: ...",
            "Question 3: ...",
            "Question 4: ...",
            "Question 5: ...",
            ...
        ]
        ```
    """


get_model_answer = """
    **Task**: You are a helpful assistant for interviewees.
    You are given a interview question,
    and also the recruiting requirements and the candidate's resume,
    generate a model answer for the question.
    You should answer in 50 words or less.

    **Recruiting Requirements**:
    {{ recruiting_requirements }}

    **Candidate's Resume**:
    {{ candidate_resume }}

    **Interview Question**:
    {{ interview_question }}
    """


evaluation = """
    **Task**: You are a helpful assistant for interviewees.
    You are given an interview question and a candidate's answer.
    Evaluate the answer by the following criteria, give each a score from 0 to 2.

    **Criterion**:
    1. Relevance and Completeness: Does the answer address the question and cover all necessary points?
        + 0: the answer deviated from the question.
        + 1: the answer addressed the question but missed some points.
        + 2: the answer nearly covers most of the points of the question.
    2. Reasonability: Does the answer make sense?
        + 0: the answer is illogical or nonsensical.
        + 1: the answer is somewhat reasonable but has flaws.
        + 2: the answer is entirely reasonable.
    3. Beneficiality: Does the answer provide value or insight?
        + 0: the answer is not helpful.
        + 1: the answer provides some value but is lacking.
        + 2: the answer is highly beneficial and insightful.

    **Notes**:
    + Ignore minor grammar errors and thesaurus that does not affect understanding.
    + Finally give the explanation with recommendation to improve.

    **Question**: {{ question }}

    **Answer**: {{ answer }}

    **Response format**:
        ```json
        {
            "relevance_and_completeness": [int: 0~2],
            "reasonability": [int: 0~2],
            "beneficiality": [int: 0~2],
            "explanation": [string]
        }
        ```
    """