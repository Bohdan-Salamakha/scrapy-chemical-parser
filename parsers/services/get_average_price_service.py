from django.db import connection

from parsers.models import ChemicalProduct


class GetAveragePriceService:
    def __init__(self, instance: ChemicalProduct):
        self.instance = instance

    def get_average(self) -> float:
        numcas = self.instance.numcas
        with connection.cursor() as cursor:
            cursor.execute(
                """
                WITH unnested AS (
                  SELECT
                    unnest(qt_list) AS quantity,
                    unnest(unit_list) AS unit,
                    unnest(price_pack_list) AS price_pack
                  FROM 
                    parsers_chemicalproduct
                  WHERE
                    numcas = %s
                )
                SELECT 
                  AVG(
                    CASE 
                      WHEN unit = 'mg' THEN price_pack::float / (quantity::float / 1000)
                      WHEN unit = 'g' THEN price_pack::float / quantity::float
                      WHEN unit = 'kg' THEN price_pack::float / (quantity::float * 1000)
                      ELSE NULL
                    END
                  ) AS avg_price_per_g,
                  AVG(
                    CASE 
                      WHEN unit = 'ml' THEN price_pack::float / quantity::float
                      WHEN unit = 'l' THEN price_pack::float / (quantity::float * 1000)
                      ELSE NULL
                    END
                  ) AS avg_price_per_ml
                FROM 
                  unnested
            """,
                [numcas],
            )
            result = cursor.fetchone()
        return (round(result[0], 2) if result[0] is not None else None) or (
            round(result[1], 2) if result[1] is not None else None
        )
