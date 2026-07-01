# My App Boilerplate

A Next.js boilerplate designed for non-coders to build modern web applications using AI tools like Cursor. This template includes everything you need to create beautiful, functional web apps without writing code from scratch.

## 🚀 Features

- **Modern Design**: Clean, responsive interface with black, white, gray, and neon orange theme
- **Easy Authentication**: Email/password and Google OAuth login built-in
- **User Management**: Complete account system with settings and preferences
- **Beginner-Friendly**: Extensive documentation and easy-to-edit configuration files
- **AI-Ready**: Perfect for building with AI coding assistants
- **Customizable**: Change colors, text, and features through simple config files

## 🛠️ Tech Stack

- **Framework**: Next.js 15.3 (App Router)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **UI Components**: Shadcn UI
- **Styling**: Tailwind CSS
- **Language**: JavaScript

## 📁 Project Structure

```
my-app-boilerplate/
├── public/                    # Static assets (images, favicon)
├── src/
│   ├── app/                   # Next.js App Router pages
│   │   ├── page.js           # Landing page (/)
│   │   ├── auth/page.js      # Login/signup page (/auth)
│   │   └── app/page.js       # Protected app page (/app)
│   ├── components/           # Reusable components
│   │   ├── ui/              # Shadcn UI components
│   │   ├── landing/         # Landing page components
│   │   ├── Navbar.js        # Navigation bar
│   │   ├── AuthForm.js      # Login/signup form
│   │   └── AccountSettings.js # User settings
│   ├── lib/
│   │   ├── supabase.js      # Supabase client setup
│   │   └── utils.js         # Utility functions
│   └── config/
│       └── landing.js       # Landing page text content
├── .env.local               # Environment variables (create this)
├── .env.example            # Template for environment variables
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have these installed:
- [Node.js](https://nodejs.org/) (version 18 or higher)
- npm (comes with Node.js)

### 2. Get the Code

**Option A: Download ZIP** (MY RECOMMENDED OPTION... EASY)
1. Download the ZIP file
2. Extract it to your desired location
3. Open the folder in your code editor (like Cursor)

**Option B: Clone Repository**
```bash
git clone [repository-url]
cd my-app-boilerplate
```

### 3. Install Dependencies

Open terminal in your project folder and run:
```bash
npm install
```

### 4. Set Up Supabase

#### Create a Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up for a free account
3. Click "New Project"
4. Fill in your project details
5. Wait for the project to be created (takes ~2 minutes)

#### Get Your Keys
1. In your Supabase dashboard, go to Settings → API
2. Copy your Project URL and anon public key
3. Create a file called `.env.local` in your project root
4. Add your keys:

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url-here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

#### Set Up the Database
1. In Supabase, go to the SQL Editor
2. Create a new query and run this code:

```sql
-- Create users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL UNIQUE,
  username TEXT,
  theme TEXT DEFAULT 'light',
  notifications BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy so users can only access their own data
CREATE POLICY user_access ON users FOR ALL
  USING (auth.uid() = id);
```

#### Enable Google OAuth (Optional)
1. In Supabase, go to Authentication → Providers
2. Enable Google provider
3. Add your Google OAuth credentials (get these from Google Cloud Console)

### 5. Run Your App

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser. You should see your landing page!

## 🎨 Customization Guide

### Change Landing Page Text

Edit `src/config/landing.js` to change all text on your homepage:

```javascript
export const landingConfig = {
  heroTitle: "Your New Title Here",
  heroSubtitle: "Your subtitle here",
  // ... change any text you want
}
```

### Change Colors

Edit `src/app/globals.css` to change the color scheme:

```css
:root {
  --primary: 14 100% 50%; /* This is the neon orange - change to any color */
  /* Change other colors here */
}
```

### Add App Features

Your main app goes in `src/app/app/page.js`. Replace the placeholder content with your own components:

```javascript
// Replace the placeholder card with your app features
<Card>
  <CardContent>
    <h2>My Custom App Feature</h2>
    <p>Add your app functionality here!</p>
  </CardContent>
</Card>
```

### Add New Settings

Edit `src/components/AccountSettings.js` to add new user settings:

```javascript
// Add new settings in the settings card
<div className="flex items-center justify-between">
  <div>
    <label className="text-sm font-medium">New Setting</label>
    <p className="text-sm text-gray-500">Description of setting</p>
  </div>
  <Switch
    checked={newSetting}
    onCheckedChange={setNewSetting}
  />
</div>
```

### Add Shadcn UI Components

To add new UI components:

```bash
npx shadcn-ui@latest add [component-name]
```

For example:
```bash
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add avatar
```

### Change App Name and Logo

1. **App Name**: Edit `src/config/landing.js` and change `appName`
2. **Logo**: Replace files in the `public/` folder
3. **Favicon**: Replace `public/favicon.ico` with your own

## 🔧 Development Commands

```bash
npm run dev    # Start development server
npm run build  # Build for production
npm run start  # Start production server
npm run lint   # Check for code issues
```

## 📱 Pages Overview

- **`/`** - Landing page with hero section and features
- **`/auth`** - Login and signup page
- **`/app`** - Protected app page (requires login)
  - **App Tab** - Your main app content (blank by default)
  - **Account Tab** - User settings and profile management

## 🚨 Troubleshooting

### Port 3000 is in use
```bash
# Kill the process using port 3000
npx kill-port 3000
# Or run on different port
npm run dev -- -p 3001
```

### Supabase Connection Issues
- Double-check your `.env.local` file has the correct keys
- Make sure there are no extra spaces in your environment variables
- Verify your Supabase project is active (not paused)

### Build Errors
- Make sure all dependencies are installed: `npm install`
- Check that you have the latest Node.js version
- Clear Next.js cache: `rm -rf .next`

## 🌐 Deployment

### Deploy to Vercel (Recommended)
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Add your environment variables in Vercel dashboard
5. Deploy!

### Deploy to Netlify
1. Build your app: `npm run build`
2. Upload the `out` folder to Netlify
3. Add environment variables in Netlify dashboard

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Shadcn UI Components](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Support

If you're having trouble:
1. Check this README for common solutions
2. Look at the code comments for guidance
3. Check the official documentation links above

## 📝 License

This project is open source and available under the MIT License.

---

**Happy Building! 🚀**

Remember: This boilerplate is designed to be your starting point. Customize it, break it, rebuild it, and make it your own! 
