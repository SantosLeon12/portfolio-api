from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.dependencies import get_db


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/database")
def database_health_check(
    db: Session = Depends(get_db),
):
    result = db.execute(
        text(
            """
            SELECT
                current_database() AS database,
                current_user AS user
            """
        )
    ).mappings().one()

    return {
        "status": "ok",
        "database": result["database"],
        "user": result["user"],
    }