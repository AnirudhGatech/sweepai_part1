![image](https://github.com/AnirudhGatech/sweepai_part1/assets/143911409/2c3b9176-63c2-4f77-8b1c-69920c0566f5)

# Repository Code Change Automation- SWEEP AI Emulation

This Python script automates the process of making code changes in multiple GitHub repositories, creating pull requests for those changes, and managing the execution of these changes in a database. It leverages the power of the OpenAI GPT-3 model for code modification generation.

## Prerequisites

Before you can use this automation script, make sure you have the following set up:

1. GitHub Token: You'll need a GitHub token to access your repositories and create pull requests. Replace `"your_github_token"` with your actual GitHub token in the script.

2. Organization: Specify the name of your organization by replacing `"your_organization"` in the script.

3. OpenAI API Key: You need an OpenAI API key to use the GPT-3 model for code generation. Replace `"your_openai_api_key"` with your actual OpenAI API key.

4. Database Setup: The script uses a database to track the status of code changes in repositories. Ensure you have set up the database correctly using the `evadb` library. You may need to modify the database connection code in the script according to your setup.

5. Dependencies: Make sure you have the required Python libraries installed, such as `os`, `path`, `github`, `evadb`, and `openai`.

## Usage

1. Configure the script by updating the necessary tokens and organization name.

2. Define the repositories you want to process and their base branches in the `repositories_to_base` dictionary.

3. Specify the `ticket` and `branch` for tracking changes and branch creation.

4. Customize the code changes and descriptions as needed in the `execute_changes` function.

5. Run the script, and it will automate the following steps for each repository in the list:

   - Clone the GitHub repository.
   - Prepare a new branch for code changes.
   - Use the OpenAI GPT-3 model to generate code modifications.
   - Check for changes and commit them to the repository.
   - Create a pull request in the GitHub repository with relevant information.
   - Update the database to mark the repository as processed.

6. The script will also clean up by removing the cloned repositories from the local file system.


