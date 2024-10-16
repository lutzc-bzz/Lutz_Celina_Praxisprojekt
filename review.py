"""Praxisprojekt: Book Reviewer - Lutz Celina"""


from dataclasses import dataclass


@dataclass
class Review:
    """Review class"""

    review_id: int
    user_id: int
    book_id: int
    rating: int
    comment: str
    review_date: str
