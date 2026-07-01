// Landing Page Configuration
// Edit these values to change the text on your landing page

export const landingConfig = {
  // App Info
  appName: "Starter App",
  appTagline: "Your next project starts here",
  
  // Hero Section
  heroTitle: "launch your next project in minutes",
  heroSubtitle: "A modern, production-ready starter template",
  heroDescription: "Get started with authentication, database integration, and beautiful UI components. Everything you need to build your next web application.",
  
  // Call-to-Action Buttons
  primaryButtonText: "Get Started Free",
  secondaryButtonText: "View Features",
  signInButtonText: "Sign In",
  
  // Stats
  stats: [
    { value: "10+", label: "components" },
    { value: "5 min", label: "setup time" },
    { value: "100%", label: "customizable" },
    { value: "Free", label: "to start" }
  ],
  
  // Features Section
  featuresTitle: "everything you need to build",
  featuresSubtitle: "Start with a solid foundation and customize to your needs.",
  features: [
    {
      title: "authentication",
      description: "Pre-built auth with email, password, and OAuth support via Supabase.",
      icon: "🔐"
    },
    {
      title: "database ready",
      description: "Supabase integration out of the box with example queries and schemas.",
      icon: "⚡"
    },
    {
      title: "beautiful ui",
      description: "Shadcn components with custom glassmorphism styling throughout.",
      icon: "🎨"
    },
    {
      title: "responsive design",
      description: "Works perfectly on all devices from mobile to desktop.",
      icon: "📱"
    }
  ],
  
  // How It Works Section
  howItWorksTitle: "get started in 3 simple steps",
  steps: [
    {
      number: "01",
      title: "clone the repository",
      description: "Get the codebase with a single command. All dependencies included."
    },
    {
      number: "02",
      title: "configure your environment",
      description: "Add your Supabase keys to the .env.local file."
    },
    {
      number: "03",
      title: "start building",
      description: "Run npm dev and customize the template to your needs."
    }
  ],
  
  // What's Included Section
  includedTitle: "everything in one package",
  included: [
    {
      number: "001",
      title: "authentication system",
      description: "Complete sign-up, sign-in, and account management with Supabase Auth."
    },
    {
      number: "002",
      title: "responsive layouts",
      description: "Mobile-first design with beautiful layouts for all screen sizes."
    },
    {
      number: "003",
      title: "ui component library",
      description: "Pre-styled buttons, inputs, cards, and more with glassmorphism effects."
    },
    {
      number: "004",
      title: "database integration",
      description: "Supabase client configured with helper functions for common operations."
    }
  ],
  
  // CTA Section
  ctaTitle: "ready to build something amazing?",
  ctaDescription: "Get started with our template and launch your next project faster than ever. No credit card required.",
  ctaPrimaryButton: "Start Free",
  ctaSecondaryButton: "View Documentation",
  
  // Footer
  footerText: "© 2025 Starter App. All rights reserved.",
  footerLinks: [
    { text: "Documentation", href: "#" },
    { text: "GitHub", href: "#" },
    { text: "Support", href: "#" }
  ],
  
  // Tech Stack
  techStack: [
    { name: "Next.js", icon: "▲" },
    { name: "Supabase", icon: "⚡" },
    { name: "Tailwind", icon: "🎨" },
    { name: "Shadcn UI", icon: "🧩" }
  ]
}
