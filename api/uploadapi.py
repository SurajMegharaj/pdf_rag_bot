from fastapi import APIRouter , UploadFile ,Form
from services.MiniUploader import MinioUploader
from services.mongo_upload import MongoUploader
from services.rag import rag

router = APIRouter()

mino_uploader = MinioUploader()
mongo_uploader = MongoUploader()
vectorizer = rag()

@router.post('/upload')
async def upload_pdf(username : str = Form(...), file: UploadFile = Form(...)):
    file_path = mino_uploader.upload_file(file.file , file.filename)
    mongo_uploader.upload_metadata(username=username ,path = file_path)
    vectorizer.vectorize(file.file)
    return {'message': 'File uploaded and vectorized successfully','path':file_path}

