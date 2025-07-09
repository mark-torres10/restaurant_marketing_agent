import json
import os

def dump_file_content_as_json_string(file_path, secret_name):
    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
        print(f"\n--- Copy this content for {secret_name} secret in Replit ---")
        print(json.dumps(content, indent=2))
        print(f"------------------------------------------------------------------\n")
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure it's in the same directory as this script.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}. Please ensure it's a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    credentials_path = os.path.join(current_dir, 'credentials.json')
    token_path = os.path.join(current_dir, 'token.json')

    print("\n--- Dumping Google Credentials and Token to JSON Strings ---")

    dump_file_content_as_json_string(credentials_path, "GOOGLE_CREDENTIALS_JSON")
    dump_file_content_as_json_string(token_path, "GOOGLE_TOKEN_JSON")

    print("\n--- Copy the above output and paste into Replit Secrets ---")

