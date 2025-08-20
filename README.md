## Introduction
Learn English by AI


## Environment setting
reference `env.sh`


## Learning Vocabularies
1. Setting GOOGLE_API_KEY as `C:\Users\James\Desktop\code\.bat`

2. Put vocabs in `data/data_tmp.txt`

3. Extract vocab into `output/vocab_tmp.json`
```bash
python srcipts/extract_vocab.py
```

4. Generate articles into `output/articles/article_*.md`
```bash
python srcipts/article_generator.py
``` 

5. Append QA after the above articles
```bash
python scripts/article_generator_qa.py
```

## Practicing Interview
1. Setting GOOGLE_API_KEY as `C:\Users\James\Desktop\code\.bat`

2. Prepare resume in `data/resume.txt` and recruiting requirements in `data/recuiting_requirements_01.txt`

3. Generate interview questions in `output/interview/interview_questions.json`
```bash
python srcipts/interview.py
```

4. (Optional) Generate model answers to `output/interview/interview_questions_with_model_answers.json`
```bash
python srcipts/interview_saver.py
``` 

5. Generate questions audio in `output/interview/interview_audio/*.wav`
```bash
python srcipts/interview_saver.py
```

6. Answer the questions
    + Copy `output/interview/interview_questions.json` to `output/data/interview_answwers.json`
    + Listen to the audio and answer all the questions

7. Evaluate the results to `output/interview/interview_results.json`
```bash
python srcipts/interview_eval.py
```