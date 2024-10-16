# Grant Engine Document Verification App

This project is a document verification application for Grant Engine. It consists of a frontend built with Next.js and a backend powered by FastAPI.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Grant Engine Document Verification App is designed to streamline the process of verifying documents for grant applications. It provides a user-friendly interface for applicants and administrators to upload, review, and verify documents.

## Features

- User authentication and authorization
- Document upload and management
- Real-time document verification status
- Admin dashboard for managing applications

## Technologies

### Frontend

- Next.js
- React
- Tailwind CSS
- ShadcnUI

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy

## Installation

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL

### Clone the repository:
- git clone https://github.com/techverx-org/grant-engine.git

### Frontend Setup

1. Change dir:
    ```bash
    cd frontend
    ```

2. Create a `.env.local` file by copying the example environment file:
  `cp env.example.txt .env.local`

3. Add the required environment variables to the `.env.local` file.

4. Install dependencies:
    ```bash
    npm install
    ```

5. Start the development server:
    ```bash
    npm run dev
    ```

### Backend Setup

1. Change dir:
    ```bash
    cd backend
    ```

2. Create a `.env` file by copying the example environment file:
  `cp .env.example .env`

3. Add the required environment variables to the `.env` file.

4. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Run the FastAPI server:
    ```bash
    fastapi dev app/main.py
    ```

## Usage

1. Open your browser and navigate to `http://localhost:3000` for the frontend.
2. The backend API will be available at `http://localhost:5000`.

