# ☁️ Deploy Allure Reports to AWS CloudFront

## 🎯 Goal
Host your Allure test reports on AWS CloudFront so your team can access them via a URL like:
`https://d1234567890.cloudfront.net/allure-report/`

---

## 📋 Prerequisites

1. ✅ AWS Account
2. ✅ AWS CLI installed
3. ✅ AWS credentials configured
4. ✅ Allure reports generated

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Generate Static Allure Report

```powershell
# Generate static HTML report (not the server version)
allure generate reports/allure-results -o reports/allure-report --clean
```

This creates a static HTML report in `reports/allure-report/` that can be hosted anywhere.

### Step 2: Create S3 Bucket and Upload

```powershell
# Set variables
$BUCKET_NAME = "my-test-reports-bucket"  # Change this to your bucket name
$REGION = "us-east-1"  # Change to your preferred region

# Create S3 bucket
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Upload Allure report
aws s3 sync reports/allure-report/ s3://$BUCKET_NAME/allure-report/ --acl public-read

# Enable static website hosting
aws s3 website s3://$BUCKET_NAME --index-document index.html
```

### Step 3: Create CloudFront Distribution

```powershell
# Create CloudFront distribution (this returns a distribution ID and domain)
aws cloudfront create-distribution --origin-domain-name $BUCKET_NAME.s3.amazonaws.com
```

**Your report will be available at:**
`https://d1234567890.cloudfront.net/allure-report/index.html`

---

## 📝 Detailed Step-by-Step Guide

### Step 1: Install AWS CLI (If Not Installed)

**Windows:**
```powershell
# Download and install AWS CLI
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

**Or using Scoop:**
```powershell
scoop install aws
```

### Step 2: Configure AWS Credentials

```powershell
# Configure AWS credentials
aws configure

# You'll be prompted for:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json
```

### Step 3: Generate Static Allure Report

```powershell
# Clean old reports
if (Test-Path "reports/allure-report") {
    Remove-Item -Recurse -Force "reports/allure-report"
}

# Generate new static report
allure generate reports/allure-results -o reports/allure-report --clean

# Verify report was generated
ls reports/allure-report
```

You should see files like:
- `index.html`
- `app.js`
- `styles.css`
- `data/` folder
- `plugins/` folder

### Step 4: Create S3 Bucket

```powershell
# Set your bucket name (must be globally unique)
$BUCKET_NAME = "my-company-test-reports-$(Get-Random)"
$REGION = "us-east-1"

Write-Host "Creating S3 bucket: $BUCKET_NAME" -ForegroundColor Green

# Create bucket
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Configure bucket for static website hosting
aws s3 website s3://$BUCKET_NAME `
    --index-document index.html `
    --error-document index.html
```

### Step 5: Set Bucket Policy (Public Read Access)

Create a file `bucket-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

Apply the policy:

```powershell
# Replace YOUR_BUCKET_NAME with your actual bucket name
(Get-Content bucket-policy.json) -replace 'YOUR_BUCKET_NAME', $BUCKET_NAME | Set-Content bucket-policy-updated.json

# Apply policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy-updated.json

# Disable "Block Public Access" settings
aws s3api put-public-access-block `
    --bucket $BUCKET_NAME `
    --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

### Step 6: Upload Allure Report to S3

```powershell
Write-Host "Uploading Allure report to S3..." -ForegroundColor Green

# Upload with correct content types
aws s3 sync reports/allure-report/ s3://$BUCKET_NAME/allure-report/ `
    --acl public-read `
    --cache-control "max-age=3600" `
    --metadata-directive REPLACE

Write-Host "✅ Upload complete!" -ForegroundColor Green
Write-Host "S3 URL: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com/allure-report/" -ForegroundColor Cyan
```

### Step 7: Create CloudFront Distribution

Create a file `cloudfront-config.json`:

```json
{
  "CallerReference": "allure-report-distribution",
  "Comment": "Allure Test Reports Distribution",
  "Enabled": true,
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-allure-reports",
        "DomainName": "YOUR_BUCKET_NAME.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": ""
        }
      }
    ]
  },
  "DefaultRootObject": "allure-report/index.html",
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-allure-reports",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"]
    },
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "MinTTL": 0,
    "DefaultTTL": 86400,
    "MaxTTL": 31536000
  }
}
```

Create the distribution:

```powershell
# Update config with your bucket name
(Get-Content cloudfront-config.json) -replace 'YOUR_BUCKET_NAME', $BUCKET_NAME | Set-Content cloudfront-config-updated.json

