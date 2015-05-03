# hw2.py
# Evan Bergeron + ebergero + Section N

"""
######################################################################
# 15-112 Fall 2013 Quiz 2 [20pts]
######################################################################

1.
    a. With one line of code, draw a circle of radius 5 centered in the region
    bounded by (50,100) and (250,200).

        canvas.create_oval(145, 145, 155, 155)

    b. Explain in just a few words what anchor=SE means when drawing text.

        The anchor point will be the text's bottom right. So the text will
        show above and to the left of the given anchor point.

    c.
        not f(x) and g(y)

    d. Rewrite the following function so it works equivalently but uses a for
    loop instead of a while loop (you may assume x is a non-negative integer):

        def f(x):
            a = -x
            b = 0
            for i in xrange(-x, x + 1, 3):
                b += g(a)
            return b

2. Indicate what each will print:

    def f(x,y):
        m = 0
        for z in xrange(2,x,y):
            if (x%z == m):
                print "A",
                m += 1
            elif (y + z > x):
                print "B",
            print (z if (z%3 == 2) else "C"),
        print
    f(12, 4)

    So z takes 3 values: 2, 6, and 10.
    For z = 2, 10%2 == m (0) is true, so it prints 'A' and increments m by one.
    Then, because 2%3 == 2, it prints z which is 2.
    For z = 6, 10%6 != 1 and 4 + 6 < 12 and 6%3 != 2, it prints 'C'.
    For z = 10, 12%10 != 1 but 4 + 10 > 12, so it prints 'B'. 10%3 != 2, so it
    prints 'C'.

        Thus, it prints: '  A 2 C B C'.

    def g():
        for x in xrange(-1,5,2):
           print x, ":",
           for y in xrange(x, -x, -2):
               print y,
           print
    g()

    x will equal -1,1, and 3.

    It will print:
    -1 :
    1 : 1
    3 : 3 1 -1

3. Find arguments for the following functions that make them return True.

    def f(x, y):
            assert((type(x) == int) and (type(y) == int))
            if ((x <= 50) or (y > 25)): z = 3
            elif (x%10 + y%10 > 0): z = 42
            elif (x == y + 40): z = 10
            else: z = 5
            return (z == 2**5/3)

    2**5/3 = 32/3 = 10. Thus, (x == y + 40) must return True, (x%10 + y%10 > 0)
    must return False, and ((x <= 50) or (y > 25)) must return False.
    (x%10 + y%10 > 0) is False implies x%10 and y%10 are 0.
    ((x <= 50) or (y > 25)) is False. x = 60, y =20 makes these False.

    x = 60, y = 20

    def g(z):
        total = 0
        while (z > 0):
            for y in range(0,z,2):
                total += 1
            z -= 2
        return ((z == 0) and (total == 1+2+3+4+5))

    z = 10 returns True. When z = 10, the for loop runs 5 times. When z = 8,
    the loop runs 4 times. And so on. When z = 2, it runs once. After that,
    z = 0 so the while loop is broken. By then total = 5+4+3+2+1 = 15 and
    z = 0. Thus, the function returns True.

4. A number n is perfect if it is an integer and it equals the sum of all its
    factors between 1 (inclusive) and itself (exclusive).  For example, 28 is
    perfect because the factors of 28 are 1, 2, 4, 7, and 14, and 1 + 2 + 4 + 7
    + 14 = 28.  With this in mind, write the function isPerfect(n) that takes a
    possibly-non-integer value and returns True if it is a perfect number and
    False otherwise.  Your function may not crash for any value of n.

    def isPerfect(x):
        if type(x) != int and type(x) != float: return False
        if (int(x) - x) != 0: return False
        x = int(x)
        sum = 0
        for i in xrange(1,x):
            if (x % i == 0): sum += i
        return (sum == x)

5. Indicate what each will print:

    def q():
        def f(x): return x+2*f(x-1) if (x>0) else 1
        def g(x): return f(x/2)*x/2
        x = "f(g(3))"
        (y,f,g) = (eval(x), eval(x)/len(x), eval(x)%5)
        return y+eval(x.replace("(","+").replace(")",""))
    print q()

    return y+eval(x.replace("(","+").replace(")","")) is the same as
    return y + f + g + 3, which is
    return f(g(3)) + (f(g(3)) / 7) + (f(g(3)) % 5) + 3
    f(g(3)) = f(f(3/2)*3/2)
            = f(f(1)*3/2)
            = f((1+2*1)*3/2)
            = f(9/2)
            = f(4)
            = 4 + 2*f(3)
            = 4 + 2*(3 + 2*f(2))
            = 4 + 2*(3 + 2*(2+2*f(1)))
            = 4 + 2*(3 + 2*(2+2*(1+2*f(0))))
            = 4 + 2*(3 + 2*(2+2*(1+2*1)))
            = 4 + 2*(3 + 2*(2+2*3))
            = 4 + 2*(3 + 2*(8))
            = 4 + 2*(19)
            = 42
    return 42 + (42 / 7) + (42 % 5) + 3
    return 42 + 6 + 2 + 3
    return 53
    53

    def r(x,y,z=0):
        while (x*y > 0): (x,y,z) = (y/(2+x%7),x/(2+y%3),x+y-z)
        return z
    print r(57,15)

    First iteration: (x,y,z) goes from (57,15,0) to (15/3,57/2,72) = (5,28,72).
    Second: (x,y,z) = (28/7,5/3,-39) = (4,1,-39).
    Third: (x,y,z) = (0, 4/(3), 44) = (0,1,44)
    Now x*y = 0. r(x,y,z=0) then prints z = 44.

"""

