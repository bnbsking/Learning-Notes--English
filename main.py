import os, pickle, random

# get cards_raw
update = False
if update:
    titles = [ chr(ord('A')+i)*3 for i in range(26) ]
    text = open("EnglishVocab.txt", "r").read()
    cards_raw = [ card.strip('\n') for card in text.split("\n\n") if all(tit not in card for tit in titles) ]
    pickle.dump(cards_raw, open('cards_raw.pkl','wb'))
else:
    cards_raw = pickle.load(open('cards_raw.pkl', 'rb'))

# get cards_mem
cards_mem = pickle.load(open("cards_mem.pkl", "rb")) if os.path.isfile("cards_mem.pkl") else []

# get cards
cards = list(set(cards_raw)-set(cards_mem))

# stats
raw, mem, tar = len(cards_raw), len(cards_mem), len(cards)
print(f"Completed = mem/all = {mem}/{raw} = {round(mem/raw,3)}")
print(f"target cards = {tar}")
print("Let's start\n"+"-"*70)

# start
count, mem0 = 1, mem
while 1:
    idx = random.randint(0,len(cards)-1)
    print(f"Count={count}")
    print(cards[idx])
    action = input("[N] Do_nothing, [Y] Add_to_mem, [Q] Save_quit: ")
    
    if action.upper() == 'Y':
        cards[idx], cards[-1] = cards[-1], cards[idx]
        cards_mem.append( cards.pop() )
        mem = len(cards_mem)
        print(f"Saved to memory. Completed = mem/all = {mem}/{raw} = {round(mem/raw,3)}")
    
    elif action.upper() == 'Q':
        pickle.dump(cards_mem, open('cards_mem.pkl','wb'))
        print(f"Bye. Today complete = {mem-mem0}")
        print(f"Completed = mem/all = {mem}/{raw} = {round(mem/raw,3)}")
        break
    
    count+=1
    print('-'*70)
