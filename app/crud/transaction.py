from sqlalchemy.orm import Session
from app.models.transaction import TransactionHistory


def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TransactionHistory)\
             .order_by(TransactionHistory.transaction_id.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

def get_transaction_count(db: Session):
    return db.query(TransactionHistory).count()

def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(TransactionHistory)\
                    .filter(TransactionHistory.transaction_id == transaction_id)\
                    .first()
    if not transaction:
        return False
    db.delete(transaction)
    db.commit()
    return True
