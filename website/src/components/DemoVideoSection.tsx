import React from "react";
import { MessageSquare, Play, Shield, CheckCircle2 } from "lucide-react";
import { SITE_CONFIG } from "@/lib/config";

export default function DemoVideoSection() {
  const waLink = `https://wa.me/${SITE_CONFIG.whatsappRaw}?text=${encodeURIComponent(SITE_CONFIG.whatsappMessages.doctorDemo)}`;

  return (
    <section className="py-20 bg-[#0F2C59] text-white relative overflow-hidden">
      {/* Glow Effects */}
      <div className="absolute top-1/2 left-0 -translate-y-1/2 -ml-24 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 right-0 -translate-y-1/2 -mr-24 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-teal-300 text-xs font-bold border border-white/15">
            <Play className="w-3.5 h-3.5 fill-teal-300" />
            <span>Product Demo Walkthrough</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            See SwasthAI in Action Across Real OPD Scenarios
          </h2>

          <p className="text-base sm:text-lg text-gray-200 leading-relaxed">
            Watch our short demonstration video showcasing patient intake, urgency scoring calculation, doctor queue management, and offline capabilities.
          </p>
        </div>

        {/* Video Embed Container */}
        <div className="max-w-4xl mx-auto rounded-3xl overflow-hidden border border-white/20 shadow-2xl bg-black/60 backdrop-blur-md">
          <div className="relative aspect-video w-full">
            <iframe
              src={SITE_CONFIG.demoVideoEmbedUrl}
              title="SwasthAI Product Demo"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
              className="absolute top-0 left-0 w-full h-full border-0"
            />
          </div>

          {/* Action Bar below video */}
          <div className="p-6 bg-[#07162C] border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="space-y-1 text-center sm:text-left">
              <span className="block text-sm font-bold text-white">Interested in trying this for your clinic?</span>
              <span className="block text-xs text-gray-400">Schedule a 15-minute walkthrough or try our low-friction 1-week pilot.</span>
            </div>

            <a
              href={waLink}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#25D366] hover:bg-[#1DA851] text-white px-6 py-3 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg transition-all shrink-0"
            >
              <MessageSquare className="w-4 h-4 fill-white" />
              <span>Book a Demo on WhatsApp</span>
            </a>
          </div>
        </div>

      </div>
    </section>
  );
}
