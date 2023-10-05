# LSService

The LSService uses Starlette framework and requires Uvicorn server. Trickiest part was the graceful shutdown.
Only this particular combination worked properly, I tried many different combinations and there was this issue
that if a request is still in progress (sleeping) during shutdown, further request would queue and you can keep
the server alive until the timeout.

## Dependencies
For the service:
```
pip install starlette
```
```
pip install uvicorn
```
For unit tests:
```
pip install httpx
```

## Project
1) LSService: This contains the rest endpoint to provide the list of directory contents.
2) UnitTests: This contains the unit tests for the endpoint.


To run the server use command:
```
uvicorn LSService:app --host 0.0.0.0 --port 8000 --workers 4
```

To send request use command:
```
curl -X POST -H "Content-Type: application/json" -d '{"path": "/Users/admin/", "response_delay": 5}' http://127.0.0.1:8000/dir/list
```

I get response like:
```
["Applications","Desktop","Documents","Downloads","IdeaProjects","JDev","Library","Movies","Music","Pictures","Postman","Postman Agent","Public"]
```


Request body:
Request body has two parameters, path: It is required for the service to work. response_delay: Number of seconds before
the service should provide response. It is optional and if left out behaves as if response_delay is 0 seconds.
```json
{
    "path": "/Users/admin/",
    "response_delay": 5
}
```
Finally to stop the serer:
Press CTRL+C to send a stop signal. The server will close all worker threads except for the ones which are currently
serving the clients. These will eventually close once they are no longer busy.

