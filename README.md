# GovTech LAUNCHPAD Intern Assessment

## Description
This project is an intelligent backend system designed to facilitate seamless interactions with OpenAI's GPT-3.5 Turbo language model. Key features include:

1. Comprehensive conversation management with full CRUD operations
2. Efficient prompt handling and response generation
3. Context-aware prompting using conversation history
4. Secure data handling with anonymization and auditing capabilities

The system provides a robust foundation for building sophisticated AI-powered applications while ensuring data privacy and traceability.

## Deployment
The application is currently hosted on AWS EC2 and can be accessed at:

http://3.138.112.200/docs

This link will take you to the Swagger UI documentation of the API, where you can explore and test the available endpoints.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation
To install and run the project:

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Obtain the `.env` file from me and place it in the project `./app` directory.
5. Run the following command:

   ```
   docker-compose up --build
   ```

This command will build the Docker images and start the containers for the application.

## Usage
Once the application is running, you can interact with it through its API endpoints. To explore and test the API:

1. Open your web browser and navigate to `http://0.0.0.0:80/docs`
2. This will open the Swagger UI, which provides an interactive documentation of the API
3. You can view all available endpoints, their descriptions, and required parameters
4. To test an endpoint:
   - Click on the endpoint you want to try
   - Click the "Try it out" button
   - Fill in any required parameters
   - Click "Execute" to send the request
   - View the response below

This interface allows you to easily test and understand the functionality of the API without needing additional tools.

## Features
1. **FastAPI Web Framework**: Utilizes FastAPI for building high-performance, easy-to-use REST APIs with automatic interactive documentation.

2. **Pydantic Data Validation**: Implements Pydantic for data validation, serialization, and settings management using Python type annotations.

3. **Data Storage with MongoDB and Beanie ODM**: Uses MongoDB for scalable and flexible data storage, managed through the Beanie ODM for seamless integration and efficient data operations.

4. **Token Management with Tiktoken**: Employs Tiktoken for accurate token counting, crucial for managing API requests to OpenAI's models.

5. **OpenAI API Integration**: Seamlessly integrates with OpenAI's GPT-3.5 Turbo model for advanced natural language processing capabilities.

6. **AWS Comprehend for Anonymization**: Leverages AWS Comprehend for robust text analysis and entity recognition, enabling effective data anonymization.

7. **Test-Driven Development with Pytest**: Implements comprehensive unit testing using pytest, including async test support and mocking. This ensures code reliability, maintainability, and facilitates a test-driven development approach.

8. **CRUD Operations for Conversations**: Provides full Create, Read, Update, and Delete functionality for managing conversation data.

9. **Context-Aware Prompting**: Utilizes conversation history to generate more relevant and coherent responses.

10. **Secure Data Handling**: Implements data anonymization and auditing features to ensure privacy and traceability.

11. **Interactive API Documentation**: Offers Swagger UI for easy API exploration and testing directly through the browser.

These features combine to create a powerful, secure, and user-friendly backend system for AI-driven applications.
