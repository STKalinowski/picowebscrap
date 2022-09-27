import collections 
import re 
def main ( ) : 
    with open ( 'text_file.txt' , 'r' ) as f : 
        words = re.findall('[a-z]+', f.read().lower()) 
        print(collections.Counter(words).most_common()) 

if __name__ == '__main__' : 
    main ( )
