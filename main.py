import os
import subprocess
import json
import re

def analyze_image(image_path):
    """
    Analyzes a single image using the Gemini CLI.
    """
    print(f"Analyzing image: {image_path}")
    prompt = f"@file:{image_path} Analyze this photo. Return a JSON object with the following keys: 'description', 'inferred_location', 'subjects', and 'dominant_emotion'. Be descriptive."
    command = [
        "gemini",
        "-p", prompt,
        "--model", "gemini-1.5-pro",
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        json_str = result.stdout.strip()
        # Look for a JSON block within ```json ... ```
        match = re.search(r"```json\n({.*?})\n```", json_str, re.DOTALL)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            # Fallback to finding the first and last curly braces
            start_index = json_str.find('{')
            end_index = json_str.rfind('}') + 1
            if start_index != -1 and end_index != -1:
                json_str = json_str[start_index:end_index]
                return json.loads(json_str)
            else:
                print(f"Error: No JSON object found in the output for {image_path}")
                return None
    except subprocess.CalledProcessError as e:
        print(f"Error analyzing {image_path}: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {image_path}: {e}")
        print(f"Raw output: {result.stdout}")
        return None

def generate_linkedin_post(photo_analyses):
    """
    Generates a LinkedIn post from a list of photo analyses.
    """
    print("Generating LinkedIn post...")
    prompt = f"""You are a social media manager. I'll provide a JSON array of photo analyses. Create a professional and engaging LinkedIn post that weaves these photos into a narrative. Use the descriptions, locations, and emotions to build the story. Include relevant hashtags. Format the output as a JSON object with 'post_text' and 'image_to_post' keys. Here is the photo data: {json.dumps(photo_analyses)}"""
    command = [
        "gemini",
        "-p", prompt,
        "--model", "gemini-1.5-pro"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        json_str = result.stdout.strip()
        match = re.search(r"```json\n({.*?})\n```", json_str, re.DOTALL)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            start_index = json_str.find('{')
            end_index = json_str.rfind('}') + 1
            if start_index != -1 and end_index != -1:
                json_str = json_str[start_index:end_index]
                return json.loads(json_str)
            else:
                print("Error: No JSON object found in the LinkedIn post generation output.")
                return None
    except subprocess.CalledProcessError as e:
        print(f"Error generating LinkedIn post: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for LinkedIn post: {e}")
        print(f"Raw output: {result.stdout}")
        return None

def main():
    """
    Main function to run the photo analysis and post generation.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    photos_dir = os.path.join(script_dir, "photos")
    outputs_dir = os.path.join(script_dir, "outputs")
    
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    image_files = [os.path.join(photos_dir, f) for f in os.listdir(photos_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No images found in the 'photos' directory.")
        return

    photo_analyses = []
    for image_path in image_files:
        analysis = analyze_image(image_path)
        if analysis:
            photo_analyses.append(analysis)

    if not photo_analyses:
        print("No analyses were generated from the photos.")
        return

    linkedin_post_data = generate_linkedin_post(photo_analyses)

    if linkedin_post_data and 'post_text' in linkedin_post_data:
        post_text = linkedin_post_data['post_text']
        output_path = os.path.join(outputs_dir, "linkedin_post.txt")
        with open(output_path, "w") as f:
            f.write(post_text)
        
        print("\n--- Generated LinkedIn Post ---")
        print(post_text)
        print(f"\nPost saved to {output_path}")
        
        # Mocking the LinkedIn API call
        print("\n--- Mocking LinkedIn API Call ---")
        print(f"Image to post: {linkedin_post_data.get('image_to_post', 'N/A')}")
        print("Post would be published to LinkedIn here.")

if __name__ == "__main__":
    main()
