import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function LandingPage() {
  return (
    <div className="min-h-screen animated-gradient-bg">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass-nav">
        <div className="container mx-auto px-4 md:px-6">
          <div className="flex items-center justify-between h-16 md:h-20">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-lg">S</span>
              </div>
              <span className="text-xl font-bold tracking-tight text-gray-900">Starter App</span>
            </div>
            
            <nav className="hidden lg:flex items-center space-x-1">
              {['Features', 'Templates', 'Docs', 'Pricing'].map((item) => (
                <a
                  key={item}
                  href="#"
                  className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-white/60 rounded-lg transition-all duration-200"
                >
                  {item}
                </a>
              ))}
            </nav>
            
            <div className="flex items-center space-x-3">
              <Link href="/auth">
                <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
                  Sign In
                </Button>
              </Link>
              <Link href="/auth">
                <Button size="sm" className="rounded-lg">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-20 right-10 w-[400px] h-[400px] bg-gray-200/40 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-20 left-10 w-[500px] h-[500px] bg-gray-300/30 rounded-full blur-3xl animate-float animation-delay-300"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gray-100/50 rounded-full blur-3xl"></div>
          </div>
          
          {/* Floating Glass Elements */}
          <div className="absolute top-40 left-10 hidden lg:block animate-float animation-delay-200">
            <div className="glass-card p-4 rounded-2xl">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">fast setup</p>
                  <p className="text-xs text-gray-500">5 minutes</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="absolute top-60 right-20 hidden lg:block animate-float animation-delay-400">
            <div className="glass-card p-4 rounded-2xl">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">production ready</p>
                  <p className="text-xs text-gray-500">best practices</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="relative z-10 container mx-auto px-4 md:px-6">
            <div className="max-w-5xl mx-auto text-center">
              <div className="inline-flex items-center space-x-2 glass-card px-4 py-2 mb-8 animate-fade-in">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span className="text-sm text-gray-600">open source starter template</span>
              </div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold mb-6 leading-[1.1] tracking-tight text-gray-900 animate-slide-up">
                launch your next project
                <br />
                <span className="text-gray-400">in minutes</span>
              </h1>
              
              <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed animate-slide-up animation-delay-100">
                A modern, production-ready starter template with authentication, 
                database integration, and beautiful UI components.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-up animation-delay-200">
                <Link href="/auth">
                  <Button size="lg" className="w-full sm:w-auto px-8 py-4 text-base rounded-xl shadow-lg">
                    Get Started Free
                  </Button>
                </Link>
                <Link href="#features">
                  <Button size="lg" variant="glass" className="w-full sm:w-auto px-8 py-4 text-base rounded-xl">
                    View Features
                  </Button>
                </Link>
              </div>
              
              <div className="mt-12 flex items-center justify-center flex-wrap gap-6 text-sm text-gray-500 animate-fade-in animation-delay-300">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>10+ components</span>
                </div>
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>5 min setup</span>
                </div>
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>production ready</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack Section */}
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <p className="text-center text-sm text-gray-500 mb-8">built with modern technologies</p>
            <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12">
              {[
                { name: 'Next.js', icon: '▲' },
                { name: 'Supabase', icon: '⚡' },
                { name: 'Tailwind', icon: '🎨' },
                { name: 'Shadcn UI', icon: '🧩' }
              ].map((tech, i) => (
                <div key={i} className="glass-card px-6 py-3 rounded-xl flex items-center space-x-2 hover:shadow-glass-lg transition-all duration-300">
                  <span className="text-xl">{tech.icon}</span>
                  <span className="font-medium text-gray-700">{tech.name}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 md:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="text-center mb-16">
              <span className="inline-block px-4 py-2 glass-card rounded-full text-sm font-semibold mb-4 text-gray-700">
                features
              </span>
              <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gray-900">
                everything you need to build
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Start with a solid foundation and customize to your needs.
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                    </svg>
                  ),
                  title: 'authentication',
                  description: 'Pre-built auth with email, password, and OAuth support via Supabase.'
                },
                {
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                    </svg>
                  ),
                  title: 'database ready',
                  description: 'Supabase integration out of the box with example queries and schemas.'
                },
                {
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                    </svg>
                  ),
                  title: 'beautiful ui',
                  description: 'Shadcn components with custom glassmorphism styling throughout.'
                },
                {
                  icon: (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                  ),
                  title: 'responsive design',
                  description: 'Works perfectly on all devices from mobile to desktop.'
                }
              ].map((feature, i) => (
                <div key={i} className="glass-card-hover p-6 rounded-2xl group">
                  <div className="w-12 h-12 rounded-xl bg-black/5 group-hover:bg-black group-hover:text-white flex items-center justify-center mb-4 text-gray-700 transition-all duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-lg font-bold mb-2 text-gray-900">{feature.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-20 md:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
              <div>
                <span className="inline-block px-4 py-2 glass-card rounded-full text-sm font-semibold mb-4 text-gray-700">
                  get started
                </span>
                <h2 className="text-3xl md:text-4xl font-bold mb-6 leading-tight text-gray-900">
                  up and running in
                  <br />
                  <span className="text-gray-400">3 simple steps</span>
                </h2>
                <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                  No complicated setup or configuration required. Clone, configure, and start building your app immediately.
                </p>
                <Link href="/auth">
                  <Button className="rounded-xl">
                    Start Building
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Button>
                </Link>
              </div>
              
              <div className="space-y-4">
                {[
                  {
                    step: '01',
                    title: 'clone the repository',
                    description: 'Get the codebase with a single command. All dependencies included.'
                  },
                  {
                    step: '02',
                    title: 'configure your environment',
                    description: 'Add your Supabase keys to the .env.local file.'
                  },
                  {
                    step: '03',
                    title: 'start building',
                    description: 'Run npm dev and customize the template to your needs.'
                  }
                ].map((item, i) => (
                  <div key={i} className="glass-card-hover p-6 rounded-2xl flex items-start space-x-4 group">
                    <div className="w-12 h-12 rounded-xl bg-black text-white flex items-center justify-center font-bold flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                      {item.step}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold mb-1 text-gray-900">{item.title}</h3>
                      <p className="text-gray-600 text-sm">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* What's Included Section */}
        <section className="py-20 md:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <span className="inline-block px-4 py-2 glass-card rounded-full text-sm font-semibold mb-4 text-gray-700">
                  what's included
                </span>
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
                  everything in one package
                </h2>
              </div>
              
              <div className="space-y-4">
                {[
                  {
                    number: '001',
                    title: 'authentication system',
                    description: 'Complete sign-up, sign-in, and account management with Supabase Auth.'
                  },
                  {
                    number: '002',
                    title: 'responsive layouts',
                    description: 'Mobile-first design with beautiful layouts for all screen sizes.'
                  },
                  {
                    number: '003',
                    title: 'ui component library',
                    description: 'Pre-styled buttons, inputs, cards, and more with glassmorphism effects.'
                  },
                  {
                    number: '004',
                    title: 'database integration',
                    description: 'Supabase client configured with helper functions for common operations.'
                  }
                ].map((feature, i) => (
                  <div key={i} className="group glass-card-hover p-6 rounded-2xl flex items-center justify-between">
                    <div className="flex items-center gap-6">
                      <span className="text-2xl font-bold text-gray-300 group-hover:text-gray-900 transition-colors duration-200">
                        {feature.number}
                      </span>
                      <div>
                        <h3 className="text-lg font-bold mb-1 text-gray-900">{feature.title}</h3>
                        <p className="text-gray-500 text-sm">{feature.description}</p>
                      </div>
                    </div>
                    <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 group-hover:bg-black group-hover:text-white transition-all duration-300">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 md:py-32 gradient-dark relative overflow-hidden">
          <div className="absolute inset-0">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-white/5 rounded-full blur-[100px]"></div>
          </div>
          
          <div className="relative z-10 container mx-auto px-4 md:px-6 text-center">
            <span className="inline-block px-4 py-2 glass-dark rounded-full text-sm font-semibold mb-6 text-white/80">
              start today
            </span>
            <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white leading-tight">
              ready to build something
              <br />
              <span className="text-gray-400">amazing?</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
              Get started with our template and launch your next project faster than ever. No credit card required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth">
                <Button size="lg" className="rounded-xl bg-white text-black hover:bg-gray-100">
                  Start Free
                </Button>
              </Link>
              <Button size="lg" variant="glass-dark" className="rounded-xl">
                View Documentation
              </Button>
            </div>
            
            <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { value: '10+', label: 'components' },
                { value: '5 min', label: 'setup time' },
                { value: '100%', label: 'customizable' },
                { value: 'Free', label: 'to start' }
              ].map((stat, i) => (
                <div key={i} className="text-center glass-dark-subtle rounded-2xl py-6 px-4">
                  <div className="text-2xl md:text-3xl font-bold text-white mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Preview Section */}
        <section className="py-20 md:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="glass-card p-8 md:p-12 rounded-3xl">
              <div className="grid lg:grid-cols-2 gap-12 items-center">
                <div>
                  <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gray-900">
                    preview before you build
                  </h2>
                  <p className="text-lg text-gray-600 mb-8">
                    See what you're getting before you start. Our template includes a complete landing page, authentication flow, and dashboard.
                  </p>
                  <div className="space-y-4">
                    {[
                      'Modern landing page with sections',
                      'Sign in / Sign up authentication',
                      'User dashboard with account settings',
                      'All glassmorphism styled components'
                    ].map((item, i) => (
                      <div key={i} className="flex items-center space-x-3">
                        <svg className="w-5 h-5 text-black flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-gray-700">{item}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-8">
                    <Link href="/auth">
                      <Button className="rounded-xl">
                        Try It Now
                        <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                      </Button>
                    </Link>
                  </div>
                </div>
                <div className="flex justify-center">
                  <div className="relative">
                    <div className="w-full max-w-md glass-card rounded-2xl p-6 shadow-glass-xl">
                      <div className="flex items-center space-x-2 mb-6">
                        <div className="w-3 h-3 rounded-full bg-red-400"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                        <div className="w-3 h-3 rounded-full bg-green-400"></div>
                      </div>
                      <div className="space-y-4">
                        <div className="h-8 bg-gray-100 rounded-lg w-1/3"></div>
                        <div className="h-4 bg-gray-100 rounded w-full"></div>
                        <div className="h-4 bg-gray-100 rounded w-5/6"></div>
                        <div className="h-10 bg-black rounded-lg w-1/2 mt-6"></div>
                      </div>
                    </div>
                    <div className="absolute -top-4 -right-4 w-16 h-16 bg-black rounded-2xl flex items-center justify-center shadow-xl">
                      <span className="text-white font-bold text-2xl">S</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="gradient-dark py-16">
        <div className="container mx-auto px-4 md:px-6">
          <div className="glass-dark rounded-2xl p-8 mb-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="flex items-center space-x-3 mb-6 md:mb-0">
                <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center">
                  <span className="text-black font-bold text-lg">S</span>
                </div>
                <span className="text-xl font-bold text-white">Starter App</span>
              </div>
              <div className="flex items-center space-x-6">
                <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">Documentation</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">GitHub</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">Support</a>
              </div>
            </div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-500 mb-4">
              &copy; 2025 Starter App. All rights reserved.
            </div>
            <h2 className="text-6xl md:text-8xl font-black text-white opacity-5">starter app</h2>
          </div>
        </div>
      </footer>
    </div>
  )
}
