import datetime, os, pickle, random, sys


# configs
path_material = "../data.txt"
path_cards_target = "cards_target.pkl"
path_cards_finish = "cards_finish.pkl"
task_dict = {
    0: "update: used when material is updated, refresh cards_target but remains cards_finish.",
    1: "study_target: study cards_target. If a card is memorized, add it to cards_finish.",
    2: "study_finish: review cards_finish. If a card is forgotten, add it to cards_target.", 
}
task_id = 2  # default 1


# update or load cards
def update_or_load_cards(task_val: str) -> tuple[list, list, str]: 
    assert task_val.count(":")==1, f"task_dict[task_id] should be in `task: description` format, but got {task_dict[task_id]}."
    task, task_description = task_val.split(":")
    print(f"Activate task {task}: {task_description}")
    
    if task == "update":
        titles = [ chr(ord('A')+i)*3 for i in range(26) ]
        data = open(path_material, "r", encoding="utf-8").read()
        cards_target = [ card.strip('\n') for card in data.split("\n\n") if all(tit not in card for tit in titles) ]
        pickle.dump(cards_target, open('cards_target.pkl','wb'))
        print("update completed :D")
        sys.exit(0)

    elif task in ("study_target", "study_finish"):
        cards_target = pickle.load(open(path_cards_target, 'rb')) if os.path.isfile(path_cards_target) else []
        cards_finish = pickle.load(open(path_cards_finish, 'rb')) if os.path.isfile(path_cards_finish) else []
        if task == "study_target":
            return cards_target, cards_finish, task
        else:
            return cards_finish, cards_target, task

    else:
        raise KeyError(f"Unknown task {task}")
cards_study, cards_trans, task = update_or_load_cards(task_dict[task_id])


# show stats
if task == "study_target":
    remembered_rate = round(len(cards_trans)/(len(cards_study)+len(cards_trans)), 5)
    print(f"Remembered rates = trans/(study+trans) = {len(cards_trans)}/{(len(cards_study)+len(cards_trans))} = {remembered_rate * 100}%")
    print("Let's start increasing the score\n" + "-" * 50)
elif task == "study_finish":
    remembered_rate = round(len(cards_study)/(len(cards_study)+len(cards_trans)), 5)
    print(f"Remembered rates = study/(study+trans) = {len(cards_study)}/{(len(cards_study)+len(cards_trans))} = {remembered_rate * 100}%")
    print("Let's start remaining the score\n" + "-" * 50)
else:
    raise KeyError(f"Unknown task {task}")


# start
count = 1  # total cards review today
move = 0  # total movement from cards_study to cards_trans
while 1:
    idx = random.randint(0, len(cards_study)-1)
    print(f"Count={count}")
    print(cards_study[idx])
    action = input("[N/Enter] Do_nothing, [Y] Add_to_trans, [Q] Save_quit: ")
    
    if action.upper() == 'Y':
        cards_study[idx], cards_study[-1] = cards_study[-1], cards_study[idx]
        cards_trans.append(cards_study.pop())
        move += 1
        print(f"total moves = {move}")
    
    elif action.upper() == 'Q':
        print("-"*50 + "\nBye! Today's progress:")
        
        if task == "study_target":
            print(f"raw_remembered ({len(cards_trans)-move}) + new_remembered ({move}) = current_remembered ({len(cards_trans)})")
            pickle.dump(cards_study, open(path_cards_target,'wb'))
            pickle.dump(cards_trans, open(path_cards_finish,'wb'))
            len_cards_target = len(cards_study)
            len_cards_finish = len(cards_trans)
        
        elif task == "study_finish":
            print(f"raw_remembered ({len(cards_study)+move}) - forgotten ({move}) = current_remembered ({len(cards_study)})")
            pickle.dump(cards_study, open(path_cards_finish,'wb'))
            pickle.dump(cards_trans, open(path_cards_target,'wb'))
            len_cards_target = len(cards_trans)
            len_cards_finish = len(cards_study)
        
        new_remembered_rate = round(len_cards_finish/(len_cards_target+len_cards_finish), 5)
        print(f"raw_remembered_rate={remembered_rate}, new_remembered_rate={new_remembered_rate}, diff={new_remembered_rate-remembered_rate}")    
        print(f"current_remained = {len_cards_target}")
        with open("status.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}, finish/(target+finish) = {len_cards_finish}/{(len_cards_target+len_cards_finish)} = {new_remembered_rate * 100}%\n")
        sys.exit(0)
    
    count+=1
    print('-'*50)