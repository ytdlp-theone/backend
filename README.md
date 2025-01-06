# YouTube Downloader Backend

This is a Flask-based backend for downloading YouTube videos and audio files in user-selected formats. It supports resolution and format selection.

## Features

- List all available formats (resolution, size, and extension).
- Download a specific format chosen by the user.

## API Endpoints

### 1. Retrieve Formats

**POST** `/formats`

**Request Body**:

```json
{
  "url": "YouTube video URL"
}
```
