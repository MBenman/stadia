# GitHub Actions entrypoint script
# This script will receive arguments from the action's metadata file

# Change to the workspace directory (GitHub will mount the workspace here)
cd "$GITHUB_WORKSPACE" || exit 1

# If args are provided, use them; otherwise use default behavior
if [ $# -gt 0 ]; then
    # Arguments were passed from the action metadata
    echo "Running with provided arguments: $*"
    exec "$@"
else
    # No arguments provided, run the default Django/Gunicorn server
    echo "No arguments provided, starting Gunicorn server..."
    exec gunicorn --bind 0.0.0.0:8000 --workers 3 stadiapi.wsgi:application
fi