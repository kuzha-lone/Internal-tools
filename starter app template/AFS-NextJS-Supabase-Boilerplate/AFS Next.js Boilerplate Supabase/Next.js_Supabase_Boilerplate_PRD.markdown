# Product Requirements Document (PRD)

## Next.js Boilerplate with Supabase for Non-Coder App Development

**Date**: June 23, 2025  
**Author**: [GrowthTech Labs]  
**Project**: Boilerplate for digital product teaching non-coders to build web apps  
**Version**: 2.0

---

## 1. Overview

### 1.1 Purpose
This PRD defines a Next.js boilerplate for helping non-coders to build web apps with Cursor or other AI tools. The boilerplate is a customizable, beginner-friendly template with a fully designed landing page, a login/signup page, a blank one-page app, and a designed account page with settings including the sign out button, all integrated with Supabase for authentication and data storage. It uses Shadcn UI for modern, editable components and prioritizes ease of setup, especially for Supabase auth, to enable students to start building apps quickly. Super clean, modern, sleek, nice-looking design. Black, white, gray, and neon orange trimming for the colors of the boilerplate.

### 1.2 Objectives
- Provide a simple Next.js template for non-coders to build web apps.
- Deliver a fully designed, editable landing page and account page with settings.
- Keep the app page blank as a starting point for user projects.
- Ensure seamless Supabase integration for auth (email/password, Google OAuth) and database, pre-connected for ease.
- Use Shadcn UI for consistent, accessible and modern styling.
- Include clear documentation and code comments for customization.
- Enable easy distribution to course users (ZIP file).

### 1.3 Target Audience
- Non-coders with no programming experience.
- Beginners learning to build apps with AI tools like Cursor.

### 1.4 Success Metrics
- Users can run the boilerplate locally (`npm run dev`) in < 5 minutes.
- Non-coders can edit landing page text/components and account settings per instructions.
- All features (landing page, blank app, account/settings, Supabase auth, Shadcn UI) work without errors.
- Positive feedback on setup ease and documentation clarity.

---

## 2. Scope

### 2.1 In Scope
- **Next.js Framework**: Next.js 15.3 (App Router) for routing and SSR - always most recent version
- **Supabase Backend**:
  - Authentication (email/password, Google OAuth).
  - Database (store user settings, e.g., username, theme).
  - Pre-connected setup with clear configuration steps.
- **Landing Page**: Fully designed, editable template with hero, features, and footer.
- **One-Page App**: Blank, protected page (`/app`) as a placeholder (should say "your app goes here").
- **Account Page**: Designed within `/app`, with user info and settings (theme toggle, username update).
- **Authentication/Login**:
  - Supabase Auth for email/password and Google OAuth.
  - Protected routes (`/app` requires login).
- **Shadcn UI**:
  - Styled components (Button, Card, Form, Input, Switch, Tabs, Nav).
  - Editable styles for landing and account pages.
- **Documentation**:
  - README.md with setup, Supabase config, and customization steps.
  - CHANGELOG.md so users can document code changes along the way
  - Inline code comments for non-coders.
- **Distribution**: GitHub repo, ZIP file, course platform delivery.

### 2.2 Out of Scope
- AI API integration or AI-related features.
- Complex app features (e.g., chat, forms) on `/app`.
- Multi-page app beyond landing, auth, and app pages.
- Non-web platforms.
- Internationalization (i18n).
- Automated testing.

---

## 3. Features and Requirements

### 3.1 Supabase Backend
**Description**: Pre-connected Supabase for authentication and user settings storage.  
**Requirements**:
- **Authentication**:
  - Email/password signup/login.
  - Google OAuth login.
  - Use `@supabase/supabase-js` SDK.
- **Database**:
  - Table: `users` (columns: `id`, `email`, `username`, `theme`, `created_at`).
  - Store username and theme preference.
  - Use Supabase PostgreSQL.
- **Setup**:
  - Initialize Supabase client in `src/lib/supabase.js`.
  - Use `.env.local` for Supabase URL and anon key.
  - Include `.env.example` with placeholder values.
- **Security**:
  - Enable Row-Level Security (RLS) on `users` table (users access own data).
  - Secure keys in `.env.local`.
