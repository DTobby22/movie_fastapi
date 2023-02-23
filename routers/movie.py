from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as Movie_model
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# Devuelve un json
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# recive la id por la url
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1, le=50,)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Se puede usar varios parametros ademas de la id
@movie_router.get('/movies/', tags=['movies'])
def get_movie(id: int = Query(ge=1, le=99)):  # Mayor o igual / menor o igual
    db = Session()
    result = db.query(Movie_model).filter(Movie_model.id == id).all()  
    if not result:        
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie):
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={'message: ': 'Pelicula Registrada'}, status_code=201)


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
# recibe 2 parametros, id de tipo entero y movie de tipo lista
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Pelicula no encontrada'})
    MovieService(db).update_movie(id, movie)        
    return JSONResponse(status_code=200, content={'message: ': 'Pelicula Modificada'})


@movie_router.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = db.query(Movie_model).filter(Movie_model.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    db.delete(result)
    db.commit()   
    return JSONResponse(status_code=200, content={'message: ': 'Pelicula Eliminada'})
