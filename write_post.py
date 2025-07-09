import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def generate_post(platform, topic):
    """
    Generates a post using the OpenAI API based on the platform and topic.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if platform == "facebook":
        prompt = f"Generate a Facebook post for a {topic} restaurant. Focus on engaging the audience and encouraging visits. Keep it concise and include a call to action."
    elif platform == "instagram":
        prompt = f"Generate an Instagram caption for a {topic} restaurant. Focus on visual appeal, use relevant hashtags, and encourage sharing. Keep it short and sweet."
    elif platform == "email_blast":
        prompt = f"Generate a short email blast content for a {topic} restaurant. Announce a special offer or new menu item, and include a clear call to action to book a table or order online."
    else:
        return "Invalid platform specified."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can change to a different model if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates marketing content for restaurants."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200, # Adjust as needed
            temperature=0.7 # Adjust as needed
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating post for {platform}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Generate marketing posts for a restaurant.")
    parser.add_argument("topic", type=str, help="The topic/cuisine of the restaurant (e.g., 'Greek', 'Mediterranean', 'Filipino').")
    args = parser.parse_args()

    restaurant_topic = args.topic

    print(f"Generating posts for a {restaurant_topic} restaurant...\n")

    # Generate Facebook post
    facebook_post = generate_post("facebook", restaurant_topic)
    print("--- Facebook Post ---")
    print(facebook_post)
    print("\n")

    # Generate Instagram post
    instagram_post = generate_post("instagram", restaurant_topic)
    print("--- Instagram Post ---")
    print(instagram_post)
    print("\n")

    # Generate Email Blast post
    email_blast_post = generate_post("email_blast", restaurant_topic)
    print("--- Email Blast Post ---")
    print(email_blast_post)
    print("\n")

if __name__ == "__main__":
    main()