- **Ease of Connection**:
  - README with step-by-step Supabase project setup (create project, get keys, enable OAuth).
  - Pre-configured client with comments for key replacement.
- **Non-Coder Customization**:
  - Comments in `src/lib/supabase.js` to change table names.
  - README: “Sign up at supabase.com, paste keys in `.env.local`.”

### 3.2 Landing Page (`/`)
**Description**: Fully designed, editable template to introduce the app.  
**Requirements**:
- **Hero Section**:
  - Title: “Start Building Your App”.
  - Subtitle: “Create modern web apps without coding!”.
  - CTA buttons: “Sign Up” and “Log In” (link to `/auth`).
  - Background: Gradient or placeholder image (`/public/hero-bg.jpg`).
- **Features Section**:
  - Three editable cards: “Customizable Design”, “Easy Auth”, “Beginner-Friendly”.
  - Use Shadcn Card components.
- **Footer**:
  - Text: “© 2025 My App Boilerplate”.
  - Links: “Privacy Policy”, “Terms of Service” (placeholders).
- **Styling**:
  - Shadcn Button, Card components.
  - Responsive (mobile-friendly).
  - Tailwind CSS with Shadcn UI (light/dark theme support).
- **Navigation**:
  - Navbar with logo (`/public/logo.png`) and “Log In”/“Sign Up” buttons.
- **Editability**:
  - Components in `src/components/landing/` (e.g., `Hero.js`, `FeatureCard.js`).
  - Text strings in `src/config/landing.js` (e.g., `{ "heroTitle": "Start Building..." }`).
  - Comments to change text, colors, or images.
  - README: “Edit `src/config/landing.js` to change hero title.”
- **Non-Coder Customization**:
  - Change text in `src/config/landing.js`.
  - Update colors in `src/app/globals.css`.
  - Swap images in `/public`.

### 3.3 One-Page App (`/app`)
**Description**: Blank, protected page as a placeholder for user projects.  
**Requirements**:
- **Content**:
  - Simple placeholder: “Build your app here!” (Shadcn Card).
  - beautiful, modern profile button in the top right-hand corner linking to Account page. Make sure its responsive and adjusts to all screen sizes
- **Navigation**:
  - Sidebar or tabs for “App” (default) and “Account” (use Shadcn Nav or Tabs).
- **Protection**:
  - Redirect to `/auth` if not logged in (Supabase Auth).
- **Styling**:
  - Minimal, matches landing page theme.
  - Responsive. Adjusts to all screen sizes. Use vw and vh for all size measurements.
- **Non-Coder Customization**:
  - README: “Edit `src/app/app/page.js` to add your app features.”

### 3.4 Account Page (within `/app`)
**Description**: Fully designed sub-view for user info and settings.  
**Requirements**:
- **User Info**:
  - Display: Email, username, signup date (from Supabase Auth).
  - Editable username field (updates Supabase `users` table).
  - Use Shadcn Card and Form.
- **Settings**:
  - Theme toggle (light/dark, saved in Supabase `users` table).
  - Notification preference toggle (placeholder, saved in `users`).
  - Logout button (Supabase Auth, redirect to `/`).
  - Use Shadcn Switch, Form, Button.
- **Design**:
  - Clean layout: User info card above settings form.
  - Responsive (stack on mobile).
  - Shadcn components for consistency.
- **Navigation**:
  - Accessible via sidebar/tabs in `/app`.
- **Non-Coder Customization**:
  - Comments to add settings fields.
  - README: “Edit `src/components/AccountSettings.js` to add settings.”

### 3.5 Authentication/Login (`/auth`)
**Description**: Page for signup, login, or OAuth via Supabase.  
**Requirements**:
- **Methods**:
  - Email/password signup/login.
  - Google OAuth.
- **UI**:
  - Tabs for “Sign Up” and “Log In” (Shadcn Tabs).
  - Error messages (e.g., “Invalid password”).
  - “Forgot Password” link (Supabase reset flow).
- **Redirects**:
  - Post-login/signup: Redirect to `/app`.
  - If logged in: Redirect from `/auth` to `/app`.
- **Styling**:
  - Shadcn Form, Input, Button, Tabs.
  - Match app theme.
