from fastapi.routing import APIRouter
from fastapi import BackgroundTasks, Depends, UploadFile, status
from fastapi.responses import StreamingResponse, PlainTextResponse, FileResponse
from project.service.jwt_service import JwtService

from project.service.model_service import ModelService

model_router = APIRouter(
    prefix='/model',
    tags=['model']
)


@model_router.get('/prepare', status_code=status.HTTP_200_OK, response_class=FileResponse)
def prepare(model_service: ModelService = Depends(),
            requester_id: int = Depends(JwtService.get_current_user_id)):
    res = model_service.prepare(requester_id)
    return csv_response(res, file_name='prepared')


@model_router.post('/fit', status_code=status.HTTP_202_ACCEPTED)
def fit(background_tasks: BackgroundTasks, model_service: ModelService = Depends(),
        requester_id: int = Depends(JwtService.get_current_user_id)):
    background_tasks.add_task(model_service.fit, requester_id)


@model_router.post('/predict', status_code=status.HTTP_200_OK, response_class=FileResponse)
def predict(upload_file: UploadFile = None, sep: str = ';', model_service: ModelService = Depends(),
            requester_id: int = Depends(JwtService.get_current_user_id)):
    res = model_service.predict(
        upload_file.file, sep, requester_id) if upload_file else model_service.predict(None, sep, requester_id)
    return csv_response(res, file_name='predict')


@model_router.get('/download', status_code=status.HTTP_200_OK, response_class=FileResponse)
def download(model_service: ModelService = Depends(),
             requester_id: int = Depends(JwtService.get_current_user_id)):
    res = model_service.download(requester_id)
    return csv_response(res)


def csv_response(string_result: str, file_name: str = 'data'):
    return PlainTextResponse(string_result,
                             media_type='text/csv',
                             headers={'Content-Disposition': f'attachment; filename={file_name}.csv'})
