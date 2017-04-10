# Simplified cwapi

## Current development tasks

- Create a simple ENDPOINT using python Flask infrastructure (py-server)
- Create a front-end using Elm
- Host frontend and backend at http://tardis.choycreative.com/photobook/PhotoGroove.html

## To dos


## API Routes

ENDPOINT: http://tardis.choycreative.com:5000/photos

### `/list.json`

Return metadata for pictures here. JSON doc.

`[{ 'uri': 'filename', 'size': kbsize, 'title': 'short_description' }, ...]`

### `/thumb/filename`

Return thumbnail or small image

### `/photo/filename`

Return actual image
