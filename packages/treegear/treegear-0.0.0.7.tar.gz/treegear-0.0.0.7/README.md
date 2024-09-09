# **Now this is just for tests to upload and pull the package.**

Version: 0.0.0.7

**Usage:**  
1\. Add a python file (e.g. app.py) with text inside:

```python
from treegear import TreeGear

trgr = TreeGear()

if __name__ == '__main__':
    quit(0)
```

2\. Run this code with command: "python -m uvicorn app:trgr"

**Usage (just for test it also works fine):** "python -m uvicorn treegear:TreeGear"

---

Then go in browser to http://127.0.0.1:8000

For any path it returns "OK and hello from TreeGear!"

You can make it return your own message  
if prior set environment variable "$TRGR\_MESSAGE" with your desired text