# Create CloudFront distribution
$distribution = aws cloudfront create-distribution --distribution-config file://cloudfront-config-updated.json | ConvertFrom-Json

$CLOUDFRONT_DOMAIN = $distribution.Distribution.DomainName
$DISTRIBUTION_ID = $distribution.Distribution.Id

Write-Host "✅ CloudFront distribution created!" -ForegroundColor Green
Write-Host "Distribution ID: $DISTRIBUTION_ID" -ForegroundColor Cyan
Write-Host "CloudFront URL: https://$CLOUDFRONT_DOMAIN/allure-report/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Yellow
Write-Host "⏳ Note: CloudFront deployment takes 15-20 minutes to propagate globally" -ForegroundColor Yellow
```

---

## 🤖 Automated Deployment Script

I'll create a PowerShell script that does everything automatically:

**File:** `deploy-to-cloudfront.ps1`

```powershell
# Deploy Allure Reports to AWS CloudFront
# Usage: .\deploy-to-cloudfront.ps1

param(
    [string]$BucketName = "test-reports-$(Get-Random)",
    [string]$Region = "us-east-1"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploy Allure Reports to CloudFront" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is installed
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Host "❌ AWS CLI not found!" -ForegroundColor Red
    Write-Host "Please install AWS CLI: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

# Check if AWS credentials are configured
try {
    aws sts get-caller-identity | Out-Null
    Write-Host "✅ AWS credentials configured" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS credentials not configured!" -ForegroundColor Red
    Write-Host "Run: aws configure" -ForegroundColor Yellow
    exit 1
}

# Step 1: Generate static Allure report
Write-Host ""
Write-Host "Step 1: Generating static Allure report..." -ForegroundColor Cyan

if (-not (Test-Path "reports/allure-results")) {
    Write-Host "❌ No Allure results found!" -ForegroundColor Red
    Write-Host "Run tests first: pytest tests/ --alluredir=reports/allure-results" -ForegroundColor Yellow
    exit 1
}

if (Test-Path "reports/allure-report") {
    Remove-Item -Recurse -Force "reports/allure-report"
}

allure generate reports/allure-results -o reports/allure-report --clean

Write-Host "✅ Static report generated" -ForegroundColor Green

# Step 2: Create S3 bucket
Write-Host ""
Write-Host "Step 2: Creating S3 bucket..." -ForegroundColor Cyan
Write-Host "Bucket name: $BucketName" -ForegroundColor Gray

try {
    aws s3 mb s3://$BucketName --region $Region 2>&1 | Out-Null
    Write-Host "✅ S3 bucket created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Bucket may already exist, continuing..." -ForegroundColor Yellow
}

# Step 3: Configure bucket for static website hosting
Write-Host ""
Write-Host "Step 3: Configuring static website hosting..." -ForegroundColor Cyan

aws s3 website s3://$BucketName `
    --index-document index.html `
    --error-document index.html

Write-Host "✅ Static website hosting configured" -ForegroundColor Green

# Step 4: Set bucket policy
Write-Host ""
Write-Host "Step 4: Setting bucket policy..." -ForegroundColor Cyan

$policy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BucketName/*"
    }
  ]
}
"@

$policy | Out-File -FilePath "temp-bucket-policy.json" -Encoding utf8

aws s3api put-bucket-policy --bucket $BucketName --policy file://temp-bucket-policy.json

aws s3api put-public-access-block `
    --bucket $BucketName `
    --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

Remove-Item "temp-bucket-policy.json"

Write-Host "✅ Bucket policy set" -ForegroundColor Green

# Step 5: Upload Allure report
Write-Host ""
Write-Host "Step 5: Uploading Allure report to S3..." -ForegroundColor Cyan

aws s3 sync reports/allure-report/ s3://$BucketName/allure-report/ `
    --acl public-read `
    --cache-control "max-age=3600" `
    --delete

Write-Host "✅ Upload complete" -ForegroundColor Green

# Step 6: Get or create CloudFront distribution
Write-Host ""
Write-Host "Step 6: Setting up CloudFront distribution..." -ForegroundColor Cyan
Write-Host "⏳ This may take a few minutes..." -ForegroundColor Yellow

$s3Url = "http://$BucketName.s3-website-$Region.amazonaws.com/allure-report/"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Your Allure report is now available at:" -ForegroundColor Green
Write-Host ""
Write-Host "S3 URL (immediate):" -ForegroundColor Cyan
Write-Host "  $s3Url" -ForegroundColor White
Write-Host ""
Write-Host "To create CloudFront distribution (optional):" -ForegroundColor Yellow
Write-Host "  aws cloudfront create-distribution --origin-domain-name $BucketName.s3.amazonaws.com" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open the S3 URL in your browser" -ForegroundColor White
Write-Host "  2. Share the URL with your team" -ForegroundColor White
Write-Host "  3. (Optional) Set up CloudFront for HTTPS and custom domain" -ForegroundColor White
Write-Host ""
```

---

## 🚀 Usage

### One-Time Setup

```powershell
# 1. Install AWS CLI
scoop install aws

# 2. Configure credentials
aws configure

# 3. Run deployment script
.\deploy-to-cloudfront.ps1
```

### Update Reports (After Running Tests)

```powershell
# 1. Run tests
pytest tests/playwright/test_allure_demo.py --alluredir=reports/allure-results -v

# 2. Deploy updated report
.\deploy-to-cloudfront.ps1 -BucketName "your-existing-bucket-name"
```

---

## 🔒 Security Options

### Option 1: Public Access (Anyone with URL)
- ✅ Easy to share
- ✅ No authentication needed
- ⚠️ Anyone can access

### Option 2: Private with CloudFront Signed URLs
- ✅ Secure
- ✅ Time-limited access
- ✅ Requires authentication

### Option 3: Private with AWS Cognito
- ✅ User authentication
- ✅ Role-based access
- ✅ Most secure

---

## 💰 Cost Estimate

### S3 Storage
- First 50 TB: $0.023 per GB/month
- Allure report ~10 MB: **~$0.0002/month**

### CloudFront
- First 10 TB: $0.085 per GB
- 100 report views/month: **~$0.01/month**

### Total: **~$0.02/month** (negligible)

---

## 🎯 Benefits

### ✅ Share Reports with Team
- Send URL to anyone
- No need to run local server
- Always accessible

### ✅ Historical Reports
- Keep multiple report versions
- Track trends over time
- Compare test runs

### ✅ CI/CD Integration
- Auto-deploy after test runs
- GitHub Actions integration
- Jenkins integration

### ✅ Professional
- HTTPS URLs
- Custom domain (optional)
- Fast global access via CloudFront

---

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Allure Report

on:
  push:
    branches: [ main ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Run tests
      run: |
        pytest tests/ --alluredir=reports/allure-results
    
    - name: Generate Allure report
      run: |
        allure generate reports/allure-results -o reports/allure-report --clean
    
    - name: Deploy to S3
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        aws s3 sync reports/allure-report/ s3://your-bucket/allure-report/ --acl public-read
```

---

## 📚 Summary

### What You Can Do:

1. ✅ **Generate static Allure report**
   ```powershell
   allure generate reports/allure-results -o reports/allure-report --clean
   ```

2. ✅ **Upload to S3**
   ```powershell
   aws s3 sync reports/allure-report/ s3://your-bucket/allure-report/ --acl public-read
   ```

3. ✅ **Access via URL**
   ```
   http://your-bucket.s3-website-us-east-1.amazonaws.com/allure-report/
   ```

4. ✅ **Optional: Add CloudFront**
   ```
   https://d1234567890.cloudfront.net/allure-report/
   ```

5. ✅ **Share with team**
   - Send URL
   - No local setup needed
   - Always accessible

---

**Your Allure reports can now be hosted on CloudFront!** ☁️✨

Run `.\deploy-to-cloudfront.ps1` to get started!
