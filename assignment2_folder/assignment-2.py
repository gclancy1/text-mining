import urllib.request
import pickle
import re

def get_book(book):
    """
    Takes a URL from gutenberg.org and returns the text of the book
    """
    url = f'{book}'
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text.lower()

def get_all_books(chosen_dict):
    """
    takes dictionary of titles and gutenberg urls and dumps to the drive using pickle
    """
    master_dict = {}
    for key in chosen_dict:
        master_dict[key] = get_book(chosen_dict[key])
    with open('assignment2_folder/texts.pickle','wb') as f:
        pickle.dump(master_dict,f)

def word_hist(text):
    """
    takes a text and returns a dictionary of word frequencies
    """
    d = {}
    for word in text:
        d[word] = d.get(word,0) + 1
    return d

def top_ten(my_dict):
    """
    takes dictionary of frequency and returns list of top 10 words
    """
    with open('assignment2_folder/common_words.txt') as z:
        words = z.read().split()
    top =[]
    ranked = sorted(my_dict, key=my_dict.__getitem__,reverse=True)
    for i in range(len(ranked)):
        if ranked[i] not in words:
            top.append((ranked[i],my_dict[ranked[i]]))
    if len(top) > 10:
        del top[10:]
    return top

def print_top_ten(separate_dict):
    """
    takes a dictionary and prints the top 10 words by frequency
    """
    for key in separate_dict:
        top = top_ten(separate_dict[key])
        i = 0
        j = 0
        for i in range(10):
            for j in range(1):
                print(f'The word {top[i][j]} appears {top[i][j+1]} times in the text {str(key)}. It is ranked #{i+1} in terms of frequency')

def dickens_occurence(word,title):
    return separate_dict[title][word]/len(text_copies[title])



def main():
    chosen_dict ={
        'Bleak House':'http://www.gutenberg.org/ebooks/1023.txt.utf-8',
        'Great Expectations':'http://www.gutenberg.org/files/1400/1400-0.txt',
        'Hard Times':'http://www.gutenberg.org/files/786/786-0.txt',
        'David Copperfield':'http://www.gutenberg.org/files/766/766-0.txt',
        'War and Peace':'http://www.gutenberg.org/files/2600/2600-0.txt'
    }
    
    global separate_dict
    global text_copies
    separate_dict = {}
    # get_all_books(chosen_dict)

    ## only run line 74 once, it is then pickled
    
    with open('assignment2_folder/texts.pickle','rb') as input_file:
        text_copies = pickle.load(input_file)

    for key in text_copies:
        text_copies[key] = re.sub('[^A-Za-z0-9\']+',' ',text_copies[key])
        text_copies[key] = text_copies[key].split(' ')
    
    for key in chosen_dict:
        separate_dict[key] = word_hist(text_copies[key])
    
    print_top_ten(separate_dict)

    # print(separate_dict['War and Peace']['little'])
    LT= dickens_occurence('old','War and Peace')
    CD = (dickens_occurence('old','Great Expectations')+dickens_occurence('old', 'Bleak House')+dickens_occurence('old','Hard Times')+dickens_occurence('old','David Copperfield'))/4
    print(CD/LT)
    
    LT_2 = dickens_occurence('little','War and Peace')
    CD_2 = (dickens_occurence('little','Great Expectations')+dickens_occurence('little', 'Bleak House')+dickens_occurence('little','Hard Times')+dickens_occurence('little','David Copperfield'))/4
    print(CD_2/LT_2)

if __name__ == "__main__":
    main()
    
