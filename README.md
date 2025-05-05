How to Run the Tests
Make sure Python is installed on your computer. If not, install it first.

Create a virtual environment for your project. Run the following command in the terminal:

python -m venv myenv
Activate the virtual environment. Run the following command in the terminal:

source myenv/bin/activate
Install the required dependencies listed in the requirements.txt file. Run the following command:

pip install -r requirements.txt
Navigate to the project directory and run the tests using pytest. Run the following command:

python -m pytest -s -v