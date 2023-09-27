from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
  User(
    id=UUID("34ae350b-3e08-4e6e-8fe5-9c27eaf2ff2f"),
    first_name="Nghia",
    last_name="Nguyen",
    gender=Gender.male,
    roles=[Role.student]
  ),
  User(
    id=UUID("919b55f4-f804-4601-8dc1-fc86c4867a2e"),
    first_name="Thuy",
    last_name="Hoang",
    gender=Gender.female,
    roles=[Role.admin, Role.user]
  )
]

@app.get('/')
async def root():
  return {"firstName": "Nghia"}

@app.get('/api/v1/users')
async def fetch_users():
  return db

@app.post('/api/v1/user')
async def add_user(user:User):
  db.append(user)
  return {"id": user.id}

@app.delete('/api/v1/user/{user_id}')
async def delete_user(user_id:UUID):
  for user in db:
    if user.id == user_id:
      db.remove(user)
      return
  raise HTTPException(
    status_code=404,
    detail=f"user with id: {user_id} does not exists"
  )

@app.put('/api/v1/user/{user_id}')
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
  for user in db:
    if user.id == user_id:
      if user_update.first_name is not None:
        user.first_name = user_update.first_name
      if user_update.last_name is not None:
        user.last_name = user_update.last_name
      if user_update.middle_name is not None:
        user.middle_name = user_update.middle_name
      if user_update.roles is not None:
        user.roles = user_update.roles
      if user_update.gender is not None:
        user.gender = user_update.gender
      return
  raise HTTPException(
    status_code=404,
    detail=f"user with id: {user_id} does not exists"
  )