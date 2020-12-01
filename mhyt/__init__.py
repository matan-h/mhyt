from __future__ import unicode_literals

__all__ = "yt_download"

import os


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def yt_download(url, filename=None, ismusic=False, video_format=None, hooks=None, logger=None, overwrite=True,codec = None,
                **ydl_opts):
    if hooks is None:
        hooks = [my_hook]

    import youtube_dl
    import os
    if video_format is None:
        video_format = os.path.splitext(filename)[1][1:]
    if not ismusic:
        ydl_opts["format"] = video_format
    if ismusic:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': codec if codec else video_format ,
                'preferredquality': '192'
            }],
        })
    if logger:
        ydl_opts["logger"] = logger
    if hooks:
        ydl_opts["progress_hooks"] = hooks
    if filename is not None:
        ydl_opts["outtmpl"] = filename
    if overwrite:
        if os.path.exists(filename):
            print(f"overwrite file {filename}")
            os.remove(filename)
        ##########################
    print(f"download {url} in format {video_format} to file {filename}")
    ########
    print(ydl_opts)
    #############################################
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def _get_ffmpeg_path():
    err = os.system("ffmpeg -version")
    if err == 0:  # ffmpeg in path
        ffmpeg = "ffmpeg"
    else:  # not in Path
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    ffmpeg = '\"' + ffmpeg + '\"'
    return ffmpeg