- **Ease of Connection**:
  - Pre-configured Supabase Auth in `src/lib/supabase.js`.
  - README with Google OAuth setup steps.
- **Non-Coder Customization**:
  - Comments to change form labels.
  - README: “Edit `src/app/auth/page.js` to update form text.”

### 3.6 Shadcn UI
**Description**: Use Shadcn UI for all components.  
**Requirements**:
- **Installation**:
  - Run `npx shadcn-ui@latest init`.
  - Configure with Tailwind CSS.
- **Components**:
  - Button, Card, Form, Input, Switch, Tabs, Nav.
  - Used in landing, auth, and account pages.
- **Theme**:
  - Light/dark mode (tied to Account settings).
  - Shadcn default theme with Tailwind.
- **Accessibility**:
  - WCAG 2.1 compliance.
  - ARIA labels for inputs.
- **Editability**:
  - Comments to change styles.
  - README: “Run `npx shadcn-ui@latest add button` for new components.”

### 3.7 Documentation
**Description**: Guide non-coders to set up and customize.  
**Requirements**:
- **README.md**:
  - **Setup**:
    - Install Node.js, npm.
    - Clone repo, run `npm install`, `npm run dev`.
    - Create Supabase project, add keys to `.env.local`.
    - Enable Google OAuth in Supabase.
  - **Customization**:
    - Edit landing page: `src/config/landing.js`.
    - Change colors: `src/app/globals.css`.
    - Add app features: `src/app/app/page.js`.
    - Add settings: `src/components/AccountSettings.js`.
    - Add Shadcn components: `npx shadcn-ui@latest add [component]`.
  - **Troubleshooting**:
    - Issues like “Port 3000 in use”.
    - Links to Supabase, Next.js, Shadcn docs.
- **Code Comments**:
  - Explain purpose (e.g., “This is the landing page hero”).
  - Highlight customization (e.g., “Change text here”).
- **Format**:
  - Markdown with screenshots/GIFs.

---

## 4. Technical Specifications

### 4.1 Tech Stack
- **Framework**: Next.js 15.3 (App Router).
- **Language**: JavaScript (ES6+).
- **Styling**: Tailwind CSS + Shadcn UI.
- **Backend**: Supabase (Auth, PostgreSQL).
- **Environment**: Node.js 18+.
- **Build Tool**: npm.

### 4.2 Dependencies
```json
{
  "dependencies": {
    "next": "15.3.x",
    "react": "19.1.x",
    "react-dom": "19.1.x",
    "@supabase/supabase-js": "latest",
    "tailwindcss": "4.x.x",
    "autoprefixer": "latest",
    "postcss": "latest",
    "@shadcn/ui": "latest"
  },
  "devDependencies": {
    "eslint": "latest",
    "eslint-config-next": "14.x.x"
  }
}
```

### 4.3 Folder Structure
```
my-app-boilerplate/
├── public/                    # Static assets
│   ├── favicon.ico
│   ├── logo.png
│   └── hero-bg.jpg
├── src/                       # Source code
│   ├── app/                   # Next.js App Router
│   │   ├── globals.css        # Tailwind and Shadcn styles
│   │   ├── layout.js          # Root layout (navbar, footer)
│   │   ├── page.js            # Landing page (/)
│   │   ├── auth/              # Auth page
│   │   │   └── page.js        # Login/signup (/auth)
│   │   ├── app/               # Protected app page
│   │   │   └── page.js        # Blank app and account (/app)
│   ├── components/            # Shadcn and custom components
│   │   ├── landing/           # Landing page components
│   │   │   ├── Hero.js
│   │   │   └── FeatureCard.js
│   │   ├── AccountSettings.js # Account info and settings
│   │   ├── Navbar.js          # Navigation bar
│   │   └── AuthForm.js        # Login/signup form
│   ├── lib/                   # Utilities
│   │   └── supabase.js        # Supabase client config
│   ├── config/                # Editable configs
│   │   └── landing.js         # Landing page text strings
├── .env.local                 # Environment variables
├── .env.example               # Template for env vars
├── next.config.js             # Next.js config
├── tailwind.config.js         # Tailwind config
├── package.json               # Dependencies
└── README.md                  # Documentation
```

