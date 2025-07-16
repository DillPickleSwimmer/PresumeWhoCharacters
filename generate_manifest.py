import os
import json
import random

# --- Configuration ---
GITHUB_USERNAME = "DillPickleSwimmer"
REPO_NAME = "PresumeWhoCharacters"
# The base path to your image directory within the repository
# (e.g., if images are in 'my-image-repo/images/', set this to 'images')
IMAGE_DIR_RELATIVE_PATH = ""
# The name of your JSON manifest file
JSON_FILE_NAME = "characters.json"
# List of image file extensions to include
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff')
# Subfolders to scan for gender categorization
GENDER_SUBFOLDERS = {
    "female": {"prefix": "Jane Doe ", "count": 1},
    "male": {"prefix": "John Doe ", "count": 1}
}

# --- Name Lists ---
FEMALE_NAMES = [
    "Sophia", "Olivia", "Emma", "Ava", "Isabella", "Mia", "Charlotte", "Amelia",
    "Harper", "Evelyn", "Abigail", "Emily", "Ella", "Elizabeth", "Camila",
    "Mila", "Aria", "Chloe", "Victoria", "Grace", "Luna", "Layla", "Lily",
    "Hannah", "Zoe", "Nora", "Scarlett", "Addison", "Eleanor", "Natalie",
    "Samantha", "Isla", "Leah", "Audrey", "Allison", "Maya", "Aurora", "Willow",
    "Anna", "Naomi", "Elena", "Sarah", "Clara", "Ruby", "Alice", "Hailey",
    "Lucy", "Sadie", "Piper", "Bella", "Stella", "Hazel", "Violet", "Penelope",
    "Josephine", "Georgia", "Madelyn", "Eliza", "Rose", "Kayla", "Eva", "Melanie",
    "Lillian", "Gabriella", "Nevaeh", "Summer", "Vivian", "Paisley", "Aaliyah",
    "Victoria", "Zara", "Skylar", "Genesis", "Maria", "Serenity", "Kennedy",
    "Alexa", "Valentina", "Rebecca", "Ariana", "Faith", "Autumn", "Destiny",
    "Amara", "Hope", "Jade", "Ruby", "Erin", "Felicity", "Gemma", "Harmony",
    "Ivy", "Jasmine", "Kendall", "Laura", "Mackenzie", "Nina", "Olive", "Paige",
    "Quinn", "Raelynn", "Savannah", "Tessa", "Uma", "Valeria", "Willa", "Ximena",
    "Yara", "Zoe", "Ashley", "Brooke", "Chelsea", "Danielle", "Elizabeth", "Frances",
    "Georgia", "Heather", "Irene", "Jessica", "Kimberly", "Lauren", "Megan", "Nicole",
    "Patricia", "Rachel", "Stephanie", "Taylor", "Vanessa", "Whitney", "Brenda",
    "Cynthia", "Deborah", "Emily", "Florence", "Gloria", "Holly", "Ivy", "Julie",
    "Karen", "Linda", "Mary", "Nancy", "Pamela", "Rosemary", "Sandra", "Theresa",
    "Ursula", "Virginia", "Wendy", "Yvonne", "Alicia", "Bianca", "Crystal", "Diana",
    "Erin", "Fiona", "Gina", "Heidi", "Ingrid", "Jocelyn", "Kara", "Lisa", "Monica",
    "Naomi", "Olga", "Paula", "Rita", "Suzanne", "Tina", "Una", "Vicky", "Wendy",
    "Yolanda", "Zena", "Susan", "Barbara", "Dorothy", "Elizabeth", "Helen", "Joyce",
    "Kathleen", "Margaret", "Nancy", "Ruth", "Shirley", "Virginia"
]

