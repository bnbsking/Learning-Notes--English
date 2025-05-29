### Introduction
Random generator for memorizing customized vocabulary. This project can be easily run on phone devices (e.g. PythonEditor) to utilize its convenience.

### File Structure
+ main.py: main program
+ data.txt.py: custom vocabulary split by "\n\n"
+ cards_target.pkl: vocabulary needs to be studied.
+ cards_finish.pkl: vocabulary have already studied.
+ status.txt: logs for the operations.

### Prerequisites
+ Python 3+

### Usage
+ task_id in main.py runs different modes:
    + 0 (update): used when data.txt.py is updated, refresh cards_target but remains cards_finish.
    + 1 (study_target): study cards_target. If a card is memorized, add it to cards_finish.
    + 2 (study_finish): review cards_finish. If a card is forgotten, add it to cards_target.
```bash
python main.py
```