######################################################################
# Place your non-graphics solutions here! [40pts]
######################################################################

def makeBoard(moves):
    board = 0
    for i in xrange(0,moves):
        board += 8*10**i
    return board

def digitCount(n):
    if n == 0:
        return 1
    return int(__import__("math").log(abs(n), 10)) + 1

def kthDigit(n, k):
    return (abs(n) / (10**abs(k))) % 10

def replaceKthDigit(n, k, d):
    righthandDigits = abs(n) % (10**k)
    lefthandDigits = abs(n) / (10**k)
    lefthandDigits = lefthandDigits - (lefthandDigits % 10) + d
    return (lefthandDigits * (10**k)) + righthandDigits

def getLeftmostDigit(n):
    return kthDigit(n, digitCount(n)-1)

def clearLeftmostDigit(n):
    return replaceKthDigit(n, digitCount(n)-1, 0)

# Don't think will work
def makeMove(board, position, move):
    if move != 1 and move != 2:
        return "move must be 1 or 2!"
    if position > digitCount(board) or position == 0:
        return "offboard!"
    if (kthDigit(board, digitCount(board) - position) == 1 or
        kthDigit(board, digitCount(board) - position) == 2):
        return "occupied!"
    if kthDigit(board, digitCount(board) - position) == 8:
        board = replaceKthDigit(board, digitCount(board) - position, move)
    return board

def isWin(board):
    for digit in xrange(0, digitCount(board) + 1):
        if board % 1000 == 112:
            return True
        board = board / 10
    return False

def isFull(board):
    for digit in xrange(0, digitCount(board) + 1):
        if board % 10 == 8:
            return False
        board = board / 10
    return True

def play112(game):
    currentPlayer = 1
    board = makeBoard(getLeftmostDigit(game))
    game = clearLeftmostDigit(game)
    for x in range(0, (digitCount(game))/2):
        position = getLeftmostDigit(game)
        game = clearLeftmostDigit(game)
        move = getLeftmostDigit(game)
        game = clearLeftmostDigit(game)
        if move != 1 and move != 2:
            return str(board) + ": Player " +\
            str(currentPlayer) + ": move must be 1 or 2!"
        if kthDigit(board, digitCount(board) - position) != 8:
            return str(board) + ": Player " +\
            str(currentPlayer) + ": occupied!"
        if position > digitCount(board):
            return str(board) + ": Player " +\
            str(currentPlayer) + ": offboard!"
        board = makeMove(board, position, move)
        currentPlayer = (currentPlayer % 2) + 1
    currentPlayer = (currentPlayer % 2) + 1
    if isWin(board):
        return str(board) + ": Player " +\
        str(currentPlayer) + " wins!"
    if not(isFull(board)):
        return str(board) + ": Unfinished!"
    else:
        return str(board) + ": Tie!"

######################################################################
##### ignore_rest: The autograder will ignore all code below here ####
######################################################################

######################################################################
# Tests
######################################################################


