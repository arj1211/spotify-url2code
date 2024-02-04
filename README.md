# Project Title

This project contains Python scripts for interacting with the Spotify API and generating Spotify codes for given tracks.

## Prerequisites

- Python 3
- Spotify Developer account

## Setting Up a Python Environment with venv

1. Open your terminal/command prompt.

2. Navigate to your project directory:

    ```
    cd /path/to/your/project
    ```

3. Create a new virtual environment inside your project directory:

    ```
    python -m venv env
    ```

4. Activate the virtual environment. On Windows, use:

    ```
    env\Scripts\activate
    ```

    On Unix or MacOS, use:

    ```
    source env/bin/activate
    ```

You should see `(env)` at the beginning of your command prompt, indicating that the virtual environment is activated.

## Installing Required Libraries

Install the required libraries using pip, Python's package installer. Make sure your virtual environment is activated, then run:

```
pip install -r requirements.txt
```


## Getting Spotify Client ID and Client Secret

1. Log in to the Spotify Developer Dashboard.

2. Click on `Create an App`.

3. Fill in the necessary information and click `Create`.

4. You will be redirected to your new app's page. Here, you can find your Client ID and Client Secret.

**Please note that you need to have a valid Spotify Developer account to use the Spotify API.**

## Configuring the Application

Before running the scripts, set your Spotify Client ID and Client Secret in the `secrets.env` file:

```
SPOTIFY_CLIENT_ID=<your Spotify Client ID> SPOTIFY_CLIENT_SECRET=<your Spotify Client Secret>
```


## Running the Scripts

You can run the scripts using Python. For example:

```
python track_info.py
```