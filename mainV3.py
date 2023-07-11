from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import FastAPI, Body, Path, Query #Añadimos Path y Query para hacer validacion de parámetros
from fastapi.responses import HTMLResponse, JSONResponse # Podemos retornar un JSON

app = FastAPI() #Creamos una instancia
app.title = "My app"#Establecemos un título para la aplicacion
app.version = "2.0.0"#Establecemos la versión

##VALIDACION DE ERRORS
#from pydantic import Field


##CREACION DE ESQUEMAS
'''
from pydantic import BaseModel
from typing import Optional
'''

#DEFINICION DE SCHEMA

'''
PROPIEDADES DE SCHEMA
gt: greater than
ge: greater than or equal
lt: less than
le: less than or equal

'''

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2023)
    rating: float
    category: str

#RELLENAR LOS CAMPOS VACIOS POR DEFECTO

    class Config:
        schema_extra = {
            "example": {
                "id" : 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": "2023",
                "rating": "5",
                "category": "Default",
            }

        }

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
    return HTMLResponse('<h1>Hello world!</h1>')

#Ruta para recibir el listado de películas como JSON
@app.get('/movies', tags=["Json Format"])
def get_movies():
    return JSONResponse(content=movies) #Retorno JSON

#Ruta para recibir parámetros con validacion
@app.get('/movies/{id}', tags=["MovieById"])
def get_movies(id:int = Path(ge=1, le=2000)):#Notese el uso de path
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)#Retorno JSON
        return JSONResponse(content=[]) #Retorna JSON vacío en caso de no encontrar coincidencias.

#Obtengamos un objeto por categoría con querys aplicando validación
@app.get('/movies/', tags=['moviesByQuerys'])
def get_movies_by_cat(category: str = Query(min_length=5, max_length=100)):
        data = [item for item in movies if item["category"]==category]
        return JSONResponse(content=data) #retorna JSON


#TRABAJANDO CON EL MÉTODO POST USANDO SCHEMAS
@app.post('/movies', tags=['moviesWithSchemas'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado correctamente la película"})

#TRABAJADO CON EL METODO PUT USANDO SCHEMAS
@app.put('/movies/{id}', tags=["moviesWithSchemas"])
def update_movie(id: int, movie: Movie):
    
    for item in movies:
        if item['id'] == id:

            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
        
            return JSONResponse(content={"message": "Se ha modificado correctamente la película"})
        
@app.delete('/movies/{id}', tags=["movies"])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se ha elminidado correctamenta la película"})