MALE_NAMES = [
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas",
    "Henry", "Theodore", "Jackson", "Sebastian", "Jack", "Ethan", "Daniel",
    "Michael", "Alexander", "Owen", "Asher", "Samuel", "Leo", "Grayson", "Luke",
    "Ezra", "Anthony", "Julian", "Hudson", "Dylan", "Gabriel", "Logan", "Mateo",
    "Maverick", "David", "Elias", "Matthew", "Ezra", "Levi", "Joseph", "Wyatt",
    "John", "Christopher", "Isaiah", "Andrew", "Joshua", "Nathan", "Christian",
    "Ryan", "Adrian", "Charles", "Thomas", "Aaron", "Caleb", "Connor", "Hunter",
    "Landon", "Jonathan", "Miles", "Lincoln", "Kai", "Colton", "Jordan", "Austin",
    "Robert", "Connor", "Nicholas", "Dominic", "Everett", "Carson", "Giovanni",
    "Adam", "Brandon", "Brian", "Bruce", "Carlos", "Dennis", "Douglas", "Edward",
    "Frank", "Gary", "Harold", "Jeffrey", "Kevin", "Larry", "Mark", "Paul",
    "Peter", "Richard", "Roger", "Scott", "Stephen", "Timothy", "Walter", "Wayne",
    "Arthur", "Barry", "Bryan", "Charles", "David", "Donald", "Edward", "George",
    "Harry", "Isaac", "Jacob", "Kenneth", "Louis", "Matthew", "Nathaniel", "Patrick",
    "Raymond", "Ronald", "Steven", "Thomas", "Vincent", "Victor", "William", "Xavier",
    "Zachary", "Abel", "Blake", "Clayton", "Derek", "Earl", "Floyd", "Gordon", "Harvey",
    "Ivan", "Jerry", "Keith", "Leo", "Malcolm", "Neal", "Oscar", "Philip", "Quentin",
    "Russell", "Sean", "Todd", "Ulysses", "Vernon", "Warren", "Xavier", "Yusuf", "Zane",
    "George", "James", "John", "Robert", "William", "Charles", "Frank", "Joseph",
    "Paul", "Richard", "Ronald", "Steven", "Kenneth", "Daniel", "Donald", "Mark"
]


# Subfolders to scan for gender categorization
# Key is the folder name, value is the list of names to use
GENDER_SUBFOLDERS_CONFIG = {
    "female": FEMALE_NAMES,
    "male": MALE_NAMES
}

# --- Script Logic ---

def generate_manifest():
    manifest_data = []
    
    # Ensure the base URL correctly points to the root of your GitHub Pages site
    base_url = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/blob/main/"
    
    # Global ID counter
    image_id_counter = 1

    # Get the absolute path to the main image directory
    main_image_dir_abs_path = os.path.join(os.getcwd(), IMAGE_DIR_RELATIVE_PATH)

    if not os.path.exists(main_image_dir_abs_path):
        print(f"Error: Image directory '{main_image_dir_abs_path}' not found. Please check IMAGE_DIR_RELATIVE_PATH configuration.")
        return

    # Prepare shuffled lists of names for each gender
    shuffled_gender_names = {}
    for gender, name_list in GENDER_SUBFOLDERS_CONFIG.items():
        shuffled_list = list(name_list) # Create a copy
        random.shuffle(shuffled_list)
        shuffled_gender_names[gender] = shuffled_list

    # Iterate through the defined gender subfolders
    for gender_folder_name, original_name_list in GENDER_SUBFOLDERS_CONFIG.items():
        gender_folder_abs_path = os.path.join(main_image_dir_abs_path, gender_folder_name)
        
        if not os.path.isdir(gender_folder_abs_path):
            print(f"Warning: Gender folder '{gender_folder_abs_path}' not found. Skipping.")
            continue

        # Get the specific shuffled list for this gender
        current_shuffled_names = shuffled_gender_names[gender_folder_name]

        # Get list of files in the current gender folder
        # Sort files to ensure consistent order across runs (important for ID, even if names are random)
        files_in_folder = [f for f in os.listdir(gender_folder_abs_path) if f.lower().endswith(IMAGE_EXTENSIONS)]
        files_in_folder.sort() # Sorting ensures predictable IDs for the same set of files

        for file_name in files_in_folder:
            # Construct the full relative path from the repo root
            full_relative_image_path = os.path.join(IMAGE_DIR_RELATIVE_PATH, gender_folder_name, file_name).replace(os.sep, '/')
            
            # Construct the full public URL
            image_url = os.path.join(base_url, full_relative_image_path, '?raw=true').replace(os.sep, '/')

            # Pick a name, ensuring no reuse until exhausted
            if current_shuffled_names:
                person_name = current_shuffled_names.pop(0) # Pop from the front of the shuffled list
            else:
                # Fallback: If we run out of unique names, print a warning and start reusing randomly
                print(f"Warning: Ran out of unique names for '{gender_folder_name}' folder. Reusing names from original list.")
                person_name = random.choice(original_name_list)


            image_data = {
                "id": image_id_counter,
                "name": person_name,
                "imageUrl": image_url # Renamed key as per request
            }
            manifest_data.append(image_data)
            image_id_counter += 1

    # Write the JSON data to the file
    json_output_path = os.path.join(os.getcwd(), JSON_FILE_NAME)
    with open(json_output_path, 'w') as f:
        json.dump(manifest_data, f, indent=2) # indent=2 for pretty printing

    print(f"Manifest '{JSON_FILE_NAME}' generated successfully with {len(manifest_data)} images.")
    print(f"Path: {json_output_path}")

if __name__ == "__main__":
    generate_manifest()
