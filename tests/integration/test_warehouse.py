from src.database.database import SessionLocal
from src.database.models import (
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

        assert source_count == 4
        assert date_count == 6
        assert fact_count == 51

    finally:

        db.close()