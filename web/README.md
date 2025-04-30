# Project Website

This website provides an interface for user entering a questionnaire and receiving a personalized prediction on the risk scores of those 4 chronic diseases.

After the model produces risk scores, a large language model (LLM) module draws on reputable medical guidelines to recommend personalized advice.

## How to Run

To run the website using Docker, follow these steps:

1. Ensure you are in the current directory (`web` folder under project root folder).
2. Execute the following command:
    ```bash
    docker compose up -d
    ```
3. Once the containers are up and running, the website will be accessible on port 80. Open your browser and visit: http://localhost/
* Note: It may take a few minutes for the ollama to download and start the language model. (It may take around 8-9G vram)

To stop and clean up the containers, execute the following command in the current directory:
```bash
docker compose down
```

## Technology Stack

The website uses the following technologies:

- **Flask** (Backend): We chose Flask as the backend framework because it integrates well with our models generating by TensorFlow and scikit-learn.
- **React** (Frontend): The frontend is built with React, providing a dynamic and responsive user interface for interacting with the data.
- **Ollama** (Language Model API): We use the Ollama API with **Gemma3** language model to generate personalized advice.
