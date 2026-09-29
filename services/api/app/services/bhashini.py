import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class BhashiniService:
    @classmethod
    async def transcribe_audio(
        cls,
        audio_base64: str,
        source_language: str = "hi",
        audio_format: str = "wav",
        sampling_rate: int = 16000
    ) -> Dict[str, Any]:
        """
        Transcribes speech audio into text using Bhashini Dhruva ASR Pipeline.
        """
        headers = {
            "Authorization": settings.BHASHINI_INFERENCE_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": source_language
                        },
                        "serviceId": "ai4bharat/conformer-hi-gpu--gpu" if source_language == "hi" else "ai4bharat/whisper-medium-en--gpu",
                        "audioFormat": audio_format,
                        "samplingRate": sampling_rate
                    }
                }
            ],
            "inputData": {
                "audio": [
                    {
                        "audioContent": audio_base64
                    }
                ]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(settings.BHASHINI_INFERENCE_URL, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    pipeline_res = data.get("pipelineResponse", [])
                    if pipeline_res and len(pipeline_res) > 0:
                        output = pipeline_res[0].get("output", [])
                        if output and len(output) > 0:
                            transcript = output[0].get("source", "")
                            return {
                                "success": True,
                                "transcript": transcript,
                                "language": source_language,
                                "provider": "bhashini_dhruva"
                            }
                logger.warning(f"Bhashini ASR response: {res.status_code} - {res.text}")
        except Exception as e:
            logger.warning(f"Bhashini ASR call notice ({e}).")

        # Fallback response
        return {
            "success": False,
            "transcript": "",
            "language": source_language,
            "fallback_used": True,
            "provider": "web_speech_fallback"
        }

    @classmethod
    async def synthesize_speech(
        cls,
        text: str,
        target_language: str = "hi",
        gender: str = "female"
    ) -> Dict[str, Any]:
        """
        Synthesizes text into high-fidelity Indic voice using Bhashini Dhruva TTS Pipeline.
        """
        headers = {
            "Authorization": settings.BHASHINI_INFERENCE_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": target_language
                        },
                        "serviceId": "ai4bharat/indic-tts-coqui-indo_aryan-gpu--gpu" if target_language == "hi" else "ai4bharat/indic-tts-coqui-misc-gpu--gpu",
                        "gender": gender
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(settings.BHASHINI_INFERENCE_URL, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    pipeline_res = data.get("pipelineResponse", [])
                    if pipeline_res and len(pipeline_res) > 0:
                        audio = pipeline_res[0].get("audio", [])
                        if audio and len(audio) > 0:
                            audio_content = audio[0].get("audioContent", "")
                            return {
                                "success": True,
                                "audio_base64": audio_content,
                                "format": "wav",
                                "provider": "bhashini_dhruva"
                            }
                logger.warning(f"Bhashini TTS response: {res.status_code} - {res.text}")
        except Exception as e:
            logger.warning(f"Bhashini TTS call notice ({e}).")

        return {
            "success": False,
            "audio_base64": None,
            "fallback_used": True,
            "provider": "browser_speech_synthesis"
        }
