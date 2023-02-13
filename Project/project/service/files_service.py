import csv
from io import StringIO
from project.models.base import Base


class FilesService:
    @staticmethod
    def row2dict(r):
        return {
            c.name: str(getattr(r, c.name)) for c in r.__table__.columns
        }

    @staticmethod
    def download(values: list[Base]) -> StringIO:
        if not values:
            return
        res = StringIO()
        print(list(values[0].__table__.columns))
        writer = csv.DictWriter(
            res, fieldnames=list(c.name for c in values[0].__table__.columns))
        writer.writeheader()
        for item in values:
            row = FilesService.row2dict(item)
            print(row)
            writer.writerow(row)
        res.seek(0)
        return res
