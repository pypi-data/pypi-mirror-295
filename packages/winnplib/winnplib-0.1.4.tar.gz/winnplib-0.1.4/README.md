# Now Playing Api

## NOW USES UP TO DATE LIBRARYS / PYTHON!

### A simple api to get windows media
This includes but not limited to cover art

To get media info you want to await it:
```python
await winnplib.get_media_info_async()
```
or you can use asyncio
```python
asyncio.run(winnplib.get_media_info_async())
```

getting media info returns a dict

to get the thumbnail you can do it async or not async
```python
winnplib.get_media_thumbnail(filepath) # Not async
winnplib.get_media_thumbnail_async(filepath) # Async
```

file path is optional in both of those

~~i hate docs~~