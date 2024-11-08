from typing import Generic, Type, TypeVar, List, Optional, Dict, Any, Union
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from pydantic import BaseModel

# Define a TypeVar for models
T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        search_terms: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[T]:
        """Fetch all records."""
        query = self.db.query(self.model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)

        if search_terms:
            search_filters = []
            for key, value in search_terms.items():
                pattern = "%{}%".format(value)
                search_filters.append(getattr(self.model, key).like(pattern))

            query = query.filter(or_(*search_filters))

        try:
            return query.offset(skip).limit(limit).all()
        except NoResultFound:
            return []

    def get_by_id(
        self,
        record_id: int
    ) -> Optional[T]:
        """Fetch a record by its ID."""
        try:
            return self.db.query(self.model).filter(self.model.id == record_id).one()
        except NoResultFound:
            return None

    def get_one(
        self,
        filters: Dict[str, Any]
    ) -> Optional[T]:
        """Fetch a record given parameters."""
        query = self.db.query(self.model)

        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)

        try:
            return query.one()
        except NoResultFound:
            return None

    def create(
        self,
        obj_in: Union[BaseModel, Dict]
    ) -> T:
        """Create a new record."""
        if isinstance(obj_in, dict):
            obj = self.model(**obj_in)
        else:
            obj = self.model(**obj_in.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(
        self,
        db_obj: T,
        obj_in: Union[BaseModel, Dict]
    ) -> T:
        """Update an existing record."""
        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(
        self,
        record_id: int
    ) -> Optional[T]:
        """Delete a record by its ID."""
        obj = self.get_by_id(record_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
