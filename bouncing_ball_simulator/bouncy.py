# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 22:52:40 2021

@author: hmates
"""


import turtle
import random

wn = turtle.getscreen()
wn.bgcolor("black")
wn.title("Bouncing Ball Simulator")
wn.tracer(0)

balls = []

for _ in range(25):
    balls.append(turtle.Turtle())
    

colors = ["red", "blue"]
shapes = ["circle"]

for ball in balls:
    ball.shape(random.choice(shapes))
    ball.color(random.choice(colors))
    ball.penup()
    ball.speed(0)
    x = random.randint(-390, 390)
    y = random.randint(200, 500)
    ball.goto(x,y)
    ball.dy = 0
    ball.dx = random.randint(-5, 5)
    ball.da = random.randint(-7, 7)

gravity = 0.05

while True:
    wn.update()   
    
    for ball in balls:
        ball.rt(ball.da)
        ball.dy -= gravity
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)
        
        #check for a wall collision
        if ball.xcor() > 400:
            ball.dx *= -1
            ball.da *= -1
            
        if ball.xcor() < -400:
            ball.dx *= -1
            ball.da *= -1
        
        #check for a bounce
        if ball.ycor() < -400:
            ball.sety(-400)
            ball.dy *= -1
            ball.da *= -1
            
        #check for collision between balls
        for i in range(0, len(balls)):
            for j in range(i+1, len(balls)):
                #check for a collision
                if balls[i].distance(balls[j]) < 25:
                    balls[i].dx, balls[j].dx = balls[j].dx, balls[i].dx
                    balls[i].dy, balls[j].dy = balls[j].dy, balls[i].dy

        
            
            
        



