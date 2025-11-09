# MongoDB Atlas Connection Issues - Troubleshooting Guide

## Current Issue
`[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error` when connecting from GCP Cloud Run to MongoDB Atlas.

## Root Cause Analysis
This error typically indicates one of the following:
1. **TLS/SSL version mismatch** between Cloud Run's Python environment and MongoDB Atlas
2. **Network configuration issues** in MongoDB Atlas  
3. **Certificate validation problems**
4. **MongoDB Atlas IP whitelist restrictions**

## Solutions to Try

### Solution 1: Check MongoDB Atlas Network Access (MOST LIKELY)
The error might be because Cloud Run's IP addresses are not whitelisted in MongoDB Atlas.

**Steps:**
1. Go to MongoDB Atlas dashboard: https://cloud.mongodb.com/
2. Navigate to your cluster → Network Access
3. Check if you have IP whitelist entries
4. **Add entry: `0.0.0.0/0`** to allow all IPs (for testing - narrow down in production)
5. Wait 2-3 minutes for changes to propagate
6. Test the connection again

### Solution 2: Verify MongoDB Connection String
Ensure your connection string format is correct for MongoDB Atlas:

```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
```

**Check these:**
- Username and password are URL-encoded (no special characters like @, :, etc.)
- Cluster name is correct  
- Database name matches your intended database

### Solution 3: Test Connection Locally
Run the test script locally to verify the connection works outside Cloud Run:

```bash
cd /Users/tedlu/Desktop/townpass-dev/backend
python3 test_mongodb_connection.py
```

This will help determine if the issue is environment-specific or configuration-related.

### Solution 4: Alternative - Use MongoDB Standard Connection
If `mongodb+srv://` continues to fail, try using a standard connection string:

In MongoDB Atlas:
1. Go to your cluster → Connect → Connect your application
2. Choose "Standard connection string" instead of "DNS Seedlist connection"  
3. Update your `MONGODB_URI` secret with the new connection string
4. Format: `mongodb://<host1>:27017,<host2>:27017,<host3>:27017/<database>?ssl=true&replicaSet=<replica-set-name>&authSource=admin`

### Solution 5: Alternative Database Options

If MongoDB Atlas continues to have connection issues from Cloud Run, consider these alternatives:

#### Option A: Google Cloud Firestore
- Native GCP service, excellent integration with Cloud Run
- No SSL/network configuration needed
- Minimal code changes required

#### Option B: Cloud SQL (PostgreSQL/MySQL)
- Managed database service on GCP
- Direct Cloud Run integration with Cloud SQL Proxy
- No network/SSL issues

#### Option C: Self-hosted MongoDB on GCP
- Deploy MongoDB on Compute Engine or GKE
- Full control over configuration
- Use VPC peering for secure access

## Recommended Action Plan

1. **FIRST** - Check MongoDB Atlas Network Access settings (Solution 1)
   - This is the most likely cause
   - Add `0.0.0.0/0` to allow all IPs
   
2. **SECOND** - Run local test script (Solution 3)
   ```bash
   cd backend
   python3 test_mongodb_connection.py
   ```

3. **THIRD** - If still failing, switch to standard connection string (Solution 4)

4. **LAST RESORT** - Consider alternative database options (Solution 5)

## Checking Current Deployment Status

```bash
# Check logs
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="townpass-backend"' \
  --limit=20 --format="table(timestamp,textPayload)" --freshness=5m

# Test health endpoint
curl https://townpass-backend-567713067473.asia-east1.run.app/api/health

# Test ride start endpoint (will fail until DB is connected)
curl -X POST https://townpass-backend-567713067473.asia-east1.run.app/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{"station_id": "test","station_name": "Test Station","start_lat": 25.0,"start_lng": 121.5}'
```

## Additional Resources

- MongoDB Atlas Documentation: https://docs.atlas.mongodb.com/
- GCP Cloud Run Networking: https://cloud.google.com/run/docs/configuring/connecting-vpc
- PyMongo SSL/TLS Configuration: https://pymongo.readthedocs.io/en/stable/examples/tls.html

## Contact MongoDB Support

If the issue persists after trying all solutions, contact MongoDB Atlas support with:
- Error message: `[SSL: TLSV1_ALERT_INTERNAL_ERROR]`
- Source: GCP Cloud Run (asia-east1)
- Client: Python 3.11 with PyMongo
- Connection method: mongodb+srv:// (or standard depending on what you tried)
