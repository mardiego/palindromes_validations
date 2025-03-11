from app.controller import delete_record
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from typing import Optional

app = FastAPI()


# Method to validate if a string is a palindrome
@app.get("/validate_palindromes")
async def validate_palindromes():
    return {"message": "Palindrome validation"}


# Method to return and filter the stored palindromes
@app.get("/get_palindromes")
async def get_palindromes():
    return {"message": "Palindromes list"}


# Method to delete a palindrome
@app.delete("/delete_palindromes")
async def delete_palindromes(language: Optional[str] = None,
                             text: Optional[str] = None,):
    print("Request to delete a Palindrome entry")
    try:
        result = delete_record(language, text)
        if result is True:
            return JSONResponse(
                content={"response": "Entry successfully deleted"},
                status_code=200
            )
        elif result is False:
            return Response(status_code=204)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Bad Request"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request"
        )


# Health check method
@app.get("/health")
async def health_check():
    print("Health check")
    return {"status": "ok"}