# OLA-AI (OpenAI Compatible Language Assistant) CLI

OLA-AI is a command-line interface tool that helps you create, manage, and run AI-powered prompts using OpenAI Compatible API.

## Installation

You can install OLA-AI directly from PyPI:

```
pip install ola-ai
```

After installation, set up your OpenAI API key:

```
ola update_env --key=your_api_key --model=gpt-4o-mini --url=https://api.openai.com/v1
```
Config will be saved to `~/.ola_env` file

## Dependencies

OLA-AI relies on the following Python packages:

- Click
- PyYAML
- openai
- python-dotenv

These will be automatically installed when you install OLA-AI via pip.

## Usage

### Creating a prompt

To create a new prompt:

```
ola create [name] [prompt]
```
Prompts will be saved in `~/.ola_config.yaml` file
Example:
```
ola create joke "You are a comedian. Tell a joke about the topic the user provides."
```

### Running a prompt

To run a saved prompt:

```
ola run [name] [user_input]
```

Example:
```
ola run joke "programming"
```

### Listing prompts

To list all saved prompts:

```
ola list
```

### Deleting a prompt

To delete a saved prompt:

```
ola delete [name]
```

### Updating environment variables

To update the API key, model, or API base URL:

```
ola update_env --key=your_api_key --model=gpt-4o-mini --url=https://api.openai.com/v1
```

### Listing environment variables

To view the current environment settings:

```
ola list_env
```

### Checking the version

To check the version of the OLA-AI CLI:

```
ola --version
```

## Troubleshooting

1. **API Key Issues**: If you're getting authentication errors, make sure you've set your API key correctly using the `update_env` command.

2. **Command Not Found**: If you're getting a "command not found" error, ensure that the installation directory is in your system's PATH.

3. **Unexpected Errors**: Check the `ola.log` file in your current directory for more detailed error information.

## Roadmap

- [ ] Add support for multiple AI models
- [ ] Implement a web interface
- [ ] Add collaborative features for sharing prompts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.
