# Weather API Service (FastAPI app with AWS integration)

This project implements a weather API service using FastAPI that fetches weather data from an external public API - OpenWeatherMap. The service is designed to handle high traffic using asynchronous programming and integrates with AWS services (S3 and DynamoDB) to store and retrieve weather data.

## Features
- Asynchronous fetching of weather data using FastAPI and Python's `asyncio`.
- Caching of weather data in AWS S3 to minimize external API calls.
- Logs weather fetch events to AWS DynamoDB.
- Fully containerized using Docker and Docker Compose for easy setup and deployment.

---

## Requirements

- Python 3.9+
- Docker and Docker Compose
- AWS account with S3 and DynamoDB configured
- OpenWeatherMap API key

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MariiaBurda/FastAPIWeatherApp.git
cd FastAPIWeatherApp
```
### 2. AWS configure
Here are the steps to obtain the required AWS credentials and configurations:

#### 1. Sign In or Register in AWS Console:
- Navigate to the AWS Management Console.
- Log in with your credentials, or create a new account if you don’t have one.

#### 2. Create an S3 Bucket:
- Go to the S3 service from the AWS Management Console.
 Click on Create Bucket and follow the prompts to set up your bucket.
- Note the bucket name (e.g., S3_BUCKET_NAME) for later use.

#### 3. Create a DynamoDB Table:
- Navigate to the DynamoDB service.
- Click on Create Table and configure the required fields.
- Note the table name (e.g., DYNAMODB_TABLE).

#### 4. Create an IAM User with Full Access:
- Go to the IAM service in the AWS Console.
- Under Users, click on Add Users.
- Provide a name for the user and select Programmatic Access.
- Click Next and attach the following managed policies to grant full access to S3 and DynamoDB: 
AmazonS3FullAccess and AmazonDynamoDBFullAccess
- Complete the user creation process.
- Obtain AWS Credentials: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
- Save these credentials securely, as they will not be shown again.

#### 5. Select AWS Region: 
- Identify and select the AWS region you want to use (e.g., us-east-1). This will be your AWS_REGION.

### 3. Weather API key configure
- [Go to OpenWeatherMap](https://openweathermap.org/) to sign up and generate an API key from your account dashboard.

### 3. Environment Variables
You can now use the collected information from steps 2 and 3 to configure the `.env` file:
   ```plaintext
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   S3_BUCKET_NAME=your_s3_bucket_name
   WEATHER_API_KEY=your_weather_api_key
   DYNAMODB_TABLE_NAME=your_dynamodb_table_name
   ```

### 3. Build and Run with Docker Compose
1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. Verify the application is running by visiting:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Test it via browser http://127.0.0.1:8000/weater?city=Kyiv or via command line
```bash
   curl http://127.0.0.1:8000/weater?city=Kyiv
   ```

---

## API Documentation

**GET /weather**

**Query Parameters:**
- `city` (string): The name of the city to fetch weather data for.

**Response Example:**
```json
{
  "source": "cache/api",
  "city": "London",
  "temperature": 15,
  "description": "clear sky",
  "s3_file": "London_20241218.json",
  "s3_url": "s3://your_bucket_name/London_20241218.json"
}
```

---

## Future Improvements
- Add unit and integration tests for critical functionality.
- Consider implementing a more efficient caching mechanism, such as using an in-memory cache like Redis, to 
reduce latency and dependency on S3 for frequent requests.
- Extend support for additional weather APIs.
- Consider deleting old data (requests older than 5 minutes) if historical data will not be needed in the future.
- Improve documentation
- Add logging
---
