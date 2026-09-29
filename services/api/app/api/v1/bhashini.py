from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from app.services.bhashini import BhashiniService

router = APIRouter(prefix="/bhashini", tags=["Bhashini Voice AI"])

class ASRRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio chunk")
    language: str = Field(default="hi", description="Source language code: hi, en, mr, etc.")
    audio_format: str = Field(default="wav", description="Audio format: wav, webm, mp3")

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize into speech")
    language: str = Field(default="hi", description="Language code")
    gender: str = Field(default="female", description="Voice gender: female or male")

@router.post("/asr")
async def transcribe_speech(request: ASRRequest):
    """
    Transcribe spoken voice audio using Bhashini ASR pipeline.
    """
    result = await BhashiniService.transcribe_audio(
        audio_base64=request.audio_base64,
        source_language=request.language,
        audio_format=request.audio_format
    )
    return result

@router.post("/tts")
async def synthesize_speech(request: TTSRequest):
    """
    Synthesize text into Indic voice audio using Bhashini TTS pipeline.
    """
    result = await BhashiniService.synthesize_speech(
        text=request.text,
        target_language=request.language,
        gender=request.gender
    )
    return result
