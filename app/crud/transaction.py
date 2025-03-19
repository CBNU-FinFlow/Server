# app/crud/transaction.py

from sqlalchemy.orm import Session
from app.models.transaction import TransactionHistory
from app.schemas.transaction import TransactionCreate

def get_transactions(db: Session, portfolio_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(TransactionHistory)
        #포트폴리오id로 필터링
        .filter(TransactionHistory.portfolio_id == portfolio_id)
        .order_by(TransactionHistory.transaction_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_transaction_count(db: Session):
    return db.query(TransactionHistory).count()

def delete_transaction(db: Session, transaction_id: int):
    transaction = (
        db.query(TransactionHistory)
        .filter(TransactionHistory.transaction_id == transaction_id)
        .first()
    )
    if not transaction:
        return False
    db.delete(transaction)
    db.commit()
    return True

def create_transaction(db: Session, transaction: TransactionCreate):
    new_transaction = TransactionHistory(**transaction.dict(exclude_unset=True))
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
