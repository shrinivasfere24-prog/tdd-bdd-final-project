"""Database models for the Product Catalog service."""

from decimal import Decimal
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})


class DataValidationError(Exception):
    """Used for data validation errors."""


class Category(Enum):
    """Valid product categories."""

    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Product database model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(
        db.Enum(Category),
        nullable=False,
        default=Category.UNKNOWN,
    )

    def create(self):
        """Create the product in the database."""
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the product in the database."""
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Delete the product from the database."""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serialize the product into JSON-compatible data."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        """Deserialize JSON data into a Product."""
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = Decimal(str(data["price"]))

            if not isinstance(data["available"], bool):
                raise DataValidationError(
                    "Invalid type for boolean [available]"
                )

            self.available = data["available"]
            self.category = Category[data["category"]]

        except KeyError as error:
            raise DataValidationError(
                f"Invalid product: missing {error.args[0]}"
            ) from error

        except (TypeError, ValueError) as error:
            raise DataValidationError(
                f"Invalid product data: {error}"
            ) from error

        return self

    @classmethod
    def all(cls):
        """Return all products."""
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """Find a product by ID."""
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Find products by name."""
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_category(cls, category=Category.UNKNOWN):
        """Find products by category."""
        return cls.query.filter(cls.category == category).all()

    @classmethod
    def find_by_availability(cls, available=True):
        """Find products by availability."""
        return cls.query.filter(cls.available == available).all()
