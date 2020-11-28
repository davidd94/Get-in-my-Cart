from pydub import AudioSegment
from pydub.playback import play

from utils.email import email
from settings import (
    alert_type,
    email_options,
)

async def execute_alert():
    if alert_type == "sound":
        await play_loud_alert()
    elif alert_type == "email":
        email()
    elif alert_type == "paypal":
        pass


async def play_quiet_alert():
    audio_clip = AudioSegment.from_mp3("audio/short_ringtone_alert.mp3")
    play(audio_clip)

async def play_loud_alert():
    print("Alerting user....")
    audio_clip = AudioSegment.from_mp3("audio/annoying_alarm.mp3")
    play(audio_clip)
