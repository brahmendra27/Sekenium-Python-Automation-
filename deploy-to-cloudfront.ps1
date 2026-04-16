# Deploy Allure Reports to AWS S3/CloudFront
# Usage: .\deploy-to-cloudfront.ps1 [-BucketName "my-bucket"] [-Region "us-east-1"]

param(
    [string]$BucketName = "",
    [string]$Region = "us-east-1",
    [switch]$CreateCloudFront = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploy Allure Reports to AWS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is installed
Write-Host "Checking prerequisites..." -ForegroundColor Cyan
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Host "❌ AWS CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install AWS CLI:" -ForegroundColor Yellow
    Write-Host "  Option 1: scoop install aws" -ForegroundColor Gray
    Write-Host "  Option 2: Download from https://aws.amazon.com/cli/" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "✅ AWS CLI found" -ForegroundColor Green

# Check if AWS credentials are configured
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "✅ AWS credentials configured" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Gray
    Write-Host "   User: $($identity.Arn)" -ForegroundColor Gray
} catch {
    Write-Host "❌ AWS credentials not configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please configure AWS credentials:" -ForegroundColor Yellow
    Write-Host "  aws configure" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You'll need:" -ForegroundColor Yellow
    Write-Host "  - AWS Access Key ID" -ForegroundColor Gray
    Write-Host "  - AWS Secret Access Key" -ForegroundColor Gray
    Write-Host "  - Default region (e.g., us-east-1)" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Check if Allure is installed
if (-not (Get-Command allure -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Allure not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Allure:" -ForegroundColor Yellow
    Write-Host "  scoop install allure" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host "✅ Allure found" -ForegroundColor Green
Write-Host ""

# Generate bucket name if not provided
if ($BucketName -eq "") {
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $BucketName = "allure-reports-$timestamp"
    Write-Host "📝 Generated bucket name: $BucketName" -ForegroundColor Cyan
} else {
    Write-Host "📝 Using bucket name: $BucketName" -ForegroundColor Cyan
}

Write-Host "📍 Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check for Allure results
Write-Host "Step 1: Checking for Allure results..." -ForegroundColor Cyan

if (-not (Test-Path "reports/allure-results")) {
    Write-Host "❌ No Allure results found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run tests first:" -ForegroundColor Yellow
    Write-Host "  pytest tests/ --alluredir=reports/allure-results -v" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$resultFiles = Get-ChildItem "reports/allure-results" -File
Write-Host "✅ Found $($resultFiles.Count) result files" -ForegroundColor Green
Write-Host ""

# Step 2: Generate static Allure report
Write-Host "Step 2: Generating static Allure report..." -ForegroundColor Cyan

if (Test-Path "reports/allure-report") {
    Write-Host "   Cleaning old report..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "reports/allure-report"
}

allure generate reports/allure-results -o reports/allure-report --clean 2>&1 | Out-Null

if (Test-Path "reports/allure-report/index.html") {
    Write-Host "✅ Static report generated" -ForegroundColor Green
    $reportSize = (Get-ChildItem "reports/allure-report" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "   Report size: $([math]::Round($reportSize, 2)) MB" -ForegroundColor Gray
} else {
    Write-Host "❌ Failed to generate report!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Create S3 bucket
Write-Host "Step 3: Creating S3 bucket..." -ForegroundColor Cyan

try {
    $bucketExists = aws s3 ls s3://$BucketName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "⚠️  Bucket already exists, will update contents" -ForegroundColor Yellow
    } else {
        aws s3 mb s3://$BucketName --region $Region 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ S3 bucket created" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to create bucket!" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Error checking/creating bucket: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 4: Configure bucket for static website hosting
Write-Host "Step 4: Configuring static website hosting..." -ForegroundColor Cyan

aws s3 website s3://$BucketName `
    --index-document index.html `
    --error-document index.html 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Static website hosting configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Could not configure website hosting" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Set bucket policy for public read
Write-Host "Step 5: Setting bucket policy for public access..." -ForegroundColor Cyan

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

$policyFile = "temp-bucket-policy-$(Get-Random).json"
$policy | Out-File -FilePath $policyFile -Encoding utf8

try {
    # Disable block public access
    aws s3api put-public-access-block `
        --bucket $BucketName `
        --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false" 2>&1 | Out-Null
    
    # Apply bucket policy
    aws s3api put-bucket-policy --bucket $BucketName --policy file://$policyFile 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Bucket policy set (public read access)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: Could not set bucket policy" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Warning: Error setting bucket policy: $_" -ForegroundColor Yellow
} finally {
    Remove-Item $policyFile -ErrorAction SilentlyContinue
}

Write-Host ""

# Step 6: Upload Allure report
Write-Host "Step 6: Uploading Allure report to S3..." -ForegroundColor Cyan
Write-Host "   This may take a minute..." -ForegroundColor Gray

$uploadStart = Get-Date

aws s3 sync reports/allure-report/ s3://$BucketName/allure-report/ `
    --acl public-read `
    --cache-control "max-age=3600" `
    --delete 2>&1 | Out-Null

$uploadDuration = (Get-Date) - $uploadStart

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Upload complete ($([math]::Round($uploadDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "❌ Upload failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Generate URLs
$s3WebsiteUrl = "http://$BucketName.s3-website-$Region.amazonaws.com/allure-report/"
$s3DirectUrl = "https://$BucketName.s3.amazonaws.com/allure-report/index.html"

# Step 7: CloudFront (optional)
if ($CreateCloudFront) {
    Write-Host "Step 7: Creating CloudFront distribution..." -ForegroundColor Cyan
    Write-Host "   ⏳ This takes 15-20 minutes to deploy globally..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Creating distribution..." -ForegroundColor Gray
    
    # Note: Full CloudFront setup requires more complex configuration
    # This is a simplified version
    Write-Host "   ⚠️  CloudFront creation requires additional configuration" -ForegroundColor Yellow
    Write-Host "   Please create manually via AWS Console or use AWS CDK/Terraform" -ForegroundColor Yellow
    Write-Host ""
}

# Display results
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Your Allure report is now available at:" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 S3 Website URL (Recommended):" -ForegroundColor Cyan
Write-Host "   $s3WebsiteUrl" -ForegroundColor White
Write-Host ""
Write-Host "🔗 S3 Direct URL (Alternative):" -ForegroundColor Cyan
Write-Host "   $s3DirectUrl" -ForegroundColor White
Write-Host ""
Write-Host "📝 Bucket Details:" -ForegroundColor Cyan
Write-Host "   Name: $BucketName" -ForegroundColor White
Write-Host "   Region: $Region" -ForegroundColor White
Write-Host "   Path: s3://$BucketName/allure-report/" -ForegroundColor White
Write-Host ""
Write-Host "🔄 To update the report:" -ForegroundColor Yellow
Write-Host "   1. Run tests: pytest tests/ --alluredir=reports/allure-results -v" -ForegroundColor Gray
Write-Host "   2. Deploy: .\deploy-to-cloudfront.ps1 -BucketName '$BucketName'" -ForegroundColor Gray
Write-Host ""
Write-Host "🗑️  To delete the bucket:" -ForegroundColor Yellow
Write-Host "   aws s3 rb s3://$BucketName --force" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: Bookmark the URL and share with your team!" -ForegroundColor Cyan
Write-Host ""

# Open in browser
$openBrowser = Read-Host "Open report in browser? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process $s3WebsiteUrl
}
