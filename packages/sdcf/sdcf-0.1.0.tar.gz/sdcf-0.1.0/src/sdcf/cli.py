import sys
import os
import subprocess

def main():
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Future command-line functionality can be implemented here
        print("Command-line functionality not implemented yet.")
        print("Running the Streamlit app by default.")
        print("To access future CLI features, use: sdcf --cli")
    
    # Run the Streamlit app by default
    try:
        subprocess.run(["streamlit", "run", script_path], check=True)
    except subprocess.CalledProcessError:
        print("Streamlit app exited with an error.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStreamlit app stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    print("Thank you for using SDCF. Goodbye!")

    print("Yours sincerely,")

    print("Shankar Dutt")
    
if __name__ == "__main__":
    main()