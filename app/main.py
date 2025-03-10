from fastapi import FastAPI

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
async def delete_palindromes():
    return {"message": "Palindrome deleted"}

# Health check method
@app.get("/health")
async def health_check():
    print("Health check")
    return {"status": "ok"}