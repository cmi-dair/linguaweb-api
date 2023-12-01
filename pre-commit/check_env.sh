if [[ ! -f .env ]]; then
    echo "WARNING: .env file not found"
    exit 0
fi

if [[ ! -f .env.example ]]; then
    echo "ERROR: .env.example file not found"
    exit 1
fi

# Check if all keys in .env.example are present in .env
env_keys=$(grep -v '^#' .env | cut -d= -f1 | sort)
example_keys=$(grep -v '^#' .env.example | cut -d= -f1 | sort)

if [[ "$env_keys" != "$example_keys" ]]; then
    echo "ERROR: .env and .env.example keys do not match" >&2
    exit 1
fi
