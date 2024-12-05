import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    """Generate a random password based on user-defined criteria."""
    
    # Create an empty character pool based on user preferences
    character_pool = ''
    
    if use_letters:
        character_pool += string.ascii_letters  # Includes both lowercase and uppercase letters
    if use_numbers:
        character_pool += string.digits  # Includes numbers 0-9
    if use_symbols:
        character_pool += string.punctuation  # Includes common symbols
    
    # Check if the character pool is empty
    if not character_pool:
        raise ValueError("At least one character type must be selected.")
    
    # Generate a random password from the character pool
    password = ''.join(random.choice(character_pool) for _ in range(length))
    
    return password

def main():
    print("Welcome to the Password Generator!")
    
    # Get user input for password criteria
    try:
        length = int(input("Enter the desired password length (minimum 8): "))
        if length < 8:
            raise ValueError("Password length must be at least 8.")
        
        use_letters = input("Include letters? (y/n): ").strip().lower() == 'y'
        use_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'
        
        # Generate the password
        password = generate_password(length, use_letters, use_numbers, use_symbols)
        
        print(f"Generated Password: {password}")
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()