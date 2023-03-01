from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie
from fastapi import HTTPException

movie_router = APIRouter(dependencies=[Depends(JWTBearer())])



@movie_router.get('/movies')
def get_movies():
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.get('/movies/{id}')
def get_movie(id: int):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.post('/movies')
def create_movie(movie: Movie):
    db = Session()
    try:
        MovieService(db).create_movie(movie)
    except:
        raise HTTPException(
            status_code=400, detail="Error al crear la película.")
    return JSONResponse(content={'message': 'Pelicula registrada'})


@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie): # recibe 2 parametros, id de tipo entero y movie de tipo lista
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'Pelicula no encontrada'})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={'message: ': 'Pelicula Modificada'})


@movie_router.delete('/movies/{id}')
def delete_movie(id: int):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'No encontrado'})
    MovieService(db).delete_movie(result)
    return JSONResponse(content={'message: ': 'Pelicula Eliminada'})
