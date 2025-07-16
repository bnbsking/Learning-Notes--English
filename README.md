## Introduction
Learn English by AI

## Steps
1. Setting GOOGLE_API_KEY as `C:\Users\James\Desktop\code\.bat`

2. Put vocabs in `data_tmp.txt`

3. Extract vocab into `output/vocab.json`
```bash
python -m src.article_generator.main
```

4. Generate QA into `output/articles/article_*.md`
```python
python -m src.article_generator.qa
```
