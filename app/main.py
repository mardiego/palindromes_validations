from app.controller import delete_record
from app.controller import validate_record
from app.controller import get_records
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from typing import Optional

app = FastAPI()


# Method to validate if a string is a palindrome
@app.post("/palindromes/validate_palindromes")
async def validate_palindromes(request: Request):
    try:
        print("Validate Palindrome")
        # Parse the JSON body
        body = await request.json()
        result = validate_record(body)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Missing fields"
            )
        else:
            return JSONResponse(
                content={'response': result},
                status_code=201
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request"
        )


# Method to return and filter the stored palindromes
@app.get("/palindromes/get_palindromes")
async def get_palindromes(text: Optional[str] = None,
                          language: Optional[str] = None):
    try:
        print("Get Palindromes")
        records = get_records(text, language)
        if not records:
            raise HTTPException(
                status_code=404,
                detail=f"No Palindromes found"
            )
        return JSONResponse(
            content={"message": "Palindromes records matching filter", 'Palindromes': records},
            status_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request"
        )

# Method to delete a palindrome
@app.delete("/palindromes/delete_palindromes")
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