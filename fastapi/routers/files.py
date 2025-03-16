# fastapi/routers/files.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
import os
import django
from django.conf import settings
from fastapi.responses import JSONResponse

from fastapi.schemas.models import DataFileResponse, DataFileCreate

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/", response_model=DataFileResponse)
async def upload_file(
        file: UploadFile = File(...),
        dataset_id: int = None
):
    try:
        # Save file to temp location
        file_path = os.path.join(settings.MEDIA_ROOT, "temp", file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Use Django ORM to create record
        from apps.core.models import DataFile, Dataset

        # Get dataset or raise exception
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Create DataFile
        file_type = file.filename.split(".")[-1].lower()
        data_file = DataFile.objects.create(
            name=file.filename,
            file_type=file_type,
            status="pending",
            dataset=dataset,
            file_path=file_path
        )

        # Return response
        return DataFileResponse.from_orm(data_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))