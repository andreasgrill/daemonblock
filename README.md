# daemonblock
OSX utility that automatically unloads daemons and agents

Daemonblock regularly checks for the configured daemons/agents and makes sure that they remain unloaded, even if they have been readded at a later point in time.

## Install
- Extract daemonblock to a custom directory.
- Have a look at [example.config.json](example.config.json) and add custom service paths in [config.json](config.json).
- All added service paths in [config.json](config.json) will be permanently blocked and should even survive app updates.
- Open Terminal.app and cd in the custom directory.
- Run ```sudo ./daemonblock.py``` to complete installation.

