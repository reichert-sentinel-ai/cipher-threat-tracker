# Sprint C2: IOC Search - Server Startup Guide

## Issue
The server fails to start when run from `src/api` directory due to relative import errors.

## Solution: Run from Project Root

From the `project/repo-cipher` directory, run:

```powershell
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Or create a startup script in `project/repo-cipher`:

```python
# run_server.py
import uvicorn
from src.api.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

Then run:
```powershell
python run_server.py
```

## Alternative: Fix Import Paths

If you want to run from `src/api`, change the imports in `main.py` from:
```python
from .routers import ...
```

To:
```python
from routers import ...
```

But this would require changing all router files too, so the first solution is better.

## Testing

Once server is running, test endpoints:
- Feed Status: http://localhost:8000/api/ioc/feeds
- Search: http://localhost:8000/api/ioc/search?query=185.220.101.45
- Enrichment: http://localhost:8000/api/ioc/enrich/185.220.101.45
- API Docs: http://localhost:8000/docs

