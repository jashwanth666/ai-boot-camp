import ollama
import time

# Configuration
MODEL = "gemma4:e4b"

# Pre-defined roles
roles = {
    "1": {
        "name": "Python Tutor",
        "prompt": "You are a patient and encouraging Python tutor. Your goal is to help the user understand Python concepts by providing clear explanations and small code snippets. If the user asks about something else, politely redirect them to Python."
    },
    "2": {
        "name": "Fitness Coach",
        "prompt": "You are an energetic and motivating fitness coach. You provide workout advice, posture tips, and encouragement. Your tone is upbeat and professional."
    },
    "3": {
        "name": "Travel Guide",
        "prompt": "You are an experienced and knowledgeable world travel guide. You offer travel recommendations, cultural insights, and logistical tips for various destinations."
    }
}

def display_menu():
    """Prints the available roles and commands."""
    print("\n" + "="*30)
    print("      ROLE-BASED CHAT")
    print("="*30)
    print("Available Roles:")
    for key, role in roles.items():
        print(f"{key}. {role['name']}")
    print("\nCommands:")
    print("- Type 'switch' to change role")
    print("- Type 'quit' to exit")
    print("- Type 'roles' to add a custom role")
    print("="*30)

def add_custom_role():
    """Allows the user to add a new system prompt role."""
    name = input("\nEnter the name for your new role: ").strip()
    prompt = input("Enter the system prompt (instructions) for this role: ").strip()
    if name and prompt:
        new_id = str(len(roles) + 1)
        roles[new_id] = {"name": name, "prompt": prompt}
        print(f"\nSuccess! Role '{name}' added as option {new_id}.")
    else:
        print("\nError: Name and prompt cannot be empty.")

def main():
    messages = []
    current_role_id = None

    while True:
        # If no role is selected, show the menu and get choice
        if current_role_id is None:
            display_menu()
            choice = input("\nPick a role (number) or type a command: ").strip().lower()
            
            if choice == 'quit':
                print("Goodbye!")
                break
            elif choice == 'roles':
                add_custom_role()
                continue
            elif choice in roles:
                current_role_id = choice
                messages = [{"role": "system", "content": roles[current_role_id]["prompt"]}]
                print(f"\n>>> Role set to: {roles[current_role_id]['name']}")
                print(">>> Type your message to start chatting.")
                continue
            else:
                print("\nInvalid choice. Please pick a number from the menu.")
                continue

        # Chat loop
        user_input = input("\nYou: ").strip()

        # Handle commands during chat
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'switch':
            current_role_id = None
            print("\nSwitching role...")
            continue
        elif user_input.lower() == 'roles':
            add_custom_role()
            print("\nUse 'switch' to change to your new role if desired.")
            continue
        
        if not user_input:
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        try:
            print(f"\n[{roles[current_role_id]['name']} is thinking...]")
            
            start_time = time.time()
            response = ollama.chat(
                model=MODEL,
                messages=messages
            )
            duration = time.time() - start_time
            
            assistant_content = response['message']['content']
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": assistant_content})
            
            print(f"\n{roles[current_role_id]['name']}: {assistant_content}")
            print(f"\n[Response time: {duration:.2f}s]")
            
        except Exception as e:
            print(f"\nError: Could not connect to Ollama. Make sure it's running and the model '{MODEL}' is pulled.")
            print(f"Details: {e}")
            # Reset to menu to allow switching model or quitting
            current_role_id = None

if __name__ == "__main__":
    main()
