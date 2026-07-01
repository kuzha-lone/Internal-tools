// Hero Section Component for Landing Page
// This is the main banner section at the top of the homepage
// Edit text content in src/config/landing.js

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { landingConfig } from '@/config/landing'

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-white gradient-mesh">
      <div className="container mx-auto px-4 py-24 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          {/* Main Hero Title */}
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight text-gray-900">
            {landingConfig.heroTitle}
          </h1>
          
          {/* Hero Subtitle */}
          <p className="text-xl md:text-2xl mb-4 text-gray-600 font-medium">
            {landingConfig.heroSubtitle}
          </p>
          
          {/* Hero Description */}
          <p className="text-lg mb-8 text-gray-500 max-w-2xl mx-auto">
            {landingConfig.heroDescription}
          </p>
          
          {/* Call-to-Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/auth">
              <Button size="lg" className="font-semibold px-8 py-3 rounded-xl">
                {landingConfig.primaryButtonText}
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="glass" className="px-8 py-3 rounded-xl">
                {landingConfig.secondaryButtonText}
              </Button>
            </Link>
          </div>
        </div>
      </div>
      
      {/* Decorative Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute top-20 right-10 w-72 h-72 bg-gray-200/40 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 left-10 w-96 h-96 bg-gray-300/30 rounded-full blur-3xl animate-float animation-delay-300"></div>
      </div>
    </section>
  )
}
