#!/bin/bash
#Author: abhiunix
#make python venv easiest than ever!


# Define the installation path
INSTALL_PATH="/usr/local/bin/superpy"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed! Please install Python3 first."
    exit 1
fi

# Check if venv module is available
if ! python3 -m venv --help &> /dev/null; then
    echo "⚠️ Python venv module is not installed. Installing it now..."

    # Determine the OS type
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # For Debian-based (Ubuntu, Debian)
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y python3-venv
        # For Fedora-based
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-venv
        else
            echo "❌ Could not determine package manager. Install python3-venv manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # For macOS
        if command -v brew &> /dev/null; then
            brew install python
        else
            echo "❌ Homebrew is not installed. Install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install python3-venv manually."
        exit 1
    fi
fi

# Create the superpy script
echo "✅ Creating superpy script at $INSTALL_PATH..."
sudo tee $INSTALL_PATH > /dev/null <<EOF
#!/bin/bash

# Get the last directory name from the current working directory
VENV_NAME=\$(basename "\$PWD")

# Define the virtual environment path
VENV_PATH="\$PWD/\$VENV_NAME"

# Check if the virtual environment already exists
if [ ! -d "\$VENV_PATH/bin" ]; then
    >&2 echo "Creating new virtual environment: \$VENV_NAME"
    python3 -m venv "\$VENV_NAME"
else
    # Print to stderr so it doesn't get "eval"-ed
    >&2 echo "Switching to existing virtual environment: \$VENV_NAME"
fi

# Print the command to activate the virtual environment
echo "source \"\$VENV_PATH/bin/activate\""
EOF

# Make the script executable
echo "✅ Making superpy executable..."
sudo chmod +x $INSTALL_PATH

# Add alias to .zshrc and .bashrc
echo "✅ Adding alias to shell configuration..."
echo 'alias superpy="eval \$(/usr/local/bin/superpy)"' | tee -a ~/.zshrc ~/.bashrc > /dev/null

# Reload the shell configuration
echo "✅ Reloading shell configuration..."
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null

echo "🎉 Installation complete! You can now use 'superpy' from any directory."
