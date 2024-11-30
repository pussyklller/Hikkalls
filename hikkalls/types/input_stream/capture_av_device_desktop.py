from ...ffprobe import FFprobe
from ...media_devices.device_info import DeviceInfo
from ...media_devices.screen_info import ScreenInfo
from .audio_parameters import AudioParameters
from .input_stream import InputAudioStream
from .input_stream import InputStream
from .input_stream import InputVideoStream
from .video_parameters import VideoParameters


class CaptureAVDeviceDesktop(InputStream):
    """Capture video from Screen and Audio from device

    Attributes:
        stream_audio (:obj:`~hikkalls.types.InputAudioStream()`):
            Input Audio Stream Descriptor
        stream_video (:obj:`~hikkalls.types.InputVideoStream()`):
            Input Video Stream Descriptor
    Parameters:
        audio_info (:obj: `~hikkalls.media_devices.DeviceInfo()`):
            The audio device capturing params
        screen_info (:obj: `~hikkalls.media_devices.ScreenManager()`):
            The screen video capturing params
        audio_parameters (:obj:`~hikkalls.types.AudioParameters()`):
            The audio parameters of the stream, can be used also
            :obj:`~hikkalls.types.HighQualityAudio()`,
            :obj:`~hikkalls.types.MediumQualityAudio()` or
            :obj:`~hikkalls.types.LowQualityAudio()`
        video_parameters (:obj:`~hikkalls.types.VideoParameters()`):
            The video parameters of the stream, can be used also
            :obj:`~hikkalls.types.HighQualityVideo()`,
            :obj:`~hikkalls.types.MediumQualityVideo()` or
            :obj:`~hikkalls.types.LowQualityVideo()`
    """

    def __init__(
        self,
        audio_info: DeviceInfo,
        screen_info: ScreenInfo,
        audio_parameters: AudioParameters = AudioParameters(),
        video_parameters: VideoParameters = VideoParameters(),
    ):
        self._audio_path = audio_info.build_ffmpeg_command()
        self.audio_ffmpeg: str = audio_info.ffmpeg_parameters
        self._video_path = screen_info.build_ffmpeg_command(
            video_parameters.frame_rate,
        )
        self.video_ffmpeg: str = screen_info.ffmpeg_parameters
        self.raw_headers = None
        super().__init__(
            InputAudioStream(
                f'device://{self._audio_path}',
                audio_parameters,
            ),
            InputVideoStream(
                f'screen://{self._video_path}',
                video_parameters,
            ),
        )

    @property
    def headers(self):
        return FFprobe.ffmpeg_headers(self.raw_headers)

    async def check_pipe(self):
        pass
