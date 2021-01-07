#! python3

'''
This program will launch a browser, go to the set solver game
and automatically solve it for you. Satisfying to write, deeply
unsatisfying to run. url: https://www.setgame.com/set/puzzle
'''

import bs4, sys, requests, os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NAMEFILL = [ 'SOLID', 'STRIPED', 'EMPTY']
NAMESHAPE = ['SQUIGGLE', 'DIAMOND', 'OVAL']
NAMECOLOR = ['RED', 'PURPLE', 'GREEN']

def CardToString(card):
    c = NAMEFILL[card[0]-1] + ',  '
    c += NAMESHAPE[card[1]-1] + ',  '
    c += NAMECOLOR[card[2]-1] + ', '
    c += str(card[3])

    return c


def imagenumToList(imgnum):
    # Pass the image number that corresponds to the set quiz website.
    # Returns a list with a card including fill, shape, color, and number
    # Represented by 3 numbers each. The visual associated with each
    # card pattern is unimportant for solving this, but we may want to 
    # associate these numbers to constant labels if we want human readable
    # reporting in the future.

    imgnum = int(imgnum)-1

    fill = imgnum // 27
    rem = imgnum % 27

    shape = rem // 9
    rem = rem % 9

    color = rem // 3

    num = rem % 3

    return [fill+1, shape+1, color+1, num+1]


def imageListToBoard(imglist):
    b = []
    for n in imglist:
        b += [imagenumToList(n)]
    return b


def isSequence(i, c1, c2, c3):
    # Are they all the same? Or are they one of each?
    if (c1[i] == c2[i] and c2[i] == c3[i]) or (c1[i] + c2[i] + c3[i] == 6):
        return True
    else:
        return False 


def isSolution(c1, c2, c3):
    return isSequence(0, c1, c2, c3) and isSequence(1, c1, c2, c3) and \
        isSequence(2, c1, c2, c3) and isSequence(3, c1, c2, c3)


def bruteForceIt(board):
    solution = []
    for c1 in range(len(board)):
        for c2 in range(c1+1, len(board)):
            for c3 in range(c2+1, len(board)):    
                if isSolution(board[c1], board[c2], board[c3]):
                    solution.append([c1, c2, c3])
    return solution
                 
                    
def main():
    # Get website into a request object
    res = requests.get(f'https://www.setgame.com/set/puzzle')
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
        sys.exit()


    # Use beautiful soup to get all of the image ID numbers into an
    # ordered list.
    pageSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    imgElems = pageSoup.select('div[class="set-card-td"] img')

    imageNums = []
    for img in imgElems:
        n = os.path.basename(img.get('src')).split('.')[0]
        imageNums.append(int(n))


    # Convert the list of image numbers into a 2 dim board list (list of cards
    # where each card consists of 4 characteristics, fill, shape, color, number)
    board = imageListToBoard(imageNums)


    # Get the solution into a list with button groups with each
    # button numbered 1-12
    solutionSets = bruteForceIt(board)
    
   
    # Use Selenium to launch the browser and click the buttons for
    # those numbers.
    browser = webdriver.Firefox()
    browser.get('https://www.setgame.com/set/puzzle')
    cookieElem = browser.find_element_by_class_name('agree-button')
    cardElems = browser.find_elements_by_class_name('set-card-td')

    cookieElem.click()
    time.sleep(1)

    for set in solutionSets:
        for i in set:        
            cardElems[i].click()
    

main()
