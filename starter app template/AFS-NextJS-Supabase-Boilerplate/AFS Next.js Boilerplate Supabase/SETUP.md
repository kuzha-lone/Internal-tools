# Setup Guide

**Don't know how to code?** Give this entire file to Claude Code or Cursor and tell it "help me set this up". It will guide you through everything.

---

## What You're Setting Up

This is a web application starter template with:
- User login via Google
- User profile settings (saved to a database)
- A beautiful glassmorphism design
- Ready for you to build on top of

You'll need to set up two services (both free):
1. **Supabase** - Your database (where user data is stored)
2. **Google Cloud** - For "Sign in with Google" functionality

Total time: ~15-20 minutes

---

## Step 1: Install Dependencies

### What is this?
Your app needs some code packages to run. This step downloads them.

### How to do it:

1. Open your terminal:
   - **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
   - **Windows**: Press `Windows key`, type "Command Prompt" or "PowerShell", press Enter

2. Navigate to your project folder. Type this command and press Enter:
   ```bash
   cd "path/to/your/project/folder"
   ```
   Replace `path/to/your/project/folder` with the actual path. For example:
   ```bash
   cd "/Users/john/Projects/my-app"
   ```

3. Install the packages by typing this and pressing Enter:
   ```bash
   npm install
   ```

4. Wait for it to finish (usually 30-60 seconds). You'll see a bunch of text scrolling. When it's done, you'll see your cursor ready for a new command.

---

## Step 2: Create a Supabase Account and Project

### What is Supabase?
Supabase is a database service. It stores your users' information (their email, name, settings, etc.). It's free for small projects.

### How to do it:

1. Open your web browser and go to: **https://supabase.com**

2. Click the green **"Start your project"** button (top right)

3. Sign up using your GitHub account or email
   - If using email: Enter your email, create a password, click "Sign Up"
   - Check your email and click the confirmation link

4. Once logged in, click **"New Project"**

5. Fill in the form:
   - **Name**: Give your project a name (e.g., "my-starter-app")
   - **Database Password**: Create a strong password and **SAVE THIS PASSWORD SOMEWHERE SAFE** - you'll need it later!
   - **Region**: Pick the one closest to you
   - Click **"Create new project"**

6. Wait 1-2 minutes for Supabase to set up your project. You'll see a loading screen.

---

## Step 3: Get Your Supabase Keys

### What are these keys?
These are like passwords that let your app connect to your database. You need three things:
- Project URL
- Anon Key
- Database URL

### How to get the Project URL and Anon Key:

1. In your Supabase dashboard, look at the left sidebar

2. Click **"Settings"** (the gear icon at the bottom)

3. Click **"API"** in the settings menu

4. You'll see a section called **"Project URL"**
   - Copy the URL (looks like `https://abcdefgh.supabase.co`)
   - Paste it somewhere (like a notes app) - you'll need it soon

5. Below that, you'll see **"Project API keys"**
   - Find the one labeled **"anon public"**
   - Click the copy button next to it
   - Paste it in your notes

### How to get the Database URL:

1. Still in Settings, click **"Database"** in the left menu

2. Scroll down to find **"Connection string"**

3. Click the **"URI"** tab

4. You'll see a long URL that starts with `postgresql://postgres:`
   - Click the copy button
   - Paste it in your notes
   - **Important**: This URL contains `[YOUR-PASSWORD]` - you need to replace that with the database password you created in Step 2

   Example:
   - Before: `postgresql://postgres:[YOUR-PASSWORD]@db.abcdefgh.supabase.co:5432/postgres`
   - After: `postgresql://postgres:MyActualPassword123@db.abcdefgh.supabase.co:5432/postgres`

---

## Step 4: Create the Database Tables

### What is this?
Your app needs a place to store user profile information (like their display name and preferences). This step creates that storage space.

### How to do it:

1. In your Supabase dashboard, click **"SQL Editor"** in the left sidebar (looks like a document icon)

2. Click **"New query"** (top right)

3. Copy and paste this entire block of code into the editor:

```sql
-- Create profiles table for user settings
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY,
  username TEXT,
  theme TEXT DEFAULT 'light',
  notifications BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Allow anyone to read/write their own profile
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own profile"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update their own profile"
  ON profiles FOR UPDATE
  USING (true);
```

4. Click the green **"Run"** button (or press Ctrl+Enter / Cmd+Enter)

5. You should see "Success. No rows returned" - this means it worked!

---

## Step 5: Set Up Google Login

### What is this?
This lets users sign into your app using their Google account. You need to register your app with Google first.

### How to do it:

1. Open a new browser tab and go to: **https://console.cloud.google.com**

2. Sign in with your Google account

3. At the top of the page, you'll see a project dropdown. Click it and then click **"New Project"**

4. Give your project a name (e.g., "My Starter App") and click **"Create"**

5. Wait a few seconds, then make sure your new project is selected in the dropdown at the top

6. In the search bar at the top, type **"OAuth consent screen"** and click on it

7. Choose **"External"** and click **"Create"**

8. Fill in the form:
   - **App name**: Your app's name (e.g., "My Starter App")
   - **User support email**: Select your email
   - **Developer contact email**: Enter your email
   - Leave everything else blank
   - Click **"Save and Continue"**

