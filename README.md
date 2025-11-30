Shipping Order System with Approval Workflow
A Streamlit-based web application that demonstrates a shipping order system with an approval workflow for large orders.

Features
Order Submission: Submit shipping requests with container count and destination
Automatic Approval: Orders with 5 or fewer containers are auto-approved
Approval Workflow: Large orders (6+ containers) require manual approval
Real-time Processing: See live updates as orders are processed
Example Requests: Quick test with pre-filled order examples
Prerequisites
Python 3.7+
Streamlit
Required Python packages (install via pip install -r requirements.txt)
Installation
Clone the repository:
bash
git clone <repository-url>
cd kaggle25day2/day2b
Install dependencies:
bash
pip install -r requirements.txt
Running the Application
bash
streamlit run app2.py
The application will open in your default web browser at http://localhost:8501

How to Use
Submit an Order:
Enter a shipping request in the format: "Ship [number] containers to [destination]"
Example: "Ship 10 containers to Rotterdam"
Approval Process:
Orders with 5 or fewer containers are automatically approved
Larger orders will show an approval request
Click "Approve" or "Reject" as needed
Example Requests:
Use the example buttons at the bottom to test different scenarios
Project Structure
app2.py
: Main Streamlit application
day2.py
: Core business logic and workflow
requirements.txt: Python dependencies
Troubleshooting
If you encounter any issues:

Check the console for error messages
Ensure all dependencies are installed
Verify that 
day2.py
 is in the same directory as 
app2.py
License
[Specify your license here]
