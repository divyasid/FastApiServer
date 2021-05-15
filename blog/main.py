from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
import database
from sqlalchemy.orm import Session


app = FastAPI()

models.database.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE BLOG
@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

# DELETE A SPECIFIC BLOG
@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def destroy(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with id {id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

# UPDATE A BLOG
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    d = {}
    for i,j in request:
        d[i] = j
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with id {id} not found")
    
    blog.update(d)
    db.commit()
    return 'updated'


# GET ALL BLOGS
@app.get('/blog')
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# GET SPECIFIC BLOG
@app.get('/blog/{id}',status_code=200)
async def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f"Blog with the id {id} is not available")
    return blog