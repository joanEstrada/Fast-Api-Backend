from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse 

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
    '''
    #Return por defecto
    return "Hello world!"

    #podría retornarse un diccionario
    return {"Hello":"World"}
    '''
    
    #podría retornarse un http pero importando una clase
    return HTMLResponse('<h1>Hello world!</h1>')

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

            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
        
            return movies