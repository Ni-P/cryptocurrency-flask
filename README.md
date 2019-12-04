**Activate the virtual environment**

```bash
source venve/bin/activate
```

**Install all packages**

```bash
pip3 install -r requirements.txt
```

**Run the  tests**

With the venv active:

```bash
python -m pytest backend.tests
```

**Run the App and API**

```bash
python3 -m backend.app
```

**Run a peer instance**

```bash
export PEER=True && python3 -m backend.app
```

