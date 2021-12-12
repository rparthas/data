
## Problem Definition
Banks run into losses when a customer doesn't pay their loans on time. Because of this, every year, banks have losses in crores, and this also impacts the country's economic growth to a large extent. In this hackathon, we look at various attributes such as funded amount, location, loan, balance, etc., to predict if a person will be a loan defaulter or not. 


## Dataset Description

Train.csv - 67463 rows x 35 columns (Includes target column as Loan Status)
Attributes
- ID: unique ID of representative
- Loan Amount: loan amount applied
- Funded Amount:loan amount funded
- Funded Amount Investor: loan amount approved by the investors
- Term: term of loan (in months)
- Batch Enrolled: batch numbers to representatives
- Interest Rate: interest rate (%) on loan
- Grade: grade by the bank
- Sub Grade: sub-grade by the bank
- Employment Duration: duration
- Home Ownership: Owner ship of home
- Verification Status: Income verification by the bank
- Payment Plan: if any payment plan has started against loan
- Loan Title: loan title provided
- Debit to Income: ratio of representative's total monthly debt repayment divided by self reported monthly income excluding mortgage
- Delinquency - two years: number of 30+ days delinquency in past 2 years
- Inquires - six months: total number of inquiries in last 6 months
- Open Account: number of open credit line in representative's credit line
- Public Record: number of derogatory public records
- Revolving Balance: total credit revolving balance
- Revolving Utilities: amount of credit a representative is using relative to revolving_balance
- Total Accounts: total number of credit lines available in representatives credit line
- Initial List Status: unique listing status of the loan - W(Waiting), F(Forwarded)
- Total Received Interest: total interest received till date
- Total Received Late Fee: total late fee received till date
- Recoveries: post charge off gross recovery
- Collection Recovery Fee: post charge off collection fee
- Collection 12 months Medical: total collections in last 12 months excluding medical collections
- Application Type: indicates when the representative is an individual or joint
- Last week Pay: indicates how long (in weeks) a representative has paid EMI after batch enrolled
- Accounts Delinquent: number of accounts on which the representative is delinquent
- Total Collection Amount: total collection amount ever owed
- Total Current Balance: total current balance from all accounts
- Total Revolving Credit Limit: total revolving credit limit
- Loan Status: 1 = Defaulter, 0 = Non Defaulters

The challenge is to predict the Loan Status 

# Source code
* model.ipynb - Jupyter Notebook to train and perform EDA
* train.py - Script to generate the trained and tuned model
* predict_loan_status.py - Script to run the model serving endpoint
* lambda_function.py - script to run the model endpoint as lambda
* Dockerfile - Building service as docker image
* LambdaDockerfile - Building lambda as docker image
* Pipfile - holds the dependencies for running the project locally

# How to run
Prerequisites : Python, Virtualenv
* Create virtual environment using the command ```python -m venv final_venv```
* Activate the environment by ```source final_venv/bin/activate```
* Run ```pip install --upgrade pip``` to upgrade pip
* Run ```pip install pipenv``` to install pipenv
* Run ```pipenv install``` to install the dependencies within the activated virtual environment
* Run ```python train.py``` to generate the model file
* Best parameters have been identified by running the notebook ```model.ipynb```
* Install jupyter-notebook if you need to run the notebook
* Once model is trained, you can run the prediction script locally by running 
```gunicorn --bind 0.0.0.0:9696 predict_loan_status:app```

* Sample Screenshot is provided for testing endpoint
![Local Endpoint](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/local_endpoint.png)

### Sample Data
```json
{
    "ID": 29092009,
    "Loan Amount": 19989,
    "Funded Amount": 8964,
    "Funded Amount Investor": 9399.521396,
    "Term": 59,
    "Batch Enrolled": "BAT3873588",
    "Interest Rate": 12.58098442,
    "Grade": "A",
    "Sub Grade": "B2",
    "Employment Duration": "MORTGAGE",
    "Home Ownership": 211833.6129,
    "Verification Status": "Source Verified",
    "Payment Plan": "n",
    "Loan Title": "Credit card refinancing",
    "Debit to Income": 35.76157679,
    "Delinquency - two years": 1,
    "Inquires - six months": 0,
    "Open Account": 12,
    "Public Record": 0,
    "Revolving Balance": 10286,
    "Revolving Utilities": 58.54007131,
    "Total Accounts": 41,
    "Initial List Status": "w",
    "Total Received Interest": 44.2672439,
    "Total Received Late Fee": 26.7526997,
    "Recoveries": 3.746518944,
    "Collection Recovery Fee": 0.476414667,
    "Collection 12 months Medical": 0,
    "Application Type": "INDIVIDUAL",
    "Last week Pay": 102,
    "Accounts Delinquent": 0,
    "Total Collection Amount": 31,
    "Total Current Balance": 470224,
    "Total Revolving Credit Limit": 9801
}
```

# Deploy in Docker
Prerequisites : Docker
* Run ```docker build . -t loan_status``` to build the docker image
* This expects the python files and trained model to be on same directory
* Run ```docker run -p 9696:9696 loan_status``` to start the service in docker
* Refer endpoint testing from above section to test the same

# Lambda Deployment
Prerequisites : AWS Account, aws-cli
* Ensure AWS credentials are stored in ```~/.aws/credentials```
* us-east-2 region is used in this project
* Run ```docker build -f LambdaDockerFile . -t loan-status``` to build the lambda image

## Elastic Container Registry
* Run ```aws configure``` to configure secret key, access key and region
* Run ```aws ecr create-repository --repository-name loan-status``` to create the ECR repository in aws
* Copy the repository name from the output ```arn:aws:ecr:us-east-2:<AccountNumber>:repository/loan-status```
* Run ```aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <AccountNumber>.dkr.ecr.us-east-2.amazonaws.com``` to login
* Run ```docker tag loan-status:latest <AccountNumber>.dkr.ecr.us-east-2.amazonaws.com/loan-status:latest``` to tag the image as ECR repository
* Run ```docker push <AccountNumber>.dkr.ecr.us-east-2.amazonaws.com/loan-status:latest``` to push the image to ECR

## Lambda
* Navigate to Lambda in AWS console
* Create Lambda function using the following screenshot
![Lambda Creation](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/lambda_function.png)
* Once created edit the configuration to increase the timeout and memory
![Lambda Configuration](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/function_configuration.png)
* Test the lambda function by providing the same input as given in Running section

## API Gateway
* Navigate to API gateway in AWS console
* Click on Build under Rest API
* Provide inputs similar to screenshot below
![API Gateway](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/api_gateway_create.png)
* In the next screen Click on Actions -> Create Method and choose the method as POST in dropdown
* Link the created lambda function similar to below screenshot
![Configuration](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/lambda_api_gateway.png)
* Once it is done, click on Test and provide the input to test the gateway
* Once it is verified, Click on Actions -> Deploy API to deploy to a new stage (prod)
* Use the generated url to verify if the endpoint is working fine
![Endpoint](https://github.com/rparthas/data/blob/master/zoomcamp/finalterm/images/api_testing.png)

# Cleaning up
* Clean the gateway,lambda and ECR
* Delete the docker container and image
* Run ```deactivate``` to exit from virtual environment
* Run ```rm -rf final_venv``` to remove the virtual environment