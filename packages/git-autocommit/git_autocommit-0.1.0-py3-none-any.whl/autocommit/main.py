import sys
from autocommit.git_helpers import commit_changes

def main():
    if commit_changes():
        print("Commit process completed successfully.")
    else:
        print("Commit process failed.")

if __name__ == "__main__":
    sys.exit(main())