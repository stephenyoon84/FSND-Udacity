import turtle

brad = turtle.Turtle()
brad.shape("turtle")
brad.color("blue")
brad.speed(20)
eq_tri = turtle.Turtle()
eq_tri.shape("circle")
eq_tri.color("green")
eq_tri.speed(20)
angie = turtle.Turtle()
angie.shape("arrow")
angie.color("yellow")
angie.speed(20)
window = turtle.Screen()
window.bgcolor("red")

def draw_square():
    i = 0
    while i < 2:
        brad.forward(100)
        brad.right(40)
        brad.forward(100)
        brad.right(140)
        i += 1

def draw_360square(a):
    i = 0
    k = 360.0/a
    while i < k:
        draw_square()
        brad.right(a)
        i += 1

def draw_regular_triangle():
    i = 0
    while i < 3:
        eq_tri.forward(100)
        eq_tri.right(120)
        i += 1

def draw_360circle(a):
    i = 0
    k = 360.0/a
    while i < k:
        angie.circle(40)
        angie.right(a)
        i += 1

def draw_360tri(a):
    i = 0
    k = 360.0/a
    while i < k:
        draw_regular_triangle()
        eq_tri.right(a)
        i += 1

def draw_art(a, b, c):
    draw_360square(a)
    draw_360tri(b)
    draw_360circle(c)
    brad.right(90)
    brad.forward(300)
    brad.right(100)
    draw_square()
    brad.right(120)
    draw_square()

draw_art(15,20,5)

window.exitonclick()
