# starchat

**starchat** is a test task for a Python Developer position at StarNavi. It is a Django-based chat API with various features, including user management, post and comment handling, profanity and abuse detection, analytics, and automated replies.

## Features

- **User Registration**: Register new users.
- **User Login**: Authenticate users and manage sessions.
- **Post Management API**: Create, read, update, and delete posts.
- **Comment Management API**: Create, read, update, and delete comments.
- **Profanity and Abuse Detection**: Checks posts and comments for profanity and abuse, blocking inappropriate content.
- **Comment Analytics**: Endpoint for comment analytics. Example URL: `/api/comments-daily-breakdown?date_from=2020-02-02&date_to=2022-02-15`. Returns aggregated data by day, including the number of created and blocked comments.
- **Automated Replies**: Automatically replies to comments if enabled by the user for their posts. Replies are delayed based on user settings and are relevant to the post and comment.

## Requirements

- Docker
- Docker Compose

All dependencies are included in `requirements.txt`. The project is based on Django, using Celery and Gunicorn.

## Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd starchat
   ```

2. **Start the Application**

   Run the following command to start the application using Docker Compose:

   ```bash
   docker-compose up
   ```

   This will set up all required services and dependencies.

## Environment Variables

The project requires the following environment variable to be set:


- `OPENAI_API_KEY`: API key for OpenAI services.

```
export OPENAI_API_KEY=<your_key>
```

## Configuration

Configuration can be modified in `docker-compose.yml` as needed. Most settings are configured out of the box.

## Usage

Once the application is running, you can use the following endpoints:

- **User Registration**: `/api/v1/accounts/register/`
- **User Login via JWT**: `/api/v1/token/`, `/api/v1/token/verify/` `/api/v1/refresh/`
- **Post Management API**: `/api/posts/`
- **Comment Management API**: `/api/comments/`
- **Profanity and Abuse Detection**: Integrated into the Post and Comment APIs.
- **Comment Analytics**: `/api/v1/analytics/comments/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
- **Automated Replies**: `/api/v1/auto_response/`

## Testing

To run tests, use:

```bash
python3 manage.py test
```

