# pip install python-fasthtml
# http://0.0.0.0:5001
import time

#from IPython import display
from enum import Enum
from pprint import pprint
import time
from fastcore.test import *
from starlette.testclient import TestClient
from starlette.requests import Headers
from starlette.datastructures import UploadFile
from fasthtml.common import *
# for adding image a static file needed
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# Adding database with .db
def render(todo):
    tid=f'todo-{todo.id}'
    toggle=A('Toggle', hx_get=f'/toggle/{todo.id}', target_id= tid)
    delete=A('Delete', hx_delete=f'/{todo.id}',
             hx_swap= 'outerHTML', target_id= tid)
    return Li(toggle, delete,
               todo.title + ('✅' if todo.done else ''),
              id= tid)
# for production, we should put in the following live=False, but it can be True
app,rt, todos, Todo = fast_app('data/todos.db', live=False, render=render,
                               id=int, title=str, done=bool, pk= 'id')

# Mount the static directory
#app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")

# def NumList(i):
#     return Ul(*[Li(o) for o in range(i)])
def mk_input(): return Input(placeholder='Add a new todo',
                             id='title', hx_swap_oob='true'
                             )
# Header component for navigation
def Header():
    return Div(
        A('Home', href='/'), ' | ',
        A('Todos', href='/todos'), ' | ',
        A('Change', href='/change'),
        cls='header'
    )
# Home route
@rt('/')
def home():
    return Titled('Home',
                  Header(),
                  Div(P('Welcome to the Home Page! Use the links above to navigate.')))
# Todos route
@rt('/')
def get():
    # Add a description for the todo section
    description = Div(
        P("Manage your tasks efficiently by adding them to the list below."),
        P("Click 'Add' to mark a task as done, or 'Confirm it' by click on it."),
        P("Then, click 'Delete' to remove it.")
    )
    # Image to be added at the bottom
    #image = Img(src='/Users/razy/GitH projects/Fasthtml-1/Hidbrain.png', alt='Image', width='200px')
    # add components to website
    frm=Form(Group(mk_input(), Button("Add")),
             hx_post='/', target_id= 'todo-list', hx_swap= 'beforeend')
    items= [Li(o) for o in todos()]
    return Titled('Todos',
                  Header(),
                  description,
                  Card(
                  Ul(*todos(), id='todo-list'),
                  header=frm)
                  #footer=image  # Adding the image here
                  )
    # return Titled('Greeting',
    #                      Div(P('Hello! Let use fasthtml to make powerful Web Apps!')),
    #                      Div(nums, id='stuff'),
    #                      P(A('Link_href', href='/change')),
    #                      P(A('Link_hx', hx_get='/change'))
@rt('/')
def post(todo: Todo): return todos.insert(todo)

@rt('/{tid}')
def delete(tid:int): todos.delete(tid)
    
@rt('/change')
def get():
    return Titled('Change',
                Header(),
                P('Change is good! Change the link to see different of href and hx_get'),
                P(A('Home', href='/')))
@rt('/toggle/{tid}')
def get(tid: int):
    todo= todos[tid]
    todo.done=not todo.done
    return  todos.update(todo)
    # return Titled('Todos',
    #               Ul())
serve()
