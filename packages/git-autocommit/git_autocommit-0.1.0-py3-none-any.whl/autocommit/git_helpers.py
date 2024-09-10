import ollama
import subprocess

SYS_PROMPT = """
Below is a git diff. Please analyze the changes and generate a concise, clear, and meaningful git commit message. Ensure the message explains what was done and why, focusing on actions like 'fix', 'add', 'update', or 'refactor'. If relevant, mention performance improvements, bug fixes, or dependency updates. Always restrict the message length to one or two lines and use active language. 

Always return the commit message in lowercase. 

You should only return the commit message, and nothing else.
"""

def get_git_diff() -> str | None:
    try:
        # add staged, unstaged, and untracked changes
        staged = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True, check=True).stdout
        unstaged = subprocess.run(['git', 'diff'], capture_output=True, text=True, check=True).stdout
        untracked = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout
        
        if untracked:
            untracked = "Untracked files:\n" + untracked

        all_changes = f"{staged}\n{unstaged}\n{untracked}".strip()
        
        if not all_changes:
            print("No changes detected in the repository.")
            return None
        
        return all_changes

    except subprocess.CalledProcessError as e:
        print(f"Error running git commands: {e}")
        return None
    except FileNotFoundError:
        print("Git command not found. Make sure Git is installed and in your PATH.")
        return None


def generate_commit_message():

    git_diff = get_git_diff()
    if git_diff is None or git_diff.strip() == "":
        print("No changes detected or unable to get git diff.")
        return None

    response = ollama.chat(model="llama3", messages=[
        {
            'role': 'user',
            'content': SYS_PROMPT 
        },
        {
            'role': 'user',
            'content': git_diff
        }
    ])

    return response['message']['content']

def commit_changes():
    try:
        subprocess.run(['git', 'add', '-A'], check=True)
        commit_message = generate_commit_message()

        if commit_message is None:
            print("No commit message generated. Exiting.")
            return False

        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"Changes committed successfully with message: {commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        return False
    except FileNotFoundError:
        print("Git command not found. Make sure Git is installed and in your PATH.")
        return False