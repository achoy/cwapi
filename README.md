# cwapi
Common Web API infrastructure

## What is cwapi?

cwapi is an infrastructure that provides some simple tools to build a web api and front-end.

## Plan

Backend development:
- Java: use simple and restlet framework. Use ant to build.
- Kotlin: rewrite Java framework in Kotlin (learning tool)

Frontend development:
- Elm: simple frontend without using Javascript

Components:
- Routing engine
- Common DB access with two planned 'adaptors': Mongo and Postgres (via jdbc)

## API Routes

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
