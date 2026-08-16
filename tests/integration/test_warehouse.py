from src.database.database import SessionLocal
from src.database.models import (
    Article,
    DimDate,
    DimSource,
    FactArticle,
)
from src.framework.warehouse.warehouse_backfill import (
    WarehouseBackfill,
)


def test_warehouse_backfill():

    backfill = WarehouseBackfill()

    inserted = backfill.run()

    assert inserted == 0

    db = SessionLocal()

    try:

        source_count = (
            db.query(DimSource).count()
        )

        date_count = (
            db.query(DimDate).count()
        )

        fact_count = (
            db.query(FactArticle).count()
        )

        article_count = (
            db.query(Article).count()
        )

        assert source_count > 0
        assert date_count > 0
        assert fact_count == article_count

    finally:

        db.close()