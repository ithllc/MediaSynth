## File locking and collaborator access

This repository marks `main.py` and `README.md` as lockable via Git LFS and designates
code owners who should review changes to these files.

Important notes:

- Git LFS file locking prevents other collaborators from pushing changes to a locked file
  while you hold the lock. It does not prevent users from cloning/downloading the repo.
- To prevent unauthorized edits by non-collaborators, use GitHub repository settings:
  - Make the repository private (if not already).
  - Use the "Manage access" page to add collaborators and control their role (Admin, Write, Read).
  - Enable branch protection rules for `main` and require pull request reviews from code owners.

How to lock a file (developer steps):

```bash
# Install Git LFS and enable in the repo
git lfs install

# Ensure the .gitattributes entry is committed (this repo already has it)
git add .gitattributes
git commit -m "Mark main.py and README.md as lockable"

# Lock a file before editing
git lfs lock main.py

# Make your changes, commit, and push
git add main.py
git commit -m "Edit main.py"
git push

# Unlock after finishing
git lfs unlock main.py
```

How to require code owner review and guard edits:

1. Go to the repository Settings -> Branches -> Add rule for `main`.
2. Check "Require pull request reviews before merging".
3. Check "Require review from Code Owners".
4. Optionally require status checks or restrict pushes to administrators.

If you want me to enable or automate any of these settings, I can prepare a GitHub Actions workflow
or provide exact instructions, but I cannot change repository settings directly from this tool.
