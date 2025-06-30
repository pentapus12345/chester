from datetime import datetime

class Memory(object):
    def __init__(self):
        pass
        self.columns = ("date","time", "keywords","fact")
        self.memories_file = "Assets/memories.csv"
        self.verbose=True

    def remember(self, keywords: list, fact: str):
        timestamp = datetime.now()
        line = f'"{datetime.strftime(timestamp,"%Y-%m-%d")}", "{datetime.strftime(timestamp, "%H:%M")}","{", ".join(keywords)}", "{fact}"\n' 
        with open(self.memories_file,'a') as fd:
            fd.write(line)
            if self.verbose:
                print (f"Remembering: {fact}\nWith Keywords:{', '.join(keywords)}")
    

  