import uvicorn
import json
from datetime import datetime
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import user_router, db, image_router

#-------------------FASTAPI-------------------
app = FastAPI(
    title='API',
    description='',
    version='0.0.1',
    contact={
        'name': 'Vo Cuong Thinh',
        'email': '52000599@student.tdtu.edu.vn'
    },
    docs_url="/docs", redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(user_router.router)
app.include_router(image_router.router)
app.include_router(db.router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app' ,
        host=config('HOST', '0.0.0.0'),
        port=int(config('PORT', 8000)),
        reload=True
    ) 