# Expense Tracker

The Expense Tracker is a full-stack, cloud-deployed web application that allows users to log, view, and analyze personal expenses. Built using Flask and MySQL, and deployed using Zappa on AWS Lambda.

## Features

- User registration and login (Flask-Login)
- Add expenses
- View expenses with category, amount, and date
- Dashboard with pie chart (Chart.js)
- Export expenses to CSV
- Serverless deployment using Zappa and AWS Lambda
- Integrated with MySQL (AWS RDS)

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Set up and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

# (Optional) Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Run the app locally
flask run
```

## Deployment with Zappa

```bash
# Initialize Zappa (only once)
zappa init

# Deploy the app
zappa deploy dev

# Update the app after making changes
zappa update dev

# To undeploy and remove resources
zappa undeploy dev
```

## License

MIT License

---