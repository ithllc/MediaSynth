import os
import subprocess
import json
import re
import logging

# --- Logging Setup ---
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'), # Overwrite log file each run
        logging.StreamHandler()
    ]
)
# --- End Logging Setup ---

def analyze_image(image_path):
    """
    Analyzes a single image using the Gemini CLI.
    """
    logging.info(f"--- Starting analyze_image for: {image_path} ---")
    
    prompt = f"@MediaSynth/photos/{os.path.basename(image_path)} Analyze this photo. Return a JSON object with the following keys: 'description', 'inferred_location', 'subjects', and 'dominant_emotion'. Be descriptive."
    logging.info(f"Generated prompt: {prompt}")
    
    command = [
        "gemini",
        "-p", prompt,
        #"--model", "gemini-1.5-pro",
    ]
    logging.info(f"Running command: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"Command stdout for {image_path}:\n{result.stdout}")
        logging.info(f"Command stderr for {image_path}:\n{result.stderr}")

        json_str = result.stdout.strip()
        logging.info("Attempting to find JSON block in output.")
        match = re.search(r"```json\n({.*?})\n```", json_str, re.DOTALL)
        if match:
            json_str = match.group(1)
            logging.info("Found JSON block using regex.")
            logging.info(f"Attempting to parse JSON: {json_str}")
            parsed_json = json.loads(json_str)
            logging.info("Successfully parsed JSON.")
            return parsed_json
        else:
            logging.warning("Could not find JSON block using regex. Falling back to curly brace search.")
            start_index = json_str.find('{')
            end_index = json_str.rfind('}') + 1
            if start_index != -1 and end_index != -1:
                json_str = json_str[start_index:end_index]
                logging.info("Found potential JSON using curly braces.")
                logging.info(f"Attempting to parse JSON: {json_str}")
                parsed_json = json.loads(json_str)
                logging.info("Successfully parsed JSON.")
                return parsed_json
            else:
                logging.error(f"No JSON object found in the output for {image_path}")
                return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error analyzing {image_path}: {e}")
        logging.error(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON for {image_path}: {e}")
        logging.error(f"Raw output that failed to parse: {json_str}")
        return None
    finally:
        logging.info(f"--- Finished analyze_image for: {image_path} ---")


def generate_linkedin_post(photo_analyses):
    """
    Generates a LinkedIn post from a list of photo analyses.
    """
    logging.info("--- Starting generate_linkedin_post ---")
    
    # Create a summarized version of the analyses to avoid long prompts
    summarized_analyses = [
        {
            "description": analysis.get("description"),
            "dominant_emotion": analysis.get("dominant_emotion")
        } 
        for analysis in photo_analyses
    ]
    
    prompt = f'''You are a social media manager. I'll provide a JSON array of photo analyses. Create a professional and engaging LinkedIn post that weaves these photos into a narrative. Use the descriptions and emotions to build the story. Include relevant hashtags. Format the output as a JSON object with 'post_text' and 'image_to_post' keys. Here is the photo data: {json.dumps(summarized_analyses)}'''
    logging.info("Generated LinkedIn prompt.")

    command = [
        "gemini",
        "-p", prompt,
    ]
    logging.info(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"LinkedIn post generation stdout:\n{result.stdout}")
        logging.info(f"LinkedIn post generation stderr:\n{result.stderr}")

        json_str = result.stdout.strip()
        logging.info("Attempting to find JSON in LinkedIn post output.")
        match = re.search(r"```json\n({.*?})\n```", json_str, re.DOTALL)
        if match:
            json_str = match.group(1)
            logging.info("Found JSON block using regex.")
            logging.info(f"Attempting to parse JSON: {json_str}")
            parsed_json = json.loads(json_str)
            logging.info("Successfully parsed JSON.")
            return parsed_json
        else:
            logging.warning("Could not find JSON block using regex. Falling back to curly brace search.")
            start_index = json_str.find('{')
            end_index = json_str.rfind('}') + 1
            if start_index != -1 and end_index != -1:
                json_str = json_str[start_index:end_index]
                logging.info("Found potential JSON using curly braces.")
                logging.info(f"Attempting to parse JSON: {json_str}")
                parsed_json = json.loads(json_str)
                logging.info("Successfully parsed JSON.")
                return parsed_json
            else:
                logging.error("No JSON object found in the LinkedIn post generation output.")
                return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating LinkedIn post: {e}")
        logging.error(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON for LinkedIn post: {e}")
        logging.error(f"Raw output that failed to parse: {json_str}")
        return None
    finally:
        logging.info("--- Finished generate_linkedin_post ---")


def main():
    """
    Main function to run the photo analysis and post generation.
    """
    logging.info("--- Starting main function ---")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    photos_dir = os.path.join(script_dir, "photos")
    outputs_dir = os.path.join(script_dir, "outputs")
    
    logging.info(f"Script directory: {script_dir}")
    logging.info(f"Photos directory: {photos_dir}")
    logging.info(f"Outputs directory: {outputs_dir}")

    if not os.path.exists(outputs_dir):
        logging.info(f"Creating outputs directory: {outputs_dir}")
        os.makedirs(outputs_dir)

    image_files = [os.path.join(photos_dir, f) for f in os.listdir(photos_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    logging.info(f"Found {len(image_files)} image file(s).")
    
    if not image_files:
        logging.warning("No images found in the 'photos' directory. Exiting.")
        return

    all_analyses = []
    for image_path in image_files:
        analysis = analyze_image(image_path)
        if analysis:
            logging.info(f"Successfully analyzed {image_path}. Appending to results.")
            all_analyses.append(analysis)
        else:
            logging.warning(f"Analysis failed for {image_path}, skipping.")

    if not all_analyses:
        logging.error("No images were successfully analyzed. Exiting.")
        return

    logging.info("Starting LinkedIn post generation with collected analyses.")
    linkedin_post_data = generate_linkedin_post(all_analyses)

    if linkedin_post_data and 'post_text' in linkedin_post_data:
        post_text = linkedin_post_data['post_text']
        
        output_path = os.path.join(outputs_dir, "linkedin_post.txt")
        
        logging.info(f"Writing LinkedIn post to {output_path}")
        try:
            with open(output_path, "w") as f:
                f.write(post_text)
            logging.info("Successfully wrote post to file.")
        except IOError as e:
            logging.error(f"Failed to write to {output_path}: {e}")
        
        print("\n--- Generated LinkedIn Post ---")
        print(post_text)
        print(f"\nPost saved to {output_path}")
        
        # Mocking the LinkedIn API call
        print("\n--- Mocking LinkedIn API Call ---")
        print(f"Image to post: {linkedin_post_data.get('image_to_post', 'N/A')}")
        print("Post would be published to LinkedIn here.")
    else:
        logging.error("Failed to generate LinkedIn post data or 'post_text' key was missing.")

    logging.info("--- Finished main function ---")

if __name__ == "__main__":
    main()
