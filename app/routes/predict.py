import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from service.species import predict
from typing import Annotated
from pydantic import Field
from deps import TMP_DIR, limiter
from auth import verify_bearer_token
from service.types import PredictionsResponse

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post(
    "/file",
    summary="Upload an image an receive one detection per species (highest confidence)",
    response_model=PredictionsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_bearer_token)],
    responses={
        200: {"description": "List of detections"},
        400: {"description": "Invalid Request"},
        500: {"description": "Internal Server Error"},
    },
)
@limiter.limit("10/minute")
async def predict_from_file(
        request: Request,
        file: UploadFile= File(
            ...,
            description=(
            "The image to be analyzed."
            ),
        ),
        lat: Annotated[
        float,
        Field(
            ...,
            ge=-90.0,
            le=90.0,
            description="Latitude of recording (between –90.0 and +90.0).",
        ),
    ] = Form(...),
    lon: Annotated[
        float,
        Field(
            ...,
            ge=-180.0,
            le=180.0,
            description="Longitude of recording (between –180.0 and +180.0).",
        ),
    ] = Form(...),
) :
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    tmp_path = os.path.join(TMP_DIR, unique_name)

    try:
        with open(tmp_path, "wb") as out_f:
            shutil.copyfileobj(file.file, out_f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {e}")

    try:
        rec = predict(tmp_path,(lat,lon))

    except Exception as e:
        os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=f"SpeciesNET analysis failed: {e}")

    os.remove(tmp_path)

    return rec
