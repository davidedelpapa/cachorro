#!/bin/bash

PACKAGE_NAME="cachorro"

echo "Building the package..."
python setup.py sdist bdist_wheel

WHEEL_FILE=$(ls dist/*.whl | head -n 1)

# Uninstall old version first
if pip show $PACKAGE_NAME > /dev/null 2>&1; then
    echo "Uninstalling the old version of the package..."
    pip uninstall -y $PACKAGE_NAME
fi

echo "Installing the new version of the package..."
pip install $WHEEL_FILE

echo "Verifying the installation..."
python -c "from cachorro import VERSION; print(f'Version: {VERSION}')"

echo "Done! The package has been built and installed successfully."
