import os
import sys

def display_env_vars(filter_params=None):
    sorted_env_variables = sorted(os.environ.items())

    for key, value in sorted_env_variables:
        if filter_params is None or key in filter_params:
            print(f"{key}: {value}")

if __name__ == "__main__":
    filter_params = sys.argv[1:] if len(sys.argv) > 1 else None
    display_env_vars(filter_params)