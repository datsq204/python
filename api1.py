import uvicorn
from fastapi import FastAPI, Body
from fastapi import Depends, FastAPI , Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

security = HTTPBasic()
@app.post("/webhook")
async def handle_webhook(data: str = Body(...)):
    try:
        # Create a timestamped filename for better organization
        import datetime
        filename = f"webhook_data_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        # Open the file in append mode (creates if it doesn't exist)
        with open(filename, "a", encoding="utf-8") as file:
            file.write(data + "\n")  # Append data with a newline character
        return "Data successfully written to file."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error occurred while processing data."

@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"datsq": credentials.username, "fit@3011": credentials.password}

@app.post("/token")
async def login(req: Request, form_data: OAuth2PasswordRequestForm = Depends()):

    # Get header's data from the raw request
    # or from the swagger login form
    user = form_data.username
    print(user)
    print(req.headers["fit@3011"])

    return {"access_token": user, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)