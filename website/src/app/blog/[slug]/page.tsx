import React from "react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import CTASection from "@/components/CTASection";
import { BLOG_POSTS, SITE_CONFIG } from "@/lib/config";
import { ArrowLeft, Clock, Calendar, User, MessageSquare } from "lucide-react";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return BLOG_POSTS.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = BLOG_POSTS.find((p) => p.slug === slug);
  if (!post) return { title: "Article Not Found" };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: `${post.title} | SwasthAI`,
      description: post.excerpt,
      type: "article",
      publishedTime: post.publishedAt,
      authors: [post.author],
    },
  };
}

export default async function SingleBlogPage({ params }: Props) {
  const { slug } = await params;
  const post = BLOG_POSTS.find((p) => p.slug === slug);

  if (!post) {
    notFound();
  }

  const waLink = `https://wa.me/${SITE_CONFIG.whatsappRaw}?text=${encodeURIComponent(SITE_CONFIG.whatsappMessages.doctorDemo)}`;

  return (
    <div className="pt-28 sm:pt-36">
      
      {/* Header */}
      <section className="bg-[#0F2C59] text-white py-16 sm:py-20 border-b border-white/10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <Link
            href="/blog"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-teal-300 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to All Articles</span>
          </Link>

          <div className="space-y-4">
            <span className="inline-block px-3 py-1 rounded-full bg-white/10 text-teal-300 text-xs font-bold border border-white/15">
              {post.category}
            </span>

            <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
              {post.title}
            </h1>

            <div className="flex items-center space-x-4 text-xs text-gray-300 pt-2 border-t border-white/10">
              <span className="flex items-center gap-1">
                <User className="w-3.5 h-3.5 text-teal-400" />
                {post.author}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-teal-400" />
                {post.publishedAt}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-teal-400" />
                {post.readTime}
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Article Content */}
      <section className="py-16 bg-white">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          
          <div className="text-lg text-slate-700 leading-relaxed font-medium border-b border-slate-200 pb-6 italic">
            &ldquo;{post.excerpt}&rdquo;
          </div>

          <div className="prose prose-slate max-w-none space-y-6 text-slate-700 leading-relaxed">
            {post.content.split('\n\n').map((paragraph, idx) => {
              if (paragraph.trim().startsWith('### ')) {
                return (
                  <h3 key={idx} className="text-xl font-bold text-[#0F2C59] pt-4">
                    {paragraph.replace('### ', '')}
                  </h3>
                );
              }
              return (
                <p key={idx} className="text-base text-slate-700 leading-relaxed">
                  {paragraph}
                </p>
              );
            })}
          </div>

          {/* Author Bio Card */}
          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 mt-12 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h4 className="text-base font-bold text-[#0F2C59]">Written by {post.author}</h4>
              <p className="text-xs text-slate-600 mt-0.5">{SITE_CONFIG.founder.bio}</p>
            </div>
            <a
              href={waLink}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#25D366] hover:bg-[#1DA851] text-white px-4 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 shadow-md shrink-0"
            >
              <MessageSquare className="w-4 h-4 fill-white" />
              <span>Book Demo on WhatsApp</span>
            </a>
          </div>

        </div>
      </section>

      <CTASection />
    </div>
  );
}
