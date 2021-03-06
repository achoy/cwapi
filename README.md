# cwapi
Common Web API infrastructure

## What is cwapi?

cwapi is an infrastructure that provides some simple tools to build a web api and front-end.

## Plan

Backend development:
- Python Flask (CURRENT)
  Using Flask 0.12 (flask.pocoo.org/docs/0.12)
- Java: use simple and restlet framework. Use ant to build. (FUTURE)
- Kotlin: rewrite Java framework in Kotlin (learning tool) (FUTURE)

Frontend development:
- Elm: simple frontend without using Javascript (CURRENT)

Components:
- Store metadata in SQLite

Future Components:
- Routing engine
- Common DB access with two planned 'adaptors': Mongo and Postgres (via jdbc)
- Common Data/Image access with two planned data stores: Google Drive and S3
- A flexible 'credential' store will be needed that keeps the credentials OUT of git.

## API Routes

To demonstrate a working API set, a representative working project is created.
Pictures API will provide a CRUD and query interface to manage images (jpg, png, gif, bmp)
and external metadata with it.  Two planned storage engines for metadata will be supported
(Mongo and PostgreSQL). Images themselves will be either stored in S3 or via Google Drive
so some access will be needed to manage S3 or Google Drive credentials.

### CURRENT IMPLEMENTATION

Using python flask for a server backend.

ENDPOINT: http://tardis.choycreative.com/photos

### `/list.json`

Return list of photos (metadata)

### `/thumb/<filename>`

Return thumbnail for filename

### `/full/<filename>`

Return full image for filename

### `/meta/<filename>`

Return metadata for one filename

### FUTURE PLAN

ENDPOINT: http://site:8888/v1/api/

All queries must be accompanied by appropriate request key.

### `/api/pictures/meta`

Return all metadata for /pictures API. JSON doc.

### `/api/pictures/list`

Return all user folders from this data source.

### `/api/pictures/list/{folder}`

Return all image metadata for a specific user folder.

### `/api/pictures/load/{filename}?loc={folder}`

Return picture data from that folder.

### `/api/pictures/save/{filename}?loc={folder}`

Write picture data into the given folder.
