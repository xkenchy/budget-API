
# Elastic Beanstalk Deployment Guide

## 1. Start from Scratch

### 1.1. Prepare Your Application

```bash
# Change to your app directory
cd /path/to/your/app

# Ensure .ebextensions directory and config files are correct
ls .ebextensions

# Package your application into a zip file
zip -r myapp.zip .
```

### 1.2. Open CloudShell

```bash
# Open CloudShell in your AWS Console
aws cloudshell start
```

### 1.3. Upload Your Zip to CloudShell

```bash
# Upload the zip file to CloudShell
# In the CloudShell terminal:
mv myapp.zip /path/to/cloudshell/
```

### 1.4. Create a New Beanstalk Application and Environment

```bash
# Initialize a new Elastic Beanstalk application
eb init -p python-3.7 myapp

# Create a new environment and deploy your app
eb create my-env

# Set environment variables if needed
eb setenv DB_USER=postgres DB_PASSWORD=your_password DB_HOST=your_host DB_PORT=5432 DB_NAME=your_db_name
```

### 1.5. Deploy Your Application

```bash
# Deploy the application
eb deploy

# Check the application health
eb health
```

### 1.6 Ensure EC2 allows all outbound traffic, give it a security group
### make RDS accept traffic from that security group 

## 2. Deploy New Changes to the Same Beanstalk Environment

### 2.1. Prepare Your Updated Application

```bash
# Change to your app directory
cd /path/to/your/app

# Package your updated application into a zip file
zip -r myapp.zip .
```

### 2.2. Open CloudShell

```bash
# Open CloudShell in your AWS Console
aws cloudshell start
```

### 2.3. Upload Your Updated Zip to CloudShell

```bash
# Upload the updated zip file to CloudShell
mv myapp.zip /path/to/cloudshell/
```

### 2.4. Deploy the Updated Application

```bash
# Deploy the updated application
eb deploy

# Check the application health
eb health
```

### 2.5. Check for Environment Variables

```bash
# If you need to update environment variables:
eb setenv DB_USER=postgres DB_PASSWORD=your_password DB_HOST=your_host DB_PORT=5432 DB_NAME=your_db_name
```

### 2.6. Restarting the Environment (if necessary)

```bash
# Restart the environment if needed
eb restart
```

# End of Guide
