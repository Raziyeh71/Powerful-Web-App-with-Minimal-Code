# pip install python-fasthtml
# http://0.0.0.0:5001
import time

#from IPython import display
from enum import Enum
from pprint import pprint

from fastcore.test import *
from starlette.testclient import TestClient
from starlette.requests import Headers
from starlette.datastructures import UploadFile
from fasthtml.common import *
# adding data base with .db
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


# def NumList(i):
#     return Ul(*[Li(o) for o in range(i)])
def mk_input(): return Input(placeholder='Add a new todo',
                             id='title', hx_swap_oob='true'
                             )

@rt('/')
def get():
    # add components to website
    #nums=NumList(5)
    #todos.insert(Todo(title='Second todo', done=False))
    frm=Form(Group(mk_input(), Button("Add")),
             hx_post='/', target_id= 'todo-list', hx_swap= 'beforeend')
    items= [Li(o) for o in todos()]
    return Titled('Todos',
                  #Div(*items),
                  Card(
                  Ul(*todos(), id='todo-list'),
                  header=frm)
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