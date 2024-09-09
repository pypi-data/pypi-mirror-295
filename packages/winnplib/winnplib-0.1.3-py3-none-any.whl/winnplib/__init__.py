import asyncio
import os
import sys
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.storage.streams import DataReader, Buffer, InputStreamOptions
from io import BytesIO
from PIL import Image

async def get_media_info_async(get_thumbnail=False):
    """
    Gets media data.
    This may hang and not return anything until a media source like Spotify starts playing.

    :param get_thumbnail: Whether to get thumbnail or not.
    :return: a dict with all data about media.
    """
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()

    if current_session:
        if current_session.source_app_user_model_id == current_session.source_app_user_model_id:
            info = await current_session.try_get_media_properties_async()

            info_dict = {song_attr: getattr(info, song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            player = str(current_session.source_app_user_model_id).lower()

            del info_dict['genres']
            del info_dict['subtitle']
            del info_dict['playback_type']

            if not get_thumbnail:
                del info_dict['thumbnail']

            if player.endswith('.exe'):
                player = player[:-4]

            info_dict['player'] = player

            return info_dict

def is_win11():
    """Checks if the system is Windows 11."""
    return sys.getwindowsversion().build >= 22000


def crop_image(image_path):
    """Crops the image if needed (for Windows 10)."""
    img = Image.open(image_path).convert("RGBA")
    left, top, right, bottom = img.size[0], img.size[1], 0, 0
    data = img.getdata()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = data[x + y * img.size[0]]
            if a > 0:
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    if left > right or top > bottom:
        return

    img = img.crop((left + 1, top + 1, right, 233))
    img.save(image_path)

async def get_media_thumbnail_async(filename='./thumb_cache.png'):
    """
    Grabs the currently playing media's cover art.

    :param filename: Optional filename for saving the image.
    :return: Absolute filepath of the saved image.
    """
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()

    if current_session:
        properties = await current_session.try_get_media_properties_async()
        media_info = {song_attr: properties.__getattribute__(song_attr) for song_attr in dir(properties) if
                      song_attr[0] != '_'}

        if media_info.get('thumbnail'):
            thumb_stream_ref = media_info['thumbnail']
            thumb_read_buffer = Buffer(5000000)

            readable_stream = await thumb_stream_ref.open_read_async()
            await readable_stream.read_async(thumb_read_buffer, thumb_read_buffer.capacity,
                                             InputStreamOptions.READ_AHEAD)

            buffer_reader = DataReader.from_buffer(thumb_read_buffer)
            byte_buffer = buffer_reader.read_buffer(thumb_read_buffer.length)

            binary = BytesIO()
            binary.write(bytearray(byte_buffer))
            binary.seek(0)
            print(len(bytearray(byte_buffer)))

            img = Image.open(binary)
            img.save(filename)

    if not is_win11():
        crop_image(filename)

    return os.path.abspath(filename)

def get_media_thumbnail(filename='./thumb_cache.png'):
    return asyncio.run(get_media_thumbnail_async(filename))