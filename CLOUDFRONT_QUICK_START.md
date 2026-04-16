# ☁️ CloudFront Deployment - Quick Start

## 🚀 Deploy Your Allure Reports to AWS in 3 Steps

### Step 1: Install AWS CLI (One-time)

```powershell
# Using Scoop (Recommended)
scoop install aws

# Or download from: https://aws.amazon.com/cli/
```

### Step 2: Configure AWS Credentials (One-time)

```powershell
aws configure
```

You'll need:
- **AWS Access Key ID** (from AWS Console → IAM → Users → Security Credentials)
- **AWS Secret Access Key** (from same place)
- **Default region**: `us-east-1` (or your preferred region)
- **Output format**: `json`

### Step 3: Deploy!

```powershell
# Run the deployment script
.\deploy-to-cloudfront.ps1
```

**That's it!** Your report will be available at a URL like:
```
http://allure-reports-20260416-123456.s3-website-us-east-1.amazonaws.com/allure-report/
```

---

## 📊 What You Get

### ✅ Public URL
Share with your team:
```
http://your-bucket.s3-website-us-east-1.amazonaws.com/allure-report/
```

### ✅ Always Accessible
- No need to run local server
- Access from anywhere
- Works on mobile devices

### ✅ Historical Reports
- Keep multiple versions
- Track trends over time
- Compare test runs

### ✅ Professional
- HTTPS support (with CloudFront)
- Fast global access
- Custom domain (optional)

---

## 🔄 Update Reports (After Running Tests)

```powershell
# 1. Run tests
pytest tests/playwright/test_allure_demo.py --alluredir=reports/allure-results -v

# 2. Deploy updated report (use same bucket name)
.\deploy-to-cloudfront.ps1 -BucketName "your-existing-bucket-name"
```

---

## 💰 Cost

**Extremely cheap!**
- S3 Storage: ~$0.0002/month for 10MB report
- S3 Requests: ~$0.01/month for 100 views
- **Total: ~$0.02/month** (less than a penny!)

---

## 🎯 Use Cases

### 1. Share with Team
```
"Hey team, check out the latest test results:
http://my-reports.s3-website-us-east-1.amazonaws.com/allure-report/"
```

### 2. CI/CD Integration
```yaml
# GitHub Actions
- name: Deploy Report
  run: .\deploy-to-cloudfront.ps1 -BucketName "ci-test-reports"
```

### 3. Historical Tracking
```
reports-2026-04-16/  ← Today's report
reports-2026-04-15/  ← Yesterday's report
reports-2026-04-14/  ← Day before
```

---

## 🔒 Security Options

### Option 1: Public (Current)
- ✅ Easy to share
- ✅ No authentication
- ⚠️ Anyone with URL can access

### Option 2: Private (Add Authentication)
```powershell
# Remove public access
aws s3api put-bucket-policy --bucket your-bucket --policy file://private-policy.json
```

Then use:
- AWS Cognito for user authentication
- CloudFront signed URLs for time-limited access
- VPN for internal-only access

---

## 📚 Full Documentation

- **Complete Guide**: `CLOUDFRONT_DEPLOYMENT_GUIDE.md`
- **Allure Guide**: `ALLURE_REPORTING_GUIDE.md`
- **Your Report Guide**: `YOUR_ALLURE_REPORT_GUIDE.md`

---

## 🆘 Troubleshooting

### Issue: "AWS CLI not found"
```powershell
scoop install aws
```

### Issue: "Credentials not configured"
```powershell
aws configure
```

### Issue: "Bucket already exists"
```powershell
# Use a different bucket name
.\deploy-to-cloudfront.ps1 -BucketName "my-unique-bucket-name-$(Get-Random)"
```

### Issue: "Access Denied"
Make sure your AWS user has these permissions:
- `s3:CreateBucket`
- `s3:PutObject`
- `s3:PutBucketPolicy`
- `s3:PutBucketWebsite`

---

## 🎉 Summary

### Before:
```
❌ Report only on local machine
❌ Need to run server to view
❌ Can't share with team
❌ No historical tracking
```

### After:
```
✅ Report hosted on AWS
✅ Access via URL
✅ Share with anyone
✅ Keep historical versions
✅ Professional presentation
✅ Costs ~$0.02/month
```

---

## 🚀 Next Steps

1. **Deploy your first report**
   ```powershell
   .\deploy-to-cloudfront.ps1
   ```

2. **Share the URL with your team**
   ```
   http://your-bucket.s3-website-us-east-1.amazonaws.com/allure-report/
   ```

3. **Set up CI/CD** (optional)
   - Auto-deploy after test runs
   - Keep historical reports
   - Track trends over time

4. **Add CloudFront** (optional)
   - HTTPS support
   - Custom domain
   - Faster global access

---

**Your Allure reports can now be shared with the world!** ☁️✨

Run `.\deploy-to-cloudfront.ps1` to get started!
