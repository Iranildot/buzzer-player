import time

class Timer:
    def __init__(self) -> None:
        self.current = 0.0
        self.variation = 0.0
        self.start = 0.0
        self.end = 0.0
    
    def timer(self, end_time):
        self.end = time.time()
        self.variation = self.end - self.start
        
        self.start = self.end
        self.current += self.variation
        
        return self.current >= end_time
    
    def reset_timer(self):
        self.current = 0.0
        self.variation = 0.0
        self.start = time.time()
        self.end = time.time()

"""my_timer = Timer()
my_timer.reset_timer()
while not my_timer.timer(20):
    print(my_timer.timer(20) * 1000, my_timer.current)"""