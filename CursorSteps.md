This readme explains the steps taken to create a simple one time use token service using AWS CDK, Lambda, DynamoDB, and API Gateway. The project was created using the interactive chat feature of Cursor AI.

### 1. Install cursor and configure a pro subscription: https://www.cursor.com/

### 2. Install the following components, if needed on your development machine

1. NPM. On Mac, install with homebrew: `brew install npm`
1. AWS CLI. On Mac, install with homebrew: `brew install awscli`
1. Python. On Mac, install with homebrew: brew install python AWS CDK. `pip install aws-cdk`
1. Install Docker Desktop, used for bundling Lambda functions with the CDK: https://www.docker.com/products/docker-desktop/

### 3. Using the terminal, create an empty project folder

```
mkdir tokenservice
cd tokenservice
cdk init app --language=python
```

### 4. Create the CDK project

Open the Cursor chat for the tokenservice project `(CMD-K/CTL-K)`, ensure claude-3.5-sonnet is the selected model, and enter the following prompt:

```
Update the current tokenservice_stack.py file in Python with a public api gateway that include two methods.

1/ The first method is a GET, implemented as an AWS Lambda function, and will issue a signed jwt token with a uuid and ttl of 8 hours. The uuid of the token will be stored in a dynamodb table.

2/ The second method is a POST, integrated as an AWS Lambda function, and will validate the token by checking if the token's uuid is present in the dynamodb table and if it has not expired. If the token is valid, it will return a 200 status code with a message "Token validated successfully" and remove that row from the dynamodb table. If the token is invalid, or the uuid does not exist in the dynamo db table it will return a 401 status code and a message "Invalid or expired token".

Also create the Lambda function implementations in python as separate python files in a lambda_functions directory.
```

1. Apply and accept the changes to the tokenservice_stack.py file.
1. Apply and accept the creation of the issue_token.py file.
1. Apply and accept the creation of the validate_token.py file.
1. Apply and accept the creation of the requirements.tst file.
1. Run the bash command to use pip for installation of the required dependencies.

### 5. Install the aws cdk libraries into the Python enviroment
`pip install aws-cdk-lib`, if needed

### 6. Deploy the stack
1. Create an aws profile, preferable with tempoorary credentials with AWS SSO and the AWS CLI
1. `cdk bootstrap --profile <your_profile>`
1. `cdk deploy --profile <your_profile>`
1. Confirm with `y` you want to deploy the stack. Wait for it to complete

### 7. Update the CDK stack using cursor chat to bundle the python packages

Open the Cursor chat for the tokenservice project `(CMD-K/CTL-K)` and enter the following prompt:

```Update the CDK tokenservice_stack.py lambda functions to bundle python packages with the code using python```

Apply/accept the changes and redeploy the cdk stack
`cdk deploy --profile <your_profile>`

After deploying and testing, there was an IAM error which required an explicit static table name. Use the Cursor editor to identify the error, apply/accept changes, and deploy again.

### 8. Open the Cursor chat for the tokenservice project `(CMD-K/CTL-K)` and enter the following prompt:

```Help with this error: [ERROR] ClientError: An error occurred (AccessDeniedException) when calling the PutItem operation: User: arn:aws:sts::724772059364:assumed-role/TokenserviceStack-IssueTokenFunctionServiceRole619B-k5ZR9zj4WkKP/TokenserviceStack-IssueTokenFunction8194C3D3-XaxioPMp5jQK is not authorized to perform: dynamodb:PutItem on resource: arn:aws:dynamodb:us-east-1:724772059364:table/TokenTable because no identity-based policy allows the dynamodb:PutItem action```

### 9. Create A Python Test Client

Using Cursor chat, create a test client with the following prompt.

Open the Cursor chat for the tokenservice project `(CMD-K/CTL-K)` and enter the following prompt:

```Create a python web client in a separate file that calls the API to get a token and then posts it to the API```

Apply/accept the changes 

### 10. Install Test Client Dependencies
Run `pip install requests` to install the requests library in the current python environment.

### 11. Configure and Run the Test Client

Substitue the APIGW URL into the client script (remove trailing slash if needed) and run it `python3 token_client.py`

### 12. Create a HTML Test Client

Create a simple HTML client that uses the API Gateway endpoint to get and validate tokens.

Open the Cursor chat for the tokenservice project `(CMD-K/CTL-K)` and enter the following prompt:

```Create a html, css, and javascript single page web app that has a button to call the api and get a token. The web page should display the token encoded and decoded. The web page should have a second button to verify the token and show the validation result.```

1. Apply/accept the changes into an index.html file
1. Change the APIGW base url in the index.html file to the one for your stack

```Update the CDK stack to deploy the index.html file as a S3 public website.```

1. Deploy the stack again and navigate to the website url to test.
1. Profit!


### Troubleshooting
If you run into integration or config issues, paste the errors into Cursor chat, apply/accept changes, and retest.