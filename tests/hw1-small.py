# hw1.py
# Evan Bergeron + ebergero + Section N

######################################################################
# Place your non-autograded solutions below here!
######################################################################
#
# Be sure to start each line with a "#" so it is a Python comment!
# Also be sure to show your work.  Provide some simple explanation
# as to how you derived your solution.  Don't be too detailed, just
# enough so we can follow your logic.
#
# 1.
# a. State and prove any of DeMorgan's laws using truth tables.
#    not(a and b) is logically equivalent to (not a) or (not b)
#    a | b | (not a) | (not b) | (a and b) | not(a and b) | (not a) or (not b)
#    T | T |   F     |    F    |     T     |      F       |         F
#    T | F |   F     |    T    |     F     |      T       |         T
#    F | T |   T     |    F    |     F     |      T       |         T
#    F | F |   T     |    T    |     F     |      T       |         T
#
# b. x and True. If x is "truthy," ("truthy" and True) is True.
#    If x is False, (False and True) is False.
#
# c. Whole numbers.
#
# d. 3*3 evaluates to 9.
#    '3'*3 evaluates to '333'.
#    Though the operator is the same, the types of the operands differ.
#    Thus, the semantics of the operator differ and the outputs are different.
#
# 2. h(9,13): return f(g(9)) % g(f(13))
#                    f(8) % g(28)
#                    64 % 27
#                    10
# It will print 10.
#
# print f(1, 0) and g(-1,-2) and f(3,4) and g(5,6)
# f(1,0) prints "f" and returns True. The and operator tells python to move on.
# g(-1,-2) prints "g" and returns True. and operator tells python to move on.
# f(3,4) prints "f" and returns False. Short-circuit evaluation cuts off
# the statement here.
# It will print
# f g f False
#
# print h(-1, 0) or h(0, 1) or h(1, 2) or h(2, 3)
# h(-1,0) prints "h" and returns 0 (which is equivalent to False). This False
# combined with the or operator tells Python to move on.
# h(0,1) prints "h" and returns 0. The above process is repeated.
# h(1,2) prints "h" and returns 2, which is a "truthy" value. Because the
# logical operator here is and, short-circuit evaluation cuts Python off.
# It will print
# h h h 2
#
# All told, running the code will print both lines like so:
# f g f False
# h h h 2
#
# 3. x = 30, y = 10. They are both integers between 0 and 100 with x > y.
#   (x % 10 == y % 10 == 0) is True.
#   (x == y * 3) is True.
#   (x/10 + x%10 + y/10 + y%10 == 3 + 0 + 1 + 0 < 5) is True.
#   Thus, f(30,10) returns True.
#
#   x = 38, y = 11. x - x/y*y is equivalent to x % y.
#   38 and 11 are both integers. 38 % 11 is 5. 40 > 38 > 30. 13 > 11 > 10.
#
# 4. def findRoot(a, b, c):
#    return (a != 0) and \
#           (b**2 - 4*a*c > 0) and \
#           max(
#               (-b+(b**2 - 4*a*c))**.5 / (2*a),
#               (-b-(b**2 - 4*a*c))**.5 / (2*a)
#              )
#
# 5. Bonus 1: they must be additive inverses.
#    Bonus 2: def r(x,y):
#                 return (x*y == 0)*1 or x+r(r(x/3,y/4),x/5)
#             print r(5,3)
#                   (5*3 == 0)*1 or 5+r(r(5/3,3/4),5/5)
#                   (False)*1 or 5+r(r(1,0),1)
#                   0 or 5+r(r((0 == 0)*1 or ...),1)
#                   0 or 5+(r(1,1))
#                   0 or 5+((1==0)*1 or 1 + r(r(0,0),0))
#                   0 or 5+(0 or 1 + r(r(0,0),0))
#                   0 or 5+(0 or 1 + r(1,0))
#                   0 or 5+(0 or 1 + 1)
#                   0 or 5+2
#                   7

######################################################################
# Place your autograde solutions below here
######################################################################

def kthDigit(x, k): # Passed
    return (abs(x) / (10**k) % 10)

def numberOfPoolBalls(rows): # Passed
    # Just the sum of the first n natural numbers.
    return rows * (rows + 1) / 2

def numberOfPoolBallRows(balls): # Passed
    # Inverse of above using quadratic formula and ceiling function.
    # Added abs() for isTriangular function below.
    return round((.5 * (-1 + (8 * abs(balls) + 1) ** .5)) + .49)

def isEvenPositiveInt(x): # Passed
    # Was important to have the type check first.
    return (type(x) == int) and (x % 2 == 0) and (x > 0)

def isPerfectCube(x): # Passed
    # almostEqual, basically.
    epsilon = 0.00001
    return abs((round(abs(x)**(1.0/3)) - abs(x)**(1.0/3))) < epsilon

def isTriangular(x): # Passed
    # First arrange the x-many balls into triangles as described. Take this number of rows and make a full triangle with that many rows. Count the balls in this new triangle. If the number of pool balls in this new triangle equal the original number of balls you had, your original number was triangular.
    return (x == numberOfPoolBalls(numberOfPoolBallRows(x)))

def fabricYards(inches): # Passed
    return (inches + 35) / 36

def fabricExcess(inches): # Passed
    return 36*fabricYards(inches) - inches

def nearestBusStop(street): # Passed
    return 8*((street + 3) / 8)

def areCollinear(x1, y1, x2, y2, x3, y3): # Passed
    # Three points form a triangle. If the biggest side of the triangle
    # adds up to the sum of the other two, it's not a triangle, but a line.
    epsilon = 0.0001
    sideLength1 = ((x1-x2)**(2) + (y1-y2)**(2))**(0.5)
    sideLength2 = ((x1-x3)**(2) + (y1-y3)**(2))**(0.5)
    sideLength3 = ((x3-x2)**(2) + (y3-y2)**(2))**(0.5)
    trianglePerimeter = sideLength1 + sideLength2 + sideLength3
    biggestSide = max(sideLength1, sideLength2, sideLength3)
    return (trianglePerimeter - biggestSide) - biggestSide < epsilon

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
