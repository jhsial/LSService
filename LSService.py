import asyncio
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
import subprocess

app = Starlette()


async def directory_list(request: Request):

    try:
        # Parse JSON data from the request
        data = await request.json()
    except ValueError:
        return JSONResponse({"error": "Invalid JSON format"}, 400) # return status code 400

    # Validate request parameters
    if 'path' not in data:
        return JSONResponse({"error": "Missing request parameter: path"}, 400) # return status code 400

    if 'response_delay' not in data:
        response_delay = 0
    else:
        response_delay = data.get("response_delay")

    path = data.get("path")

    # Check if the specified folder exists
    ls_process = subprocess.Popen(['ls', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ls_output, ls_error = ls_process.communicate()

    if ls_process.returncode != 0: # Return status code 404
        return JSONResponse({"error": f"Folder '{path}' does not exist or could not be listed"},404)

    # Parse the ls command output to a list of file names
    files = ls_output.decode().strip().split('\n')

    # Now wait for number of seconds in response delay to simulate blocking request
    await asyncio.sleep(response_delay)

    return JSONResponse(files, 200) # Return status code 200


# Set up the routs in starlette framework
app.routes.append(Route("/dir/list", directory_list, methods=["POST"]))