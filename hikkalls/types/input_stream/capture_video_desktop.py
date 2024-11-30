from ...ffprobe import FFprobe
from ...media_devices.screen_info import ScreenInfo
from .input_stream import InputStream
from .input_stream import InputVideoStream
from .video_parameters import VideoParameters


class CaptureVideoDesktop(InputStream):
    """Capture video only from Screen

    Attributes:
        ffmpeg_parameters (``str``):
            FFmpeg additional parameters
        stream_audio (:obj:`~hikkalls.types.InputAudioStream()`):
            Input Audio Stream Descriptor
        stream_video (:obj:`~hikkalls.types.InputVideoStream()`):
            Input Video Stream Descriptor
    Parameters:
        screen_info (:obj: `~hikkalls.media_devices.ScreenManager()`):
            The screen video capturing params
        video_parameters (:obj:`~hikkalls.types.VideoParameters()`):
            The video parameters of the stream, can be used also
            :obj:`~hikkalls.types.HighQualityVideo()`,
            :obj:`~hikkalls.types.MediumQualityVideo()` or
            :obj:`~hikkalls.types.LowQualityVideo()`
    """

    def __init__(
        self,
        screen_info: ScreenInfo,
        video_parameters: VideoParameters = VideoParameters(),
    ):
        self._path = screen_info.build_ffmpeg_command(
            video_parameters.frame_rate,
        )
        self.ffmpeg_parameters: str = screen_info.ffmpeg_parameters
        self.raw_headers = None
        super().__init__(
            stream_video=InputVideoStream(
                f'screen://{self._path}',
                video_parameters,
            ),
        )

    @property
    def headers(self):
        return FFprobe.ffmpeg_headers(self.raw_headers)

    async def check_pipe(self):
        pass
