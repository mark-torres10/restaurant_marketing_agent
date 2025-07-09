# Deployment Guide for Restaurant Marketing Agent API

This guide provides instructions on how to deploy the FastAPI application (`api.py`) that generates marketing posts, along with considerations for securely handling your OpenAI API key.

## 1. Running the API Locally

To run the API locally, ensure you have `uvicorn` installed (`uv pip install uvicorn`). Then, execute the following command in your terminal from the project root directory:

```bash
uvicorn api:app --reload
```

This will start the API server, typically accessible at `http://127.0.0.1:8000`.

## 2. Invoking the API with cURL

You can test the API using `curl`. Replace `YOUR_TOPIC` with the desired restaurant cuisine (e.g., `Greek`, `Filipino`, `Mediterranean`).

```bash
curl "http://127.0.0.1:8000/generate_posts?topic=YOUR_TOPIC"
```

**Example for a Greek restaurant:**

```bash
curl "http://127.0.0.1:8000/generate_posts?topic=Greek"
```

## 3. Deployment Options

When deploying your FastAPI application, it's crucial to securely manage your `OPENAI_API_KEY`. Most modern deployment platforms offer mechanisms for handling environment variables securely.

### A. Replit (Recommended for ease of use)

Replit is an excellent choice for quick and easy deployment, especially for small to medium-sized applications. It provides built-in support for environment variables, making secret management straightforward.

**Steps for Replit Deployment:**

1.  **Create a new Repl:** Go to [Replit](https://replit.com/) and create a new Repl. Choose Python as the language.
2.  **Upload your files:** Upload `api.py`, `write_post.py`, and `requirements.txt` to your Repl.
3.  **Set Environment Variables:** In Replit, navigate to the "Secrets" tab (usually a lock icon in the sidebar). Add a new secret with the key `OPENAI_API_KEY` and your actual OpenAI API key as the value. Replit will automatically inject this into your application's environment.
4.  **Configure `pyproject.toml` (or `replit.nix`):** Replit often auto-detects the run command. If not, you might need to configure `pyproject.toml` or `replit.nix` to run your FastAPI application. A common entry for `pyproject.toml` would be:
    ```toml
    [tool.poetry.scripts]
    start = "uvicorn api:app --host 0.0.0.0 --port 8000"
    ```
    Or, for `replit.nix`:
    ```nix
    { pkgs }:

    { deps = [ pkgs.python39Packages.uvicorn ];
      enterShell = ''
        uvicorn api:app --host 0.0.0.0 --port 8000
      '';
    }
    ```
    Ensure `uvicorn` is installed via `uv pip install uvicorn` in your Repl's shell.
5.  **Run the Repl:** Click the "Run" button. Replit will install dependencies from `requirements.txt` and start your FastAPI application. It will provide a public URL for your deployed API.

### B. Modal

Modal is a cloud platform that allows you to run Python code in the cloud, including web services. It's designed for scalable, serverless deployments and handles environment variables securely.

**Key Features for Deployment:**

*   **Serverless:** You define your application, and Modal handles the infrastructure.
*   **Environment Variables:** Securely manage secrets and environment variables.
*   **Scalability:** Automatically scales your application based on demand.

**General Steps (refer to Modal documentation for specifics):**

1.  **Install Modal client:** `pip install modal-client`
2.  **Define your app:** Create a Modal app file (e.g., `modal_app.py`) that defines your FastAPI application as a Modal function.
3.  **Deploy:** Use the Modal CLI to deploy your application.

### C. Render

Render is a unified cloud platform for building and running all your apps and websites. It supports various types of services, including web services, and offers secure environment variable management.

**Key Features for Deployment:**

*   **Easy Setup:** Connects directly to your Git repository.
*   **Environment Variables:** Securely store and inject environment variables.
*   **Automatic Deployments:** Deploys automatically on Git pushes.

**General Steps (refer to Render documentation for specifics):**

1.  **Connect to Git:** Connect your GitHub/GitLab repository to Render.
2.  **Create a Web Service:** Choose "Web Service" and configure it for Python/FastAPI.
3.  **Set Build and Start Commands:**
    *   Build Command: `uv pip install -r requirements.txt`
    *   Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT` (Render provides the `$PORT` environment variable).
4.  **Add Environment Variables:** In Render's dashboard, add `OPENAI_API_KEY` as an environment variable.

### D. Heroku

Heroku is a platform as a service (PaaS) that allows developers to build, run, and operate applications entirely in the cloud. It's a good option for small to medium-sized applications and has robust support for environment variables.

**Key Features for Deployment:**

*   **Git Integration:** Deploy directly from your Git repository.
*   **Config Vars:** Securely manage environment variables (Config Vars).

**General Steps (refer to Heroku documentation for specifics):**

1.  **Install Heroku CLI:** Follow Heroku's instructions to install their CLI.
2.  **Login:** `heroku login`
3.  **Create a Heroku app:** `heroku create your-app-name`
4.  **Set Buildpack:** `heroku buildpacks:set heroku/python`
5.  **Set Config Var:** `heroku config:set OPENAI_API_KEY=your_api_key_here`
6.  **Create a `Procfile`:** In your project root, create a file named `Procfile` (no extension) with the following content:
    ```
    web: uvicorn api:app --host 0.0.0.0 --port $PORT
    ```
7.  **Deploy:** `git push heroku main`

## 4. Secure Handling of Environment Variables

Regardless of the deployment platform, always follow these best practices for handling sensitive information like API keys:

*   **Never hardcode secrets:** Do not embed your API key directly in your code.
*   **Use environment variables:** Store secrets as environment variables.
*   **Utilize platform-specific secret management:** Leverage the secure secret management features provided by your chosen deployment platform (e.g., Replit Secrets, Modal Secrets, Render Environment Variables, Heroku Config Vars).
*   **`.env` for local development only:** The `.env` file should only be used for local development and should *never* be committed to version control (add `.env` to your `.gitignore` file).

By following these guidelines, you can ensure your API is deployed securely and your sensitive information remains protected.
