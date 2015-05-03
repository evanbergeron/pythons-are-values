def makeBoard(moves):
    board = 0
    for i in xrange(0,moves):
        board = board + 8*10**i
    return board

def testMakeBoard():
    print "Testing makeBoard()...",
    assert(makeBoard(1) == 8)
    assert(makeBoard(2) == 88)
    assert(makeBoard(3) == 888)
    print "Passed!"

def testAll():
    testMakeBoard()

testAll()