def testDigitCount():
    print "Testing digitCount()...",
    assert(digitCount(0) == 1)
    assert(digitCount(5) == digitCount(-5) == 1)
    assert(digitCount(42) == digitCount(-42) == 2)
    assert(digitCount(121) == digitCount(-121) == 3)
    print "Passed!"

def testKthDigit():
    print "Testing kthDigit()...",
    assert(kthDigit(789, 0) == kthDigit(-789, 0) == 9)
    assert(kthDigit(789, 1) == kthDigit(-789, 1) == 8)
    assert(kthDigit(789, 2) == kthDigit(-789, 2) == 7)
    assert(kthDigit(789, 3) == kthDigit(-789, 3) == 0)
    assert(kthDigit(789, 4) == kthDigit(-789, 4) == 0)
    print "Passed!"

def testReplaceKthDigit():
    print "Testing replaceKthDigit()...",
    assert(replaceKthDigit(789, 0, 6) == 786)
    assert(replaceKthDigit(789, 1, 6) == 769)
    assert(replaceKthDigit(789, 2, 6) == 689)
    assert(replaceKthDigit(789, 3, 6) == 6789)
    assert(replaceKthDigit(789, 4, 6) == 60789)
    print "Passed!"

def testGetLeftmostDigit():
    print "Testing getLeftmostDigit()...",
    assert(getLeftmostDigit(7089) == 7)
    assert(getLeftmostDigit(89) == 8)
    assert(getLeftmostDigit(9) == 9)
    assert(getLeftmostDigit(0) == 0)
    print "Passed!"

def testClearLeftmostDigit():
    print "Testing clearLeftmostDigit()...",
    assert(clearLeftmostDigit(60789) == 789)
    assert(clearLeftmostDigit(789) == 89)
    assert(clearLeftmostDigit(89) == 9)
    assert(clearLeftmostDigit(9) == 0)
    assert(clearLeftmostDigit(0) == 0)
    print "Passed!"

def testMakeMove():
    print "Testing makeMove()...",
    assert(makeMove(8, 1, 1) == 1)
    assert(makeMove(888888, 1, 1) == 188888)
    assert(makeMove(888888, 2, 1) == 818888)
    assert(makeMove(888888, 5, 2) == 888828)
    assert(makeMove(888888, 6, 2) == 888882)
    assert(makeMove(888888, 6, 3) == "move must be 1 or 2!")
    assert(makeMove(888888, 7, 1) == "offboard!")
    assert(makeMove(88888888, 0, 1) == "offboard!") # FIX THIS EDGE CASE
    assert(makeMove(888881, 6, 1) == "occupied!")
    print "Passed!"

def testIsWin():
    print "Testing isWin()...",
    assert(isWin(888888) == False)
    assert(isWin(112888) == True)
    assert(isWin(811288) == True)
    assert(isWin(888112) == True)
    assert(isWin(211222) == True)
    assert(isWin(212212) == False)
    print "Passed!"

def testIsFull():
    print "Testing isFull()...",
    assert(isFull(888888) == False)
    assert(isFull(121888) == False)
    assert(isFull(812188) == False)
    assert(isFull(888121) == False)
    assert(isFull(212122) == True)
    assert(isFull(212212) == True)
    print "Passed!"

def testPlay112():
    print "Testing play112()...",
    assert(play112( 5 ) == "88888: Unfinished!")
    assert(play112( 521 ) == "81888: Unfinished!")
    assert(play112( 52112 ) == "21888: Unfinished!")
    assert(play112( 5211231 ) == "21188: Unfinished!")
    assert(play112( 521123142 ) == "21128: Player 2 wins!")
    assert(play112( 521123151 ) == "21181: Unfinished!")
    assert(play112( 52112315142 ) == "21121: Player 1 wins!")
    assert(play112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(play112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(play112( 51211 ) == "28888: Player 2: occupied!")
    assert(play112( 5122221 ) == "22888: Player 1: occupied!")
    assert(play112( 51261 ) == "28888: Player 2: offboard!")
    assert(play112( 51122324152 ) == "12212: Tie!")
    print "Passed!"

def testAll():
    testMakeBoard()
    testDigitCount()
    testKthDigit()
    testReplaceKthDigit()
    testGetLeftmostDigit()
    testClearLeftmostDigit()
    testMakeMove()
    testIsWin()
    testIsFull()
    testPlay112()

######################################################################
# Main: you may modify this to run just the parts you want to test
######################################################################

def main():
    testAll()

if __name__ == "__main__":
    main()
