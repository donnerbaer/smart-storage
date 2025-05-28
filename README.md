# smart-storage
A website for storing and managing household items


## Setup

1. Open a command line/terminal.
2. Navigate to the project folder.

3. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:

    - **Windows:**

      ```sh
      venv\Scripts\activate
      ```

    - **Mac/Linux:**

      ```sh
      source venv/bin/activate
      ```

5. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

6. Create a `.env` file:
    1. Add the following content:
        ```sh
        DATABASE_URL=sqlite:///database.db
        SECRET_KEY=mysecretkey
        ```
    2. Provide your secret key.
    3. Set your database path.



# Start the application

1. Start the webserver:
    - Navigate to the `/` folder and run `main.py`:
    
    ```sh
    py main.py
    ```
