from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Assuming write_post.py is in the same directory
from write_post import generate_post

app = FastAPI()

class PostResponse(BaseModel):
    facebook_post: str
    instagram_post: str
    email_blast_post: str

@app.get("/generate_posts", response_model=PostResponse)
async def get_generated_posts(topic: str):
    """
    Generates marketing posts for a given restaurant topic across Facebook, Instagram, and Email Blast.
    """
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    facebook_post = generate_post("facebook", topic)
    instagram_post = generate_post("instagram", topic)
    email_blast_post = generate_post("email_blast", topic)

    if "Error generating post" in facebook_post or \
       "Error generating post" in instagram_post or \
       "Error generating post" in email_blast_post:
        raise HTTPException(status_code=500, detail="Failed to generate one or more posts. Check API key and network connection.")

    return PostResponse(
        facebook_post=facebook_post,
        instagram_post=instagram_post,
        email_blast_post=email_blast_post
    )

# To run this API locally:
# 1. Make sure you have uvicorn installed: uv pip install uvicorn
# 2. Run the command: uvicorn api:app --reload
# 3. Access in your browser: http://127.0.0.1:8000/generate_posts?topic=Greek

