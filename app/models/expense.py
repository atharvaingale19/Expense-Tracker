from dataclasses import dataclass


@dataclass
class Expense:
    id: int
    title: str
    amount: float
    category: str

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            amount=data["amount"],
            category=data["category"]
        )