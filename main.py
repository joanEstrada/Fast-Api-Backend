from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse #Para retornar un html

app = FastAPI() #Creamos una instancia
app.title = "My app"#Establecemos un título para la aplicacion
app.version = "0.0.1"#Establecemos la versión

##CREACION DE ESQUEMAS
from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel): #Hereda de la clase BaseModel
    #Defino los atributos de la clase movie
    ##Para id, existen dos maneras de definirlo como atributo de clase:
    '''
    #1
    id: int | None = None #Id podría ser entero o ninguno y por defecto se podría asignar ninguno.
    '''    
    #2
    id: Optional[int] = None
    title: str
    overview: str
    year: str
    rating: float
    category: str

#CORS
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Supongamos un diccionario como fuente de datos
movies = [

    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Super Mario Bros',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Drama'    
    },        
    {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Fantasy'    
    } 


]

#creamos un endpoint
'''
#Default endpoint
@app.get('/')
'''
@app.get('/', tags=['home']) #Agregamos un tag a la ruta

def message():
    '''
    #Return por defecto
    return "Hello world!"

    #podría retornarse un diccionario
    return {"Hello":"World"}
    '''
    
    #podría retornarse un http pero importando una clase
    return HTMLResponse('<h1>Hello world!</h1>')
    
#Ruta para mostrar un diccionario    GET
@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

#Ruta para recibir parámetros   GET with parameters
@app.get('/movies/{id}', tags=["MovieById"])
def get_movies(id:int):#toma el id que digita el usuario y su tipo
    
    '''
    #Algoritmo de filtrado
    #auxiliar
    i = 0
    for index in movies:
        dictionary = index
        if dictionary['id'] == id:

            print(movies[id-1])
            return movies[id-1]
            break             
    i+=1
    '''

    for item in movies:
        if item["id"] == id:
            return item
        return [] #Retorna un objeto vacío en caso de no encontrar coincidencias.

'''
#Obtengamos un objeto por categoría con querys
@app.get('/movies/', tags=['moviesByQuerys'])
def get_movies_by_cat(category: str, year: int):
        return category+year
'''

#Obtengamos un objeto por list comprehension (más optima)
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return [movie for movie in movies if movie['genre'] == category]

#trabajando con método post 
#EJEMPLO DE ENVÍO
#http://127.0.0.1:8000/moviess?id=3&title=sda&overview=asd&year=123&rating=32&category=sadf
@app.post('/movies', tags=["movies_prev"])
def create_movie(
        id: int,
        title: str,
        overview: str,
        year: int,
        rating: float,
        category: str ):
    return title


#trabajando con método post pero estableciendo que el contenido estará en el body
#de la peticion
'''
@app.post('/movies', tags=["moviesPost"])
def create_movie(
        id: int = Body(),
        title: str = Body(),
        overview: str = Body(),
        year: int = Body(),
        rating: float = Body(),
        category: str = Body()):
    
    movies.append({
        "id" : id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category,
    })
    return movies
'''
#PARA USAR UN APPLICATION/JSON 
@app.post('/movies', tags=['moviesPost'])
def create_movie(id: int = Body(), title: str = Body(), overview:str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies

#Usando métodos put por ID
@app.put('/movies/{id}', tags=["movies"])
def update_movie(id: int, title: str = Body(), overview:str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):
    
    for item in movies:
        if item['id'] == id:

            item['title']=title,
            item['overview']=overview,
            item['year']=year,
            item['rating']=rating,
            item['category']=category,
        
        return movies
    
@app.delete('/movies/{id}', tags=["movies"])
def delete_movie(id: int):    
        for item in movies:
            if item['id']==id:
                movies.remove(item)
            return movies
        
#TRABAJANDO CON EL MÉTODO POST USANDO SCHEMAS
@app.post('/movies', tags=['moviesWithSchemas'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

#TRABAJADO CON EL METODO PUT USANDO SCHEMAS
@app.put('/movies/{id}', tags=["moviesWithSchemas"])
def update_movie(id: int, movie: Movie):
    
    for item in movies:
        if item['id'] == id:

            item['title']=movie.title,
            item['overview']=movie.overview,
            item['year']=movie.year,
            item['rating']=movie.rating,
            item['category']=movie.category,
        
        return movies