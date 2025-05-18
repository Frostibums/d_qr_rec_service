from enum import Enum


class Role(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"
