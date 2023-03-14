### How to use a Python env

If you have not the package intalled previuously, start with that in you machine
```python
pip install virtualenv
```

Create your env
```python
python -m venv myenv
```

Activate your env
  - In windows
    ```bash
    myenv/Scripts/activate.bat
    ```

  - In macOS/Linux
    ```bash
    source myenv/bin/activate
    ```

Install the requirements
```bash
pip install -r requirements.txt
```

To leave the env
```bash
deactivate
```