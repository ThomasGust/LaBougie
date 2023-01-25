import pickle as pkl
import time


class Candle:

    def __init__(self, name, burn_time, color):

        assert type(color) == tuple or type(color) == str or type(color) == None

        self.color = color
        self.burn_time = burn_time
        self.e_time = 0.0
        self.name = name
        self.creation_date = time.time()
    
    def save_candle(self, path):

        with open(path, "wb") as f:
            pkl.dump({'color':self.color,
            'burn_time':self.burn_time,
            'elapsed_time':self.e_time,
            'name':self.name,
            'created':self.creation_date}, f)
    
    def load_candle(self, path):

        with open(path, "rb") as f:
            d = pkl.load(f)

            self.color = d['color']
            self.burn_time = d['burn_time']
            self.e_time = d['elapsed_time']
            self.name = d['name']
            self.creation_date = d['created']

if __name__ == "__main__":
    candle = Candle('TEST', 12.0*60.0*60.0, (255, 255, 0))
