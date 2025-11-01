# Google Authentication Setup Guide

## Prerequisites
Before you can use Google authentication, you need to obtain OAuth 2.0 credentials from Google Cloud Console.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API or Google Identity Services

## Step 2: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Select **Web application** as the application type
4. Configure the OAuth consent screen if prompted
5. Add authorized redirect URIs:
   - For local development: `http://localhost:5000/login/google/callback`
   - For production: `https://yourdomain.com/login/google/callback`
6. Click **Create**
7. Copy the **Client ID** and **Client Secret**

## Step 3: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
```

Or set them as environment variables:

**Windows (Command Prompt):**
```cmd
set GOOGLE_CLIENT_ID=your-client-id-here
set GOOGLE_CLIENT_SECRET=your-client-secret-here
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_CLIENT_ID="your-client-id-here"
$env:GOOGLE_CLIENT_SECRET="your-client-secret-here"
```

**Linux/Mac:**
```bash
export GOOGLE_CLIENT_ID=your-client-id-here
export GOOGLE_CLIENT_SECRET=your-client-secret-here
```

## Step 4: Install Required Packages

```bash
pip install authlib requests
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 5: Run the Application

```bash
python app.py
```

Navigate to `http://localhost:5000/login` and you should see the "Continue with Google" button.

## Security Notes

1. **Never commit credentials to Git**: Add `.env` to `.gitignore`
2. **Use environment variables**: Don't hardcode credentials in code
3. **HTTPS in production**: Always use HTTPS for OAuth callbacks in production
4. **Secure secret key**: Change the Flask secret key in production

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Make sure the redirect URI in Google Cloud Console matches exactly with your callback URL
- Include the protocol (http/https), port number, and exact path

### Error: "invalid_client"
- Verify your Client ID and Client Secret are correct
- Check that environment variables are properly set

### Error: "access_denied"
- User cancelled the Google sign-in
- Check OAuth consent screen configuration

## Testing Without Google Auth

You can still use the regular username/password authentication:
- Username: `admin`
- Password: `admin123`

Or create a new account using the signup page.
