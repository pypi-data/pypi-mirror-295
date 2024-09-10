# 📝 pymemos

Supercharge your note-taking with pymemos - your Python-based command-line companion for the Memos API!

## 🚀 Features

- ✍️ Create, read, update, and delete memos
- 🏷️ Manage memo visibility (Private, Protected, Public)
- 📂 List and manage resources
- 🗑️ Bulk delete all memos
- 🖥️ Clean, intuitive command-line interface
- 🐞 Debug logging for troubleshooting

## 🛠️ Installation

Get up and running in no time:

```
    pip install pymemos
```

## Configuration

Before using pymemos, you need to set the following environment variables:

- `MEMOS_BASE_URL`: The base URL of your Memos API (e.g., `http://localhost:5230`)
- `MEMOS_ACCESS_TOKEN`: Your access token (required)

You can set these in your shell:

```bash
export MEMOS_BASE_URL="http://your-memos-instance.com/api/v1"
export MEMOS_ACCESS_TOKEN="your-access-token"
```

## 🎮 Usage

After installation and configuration, you can use the `memos` command to interact with your Memos instance:

```bash
memos [command] [options]
```

Available commands:

- `create`: Create a new memo
- `list`: List all memos
- `get`: Retrieve a specific memo
- `update`: Update an existing memo
- `delete`: Delete a specific memo
- `delete-all`: Delete all memos (use with caution!)
- `list-resources`: List all resources

### Examples

1. Create a new memo:
   ```
   memos create --content "Remember to buy groceries" --visibility PRIVATE
   ```

2. List all memos:
   ```
   memos list
   ```

3. Get a specific memo:
   ```
   memos get <memo_uid>
   ```

4. Update a memo:
   ```
   memos update <memo_uid> --content "Updated content"
   ```

5. Delete a memo:
   ```
   memos delete <memo_uid>
   ```

6. Delete all memos:
   ```
   memos delete-all
   ```
   Use the `--force` flag to skip the confirmation prompt:
   ```
   memos delete-all --force
   ```

## 🐞 Debugging

To enable debug logging, use the `--debug` flag with any command:

```bash
memos --debug [command] [options]
```

Debug logs are written to `memos_debug.log` in the current directory.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Memos](https://github.com/usememos/memos) - The open-source, self-hosted memo hub