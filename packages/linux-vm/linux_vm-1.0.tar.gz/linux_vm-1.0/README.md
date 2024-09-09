# Linux_VM

The My Package provides utilities to manage a Docker-based Linux VM and start a basic HTTP server.

## Installation

Install the package using pip:

```sh
pip install -e .
```

## Usage

1. **Create the Linux VM:**

    ```sh
    create-linux-vm
    ```

2. **Start the Linux VM:**

    ```sh
    start-linux-vm
    ```

3. **Stop the Linux VM:**

    ```sh
    stop-linux-vm
    ```

4. **Start the Web Server:**

    ```sh
    start-webserver
    ```

5. Open a web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Notes

- Ensure Docker is installed and running on your system.
- Adjust Docker and server settings as needed for your environment.

## License

This project is licensed under the MIT License.