import os

def get_ant():
    return 1,2
    
def write_file():
    pass

def process():
    for i in range(0, 3):
        print 'loop ',i
        os.system('hadoop jar /code/hadoop-streaming.jar \
-file /code/mapper.py    -mapper /code/mapper.py \
-file /code/reducer.py   -reducer /code/reducer.py \
-input /input/* -output /output_{}'.format(i))    
            
    
if __name__ == '__main__':
    process()