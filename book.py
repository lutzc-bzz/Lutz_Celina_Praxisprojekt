"""Praxisprojekt: Book Reviewer - Lutz Celina"""


from dataclasses import dataclass


@dataclass
class Book:
    """Book class"""

    book_id: int
    title: str
    author: str
    release_date: str
    average_rating: int
