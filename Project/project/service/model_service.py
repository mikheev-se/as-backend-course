import pickle
from io import StringIO
from typing import BinaryIO
from fastapi import Depends, HTTPException, status
from project.entities.dto.logs_dto import AddLogDto
from project.service.logs_service import LogsService
import pandas as pd


class ModelService:
    def __init__(self, logs_service: LogsService = Depends()) -> None:
        self.logs_service = logs_service
        self.to_drop = ['CITY', 'COUNTY', 'COUNTY_FIPS', 'FACILITY_ID',
                        'FINAL_NAICS_CODE', 'MECS_NAICS', 'REPORTING_YEAR',
                        'STATE', 'Temp_Band', 'UNIT_NAME', 'for_EU_sum']
        self.numeric_features = ['Coal', 'Diesel', 'LPG_NGL', 'Natural_gas',
                                 'Other', 'Residual_fuel_oil', 'Temp_degC', 'Total']
        self.target = 'MMTCO2E'
        self.prefixes = ['eu', 'ft', 'ftb', 'fto', 'pb', 'pp', 'ut', 'b']

        self.model_path = '../models/regression/best-regressor.model'
        self.data = pd.read_csv('../data/dataset.csv')
        with open(self.model_path, 'rb') as f:
            self.model = pickle.loads(pickle.load(f))

    def get_file(self, file: BinaryIO, sep: str):
        return pd.read_csv(file, sep=sep)

    def return_file(self, data: pd.DataFrame) -> str:
        # output = StringIO()

        # # writer = DictWriter(output, fieldnames=data.columns)

        # # writer.writerows([dict(data.loc[i]) for i in range(len(data))])
        # # writer.writeheader()
        # data.to_csv(output, sep=';', index=False)

        # # output.seek(0)

        # return iter([output.getvalue()])

        return data.to_csv(sep=';', index=None)

    def prepare(self, requester_id: int) -> str:
        df = self.data.copy()
        df = df.drop(self.to_drop, axis=1)

        categorical_features = list(
            df.columns.drop(self.numeric_features + [self.target]))

        df = pd.get_dummies(
            data=df, columns=categorical_features, prefix=self.prefixes)

        df.to_csv('../data/prepared.csv', sep=';', index=None)
        self.data_prepared = df

        res = self.return_file(df)

        dto = AddLogDto(action='prepare', invoked_by=requester_id)
        self.logs_service.add(dto)

        return res

    def fit(self, requester_id: int):
        try:
            df = self.data_prepared
        except AttributeError:
            self.data_prepared = pd.read_csv('../data/prepared.csv', sep=';')
            df = self.data_prepared
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Данные не подготовлены')

        self.model.fit(
            df.drop([self.target], axis=1).values, df[self.target].values
        )

        with open(self.model_path, 'wb') as f:
            pickle.dump(pickle.dumps(self.model), f)

        dto = AddLogDto(action='fit', invoked_by=requester_id)
        self.logs_service.add(dto)

    def predict(self, data: BinaryIO | None, sep: str, requester_id: int) -> str:
        try:
            df = self.get_file(data, sep) if data else pd.read_csv(
                '../data/prepared.csv', sep=';')
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Данных нет')

        if self.target in df.columns:
            df = df.drop(self.target, axis=1)

        pred = self.model.predict(df.values)
        res = self.return_file(pd.DataFrame(pred, columns=[self.target]))

        dto = AddLogDto(action='predict', invoked_by=requester_id)
        self.logs_service.add(dto)

        return res

    def download(self, requester_id: int) -> str:
        res = self.return_file(self.data)

        dto = AddLogDto(action='download', invoked_by=requester_id)
        self.logs_service.add(dto)

        return res
