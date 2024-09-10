import logging
import os
from typing import Literal

import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI

from .utils import remove_markdown


class GenAudioCard:
    logger = logging.getLogger(__name__)

    def generate_audio_openai(self, api_key: str, text: str, file_path: str, voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "echo", model: str = "tts-1", response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "wav"):
        client = OpenAI(api_key=api_key)
        response = client.audio.speech.create(
          model=model,
          voice=voice,
          input=text,
          response_format=response_format
        )
        response.stream_to_file(file_path)


    def generate_audio_azure(self, text: str, file_path: str, voice: str = "it-IT-GiuseppeMultilingualNeural"):
        speech_key = os.getenv("AZURE_SUBSCRIPTION_KEY", "0833ffefa2fe47948d5cd01c93b0b20a")
        service_region = "westeurope"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = voice
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_path)

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        text = remove_markdown(text)

        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            self.logger.debug("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            self.logger.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.logger.error("Error details: {}".format(cancellation_details.error_details))
