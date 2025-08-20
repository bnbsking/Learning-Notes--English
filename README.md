## Introduction
Learn English by AI

## Steps
1. Setting GOOGLE_API_KEY as `C:\Users\James\Desktop\code\.bat`

2. Put vocabs in `data_tmp.txt`

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
