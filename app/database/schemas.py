import datetime
from typing import Optional, List
from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr, validator, Field, HttpUrl

from utils import hashing


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class UserBase(BaseModel):
    username: str = Field("default_username", description="The user's username")
    email: EmailStr = Field("default@example.com", description="The user's email address")

    class Config:
        str_min_length = 1
        str_strip_whitespace = True


class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class UserWithPassword(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserCreate(UserBase):
    password: str = Field("default_password123", description="The user's password")
    first_name: str = Field("John", description="The user's first name")
    last_name: str = Field("Doe", description="The user's last name")
    phone_number: str = Field("123-456-7890", description="The user's phone number")

    # Combined password validation and hashing in one validator
    @validator('password')
    def password_strength_and_hash(cls, value):
        # Password strength check
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one number')

        # Hash the password
        return hashing.hash_password(value)

    # Validator for phone number format (if provided)
    @validator('phone_number')
    def phone_number_format(cls, value):
        if value and len(value) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return value


class AnnouncementSchema(BaseModel):
    title: str = Field(..., description="Title of the announcement")
    category_id: int
    photo: Optional[UploadFile] = File(None)
    photo_url: Optional[HttpUrl] = None
    description: Optional[str] = Field(None, description="Detailed description of the announcement")
    location: Optional[str] = Field(None, description="Location of the announcement")

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str = Field(..., description="Name of the category")


class CategorySchemaWithCount(BaseModel):
    id: int
    name: str
    announcements_count: int
    announcements: Optional[List[AnnouncementSchema]] = Field(None,
                                                              description="List of announcements under this category")

    class Config:
        orm_mode = True