### 4.4 Environment Variables
```
# .env.local
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 4.5 Database Schema
```sql
-- Table: users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL UNIQUE,
  username TEXT,
  theme TEXT DEFAULT 'light',
  notifications BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_access ON users FOR ALL
  USING (auth.uid() = id);
```

---

## 5. Non-Functional Requirements
- **Performance**: Page load < 2 seconds.
- **Accessibility**: WCAG 2.1 via Shadcn UI.
- **Security**:
  - Secure Supabase keys in `.env.local`.
  - RLS on Supabase tables.
  - Sanitize inputs to prevent XSS.
- **Compatibility**: Chrome, Firefox, Safari, Edge (latest).
- **Scalability**: Handle 100 concurrent users locally.

---

## 6. Customization Points for Non-Coders
- **Landing Page**:
  - Edit text in `src/config/landing.js`.
  - Change colors in `src/app/globals.css`.
  - Swap images in `/public`.
- **App Page**:
  - Add features in `src/app/app/page.js`.
- **Account/Settings**:
  - Add fields in `src/components/AccountSettings.js`.
- **Auth**:
  - Change form labels in `src/components/AuthForm.js`.
- **Shadcn UI**:
  - Add components with `npx shadcn-ui@latest add [component]`.

---

## 7. Distribution Plan
**Description**: Deliver the boilerplate to course users.  
**Requirements**:
- **Packaging**:
  - GitHub repo (`my-app-boilerplate`).
  - Include all files (code, README, `.env.example`).
  - ZIP file as GitHub release.
- **Hosting**:
  - GitHub repo (public or private).
  - Optional: Vercel demo (live app showcase).
- **Delivery**:
  - **Course Platform**: Share GitHub link or ZIP via LMS (e.g., Teachable).
  - **Email**: Send ZIP/link to students.
  - **Docs Site**: README on GitHub Pages (optional).
- **Instructions**:
  - README: Clone repo, download ZIP, or use demo.
  - Setup video link (placeholder).
- **Access**:
  - Public repo or private with invites.
  - ZIP for non-GitHub users.

---

## 8. Potential Gaps and Suggestions
### 8.1 Gaps
- **Supabase Setup**: Non-coders may struggle with project creation.
- **Distribution**: Course platform details unclear.
- **Onboarding**: No in-app guide.

### 8.2 Suggestions
- **Supabase Guide**: Detailed README with screenshots.
- **Onboarding Modal**: Optional Shadcn Dialog: “Welcome! Check Settings to update your profile.”
- **Config File**: `src/config/app.js` for global settings (e.g., `{ "primaryColor": "#3b82f6" }`).
- **Vercel Deployment**: README step for optional deployment.

---

## 9. Implementation Notes for AI Coding Partner
- **Simplicity**: Modular code, avoid advanced features.
- **Comments**: Verbose comments (e.g., “This sets up Supabase”).
- **Supabase**:
  - Docs: https://supabase.com/docs.
  - Create project, enable Google OAuth, set up `users` table.
- **Shadcn**:
  - Run `npx shadcn-ui@latest init`, add components.
  - Docs: https://ui.shadcn.com/.
- **Testing**:
  - Run `npm run dev`, test landing, auth, app, account.
  - Verify Supabase auth and settings updates.
- **README**:
  - 500+ words, step-by-step setup.
  - Include Supabase and Vercel steps, screenshots.

---

## 10. Risks and Mitigations
- **Risk**: Non-coders struggle with Supabase setup.  
  **Mitigation**: Detailed README with screenshots, Supabase docs link.
- **Risk**: Distribution access issues.  
  **Mitigation**: Offer ZIP file, test delivery.
- **Risk**: Shadcn/Tailwind conflicts.  
  **Mitigation**: Follow Shadcn CLI, test thoroughly.

---

## 11. Timeline
- **Development**: 2-3 days.
- **Testing**: 1 day.
- **Documentation**: 1 day.
- **Total**: ~5 days.

---

## 12. References
- Next.js: https://nextjs.org/docs
- Supabase: https://supabase.com/docs
- Shadcn UI: https://ui.shadcn.com/
- Tailwind CSS: https://tailwindcss.com/docs/installation/framework-guides/nextjs


---
