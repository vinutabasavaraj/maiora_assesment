# Project Title

Task Management System with Real-time Chat

## Overview

This project is a simple yet powerful web application for task management. It provides a RESTful API for CRUD operations on tasks and a real-time chatroom feature for communication between team members.

## Features

- Create, Read, Update, and Delete tasks through RESTful API.
- Each task can have details such as due date, priority level, and assigned team members.
- Real-time chatroom for communication between team members.
- Information is stored in a relational database for maintaining task relationships.

## Tech Stack

- FastAPI: A modern, fast, web framework for building APIs with Python 3.7+.
- WebSocket: For real-time communication in the chatroom.
- SQLAlchemy: For working with relational databases.
- Jinja2: Template engine for rendering HTML templates.

## Getting Started

1. Clone the repository:
   git clone https://github.com/vinutabasavaraj/maiora_assesment.git

2. Install dependencies:
    pip install -r requirements.txt

3. Run the FastAPI application:
    uvicorn app.main:app --host 0.0.0.0 --port 8000(port number)

4. Access the API documentation:
    Swagger UI: http://localhost:8000/docs

5. Access the Chatroom:
    http://localhost:8000/chatroom/{task_id}

    