9. On the "Scopes" page, just click **"Save and Continue"** (no changes needed)

10. On the "Test users" page, click **"Add Users"**, enter your email, click **"Add"**, then **"Save and Continue"**

11. Click **"Back to Dashboard"**

12. Now, in the left sidebar, click **"Credentials"**

13. Click **"+ Create Credentials"** at the top, then select **"OAuth client ID"**

14. For "Application type", choose **"Web application"**

15. Give it a name (e.g., "Web Client")

16. Under **"Authorized JavaScript origins"**, click **"+ Add URI"** and enter:
    ```
    http://localhost:3000
    ```

17. Under **"Authorized redirect URIs"**, click **"+ Add URI"** and enter:
    ```
    http://localhost:3000/api/auth/callback/google
    ```

18. Click **"Create"**

19. A popup will show your credentials:
    - **Client ID**: Copy this and save it in your notes
    - **Client Secret**: Copy this and save it in your notes
    - Click **"OK"**

---

## Step 6: Configure Your App

### What is this?
Now you'll put all those keys and passwords into your app so it knows how to connect to everything.

### How to do it:

1. In your project folder, find the file called `.env.local.example`

2. Make a copy of this file and name it `.env.local`
   - **Mac**: In terminal, run: `cp .env.local.example .env.local`
   - **Windows**: In Command Prompt, run: `copy .env.local.example .env.local`
   - Or just duplicate the file manually and rename it

3. Open `.env.local` in any text editor (like Notepad, TextEdit, or VS Code)

4. Replace each placeholder with your actual values from your notes:

```
# Supabase (from Step 3)
NEXT_PUBLIC_SUPABASE_URL=https://your-actual-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-actual-anon-key-here

# Database URL (from Step 3 - make sure you replaced [YOUR-PASSWORD])
DATABASE_URL=postgresql://postgres:your-actual-password@db.your-project-id.supabase.co:5432/postgres

# Better Auth Secret (make up any random string - at least 20 characters)
BETTER_AUTH_SECRET=make-up-any-random-string-like-this-one-here-12345

# Google OAuth (from Step 5)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# App URL (keep this as-is for local development)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

5. Save the file

---

## Step 7: Run Your App

### How to do it:

1. Open your terminal (if it's not still open from Step 1)

2. Make sure you're in your project folder (use the `cd` command from Step 1 if needed)

3. Type this command and press Enter:
   ```bash
   npm run dev
   ```

4. Wait a few seconds. You'll see some text, and eventually something like:
   ```
   ▲ Next.js 16.1.4
   - Local: http://localhost:3000
   ```

5. Open your web browser and go to: **http://localhost:3000**

6. You should see your app's landing page!

7. Click "Get Started" or go to http://localhost:3000/auth to sign in with Google

---

## Step 8: Test Everything

1. Click **"Continue with Google"**

2. Sign in with the Google account you added as a test user in Step 5

3. You should be redirected to the dashboard at `/app`

4. Click the **"Account"** tab

5. Try changing your display name and click **"Save Changes"**

6. If it says "Settings saved!" - congratulations, everything works!

---

## Stopping and Starting the App

### To stop the app:
- Go to your terminal and press `Ctrl + C`

### To start it again later:
1. Open terminal
2. Navigate to your project folder: `cd "path/to/your/project"`
3. Run: `npm run dev`
4. Open http://localhost:3000 in your browser

---

## Troubleshooting

### "Google login doesn't work"
- Make sure you added yourself as a test user in Google Cloud Console (Step 5, #10)
- Double-check that your redirect URI is exactly: `http://localhost:3000/api/auth/callback/google`
- Make sure there are no extra spaces when you copied your Client ID and Secret

### "Database error" or "Failed to initialize database adapter"
- Check that you replaced `[YOUR-PASSWORD]` in your DATABASE_URL with your actual password
- Make sure there are no typos in your Supabase URL
- Try regenerating your database password in Supabase: Settings → Database → Reset database password

### "Settings won't save"
- Make sure you ran the SQL in Step 4
- Check that your Supabase URL and anon key are correct

### "npm command not found"
- You need to install Node.js first
- Go to https://nodejs.org and download the LTS version
- Install it, then restart your terminal and try again

### "The page won't load" or "localhost refused to connect"
- Make sure `npm run dev` is still running in your terminal
- Check that you're going to http://localhost:3000 (not https)

### "I messed something up and want to start over"
- Delete the `.env.local` file and redo Step 6
- If your database is messed up, you can delete the project in Supabase and create a new one

---

## Going Live (Deploying to the Internet)

Once your app works locally and you want to put it on the internet:

1. Create an account at **https://vercel.com** (free)
2. Connect your GitHub account
3. Push your code to GitHub
4. Import your project in Vercel
5. Add all your environment variables (same ones from `.env.local`) in Vercel's settings
6. Update your Google OAuth settings to include your new Vercel URL

This is a more advanced topic - consider asking Claude Code or Cursor for help with deployment when you're ready.

---

## Need Help?

Give this entire SETUP.md file to Claude Code or Cursor and describe your problem. Include any error messages you see. The AI will help you debug it.
