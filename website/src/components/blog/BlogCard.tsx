import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Clock, Calendar, ArrowUpRight } from "lucide-react";
import { BlogPostMeta } from "@/lib/mdx";

interface BlogCardProps {
  post: BlogPostMeta;
  featured?: boolean;
}

export default function BlogCard({ post, featured = false }: BlogCardProps) {
  if (featured) {
    return (
      <div className="group bg-gradient-to-br from-[#0F2C59] via-[#0D254C] to-[#07162C] text-white rounded-3xl overflow-hidden border border-white/15 shadow-2xl hover:border-teal-400/50 transition-all duration-500 grid grid-cols-1 lg:grid-cols-12 blog-card-hover relative">
        {/* Glow backdrop */}
        <div className="absolute top-0 right-0 w-80 h-80 bg-teal-500/10 rounded-full blur-3xl pointer-events-none group-hover:bg-teal-500/20 transition-all"></div>

        <div className="lg:col-span-7 relative aspect-[16/10] lg:aspect-auto bg-slate-950 overflow-hidden min-h-[260px] sm:min-h-[320px]">
          <Image
            src={post.featuredImage}
            alt={post.title}
            fill
            className="object-cover object-center group-hover:scale-105 transition-transform duration-700 ease-out"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#07162C]/80 via-transparent to-transparent lg:hidden"></div>
          <div className="absolute top-4 left-4 z-10">
            <span className="px-3.5 py-1.5 rounded-full bg-gradient-to-r from-teal-500 to-emerald-500 backdrop-blur-md text-white font-extrabold text-xs tracking-wider uppercase shadow-lg border border-white/20">
              Spotlight Case Study
            </span>
          </div>
        </div>

        <div className="lg:col-span-5 p-6 sm:p-9 flex flex-col justify-between space-y-6 relative z-10">
          <div className="space-y-3.5">
            <div className="flex items-center gap-2.5 text-xs text-teal-300 font-semibold flex-wrap">
              <span className="px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/30">
                {post.category}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1.5 text-slate-300">
                <Clock className="w-3.5 h-3.5 text-teal-400" />
                {post.readingTime}
              </span>
            </div>

            <Link href={`/blog/${post.slug}`} className="block group-hover:text-teal-300 transition-colors">
              <h2 className="text-xl sm:text-2xl font-extrabold tracking-tight leading-snug text-white">
                {post.title}
              </h2>
            </Link>

            <p className="text-xs sm:text-sm text-slate-300 line-clamp-3 leading-relaxed font-normal">
              {post.excerpt}
            </p>
          </div>

          <div className="pt-5 border-t border-white/10 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-full bg-teal-500/20 text-teal-300 border border-teal-400/40 flex items-center justify-center font-bold text-xs shadow-xs">
                {post.author.charAt(0)}
              </div>
              <div>
                <span className="block text-xs font-bold text-white">{post.author}</span>
                <span className="block text-[10px] text-slate-400">{post.publishedAt}</span>
              </div>
            </div>

            <Link
              href={`/blog/${post.slug}`}
              className="w-10 h-10 rounded-2xl bg-teal-500/20 group-hover:bg-gradient-to-r group-hover:from-teal-500 group-hover:to-emerald-500 text-teal-300 group-hover:text-white flex items-center justify-center transition-all shadow-md group-hover:scale-105"
              title="Read full article"
            >
              <ArrowUpRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <article className="group bg-white rounded-3xl overflow-hidden border border-slate-200/90 shadow-sm hover:shadow-xl transition-all duration-400 flex flex-col justify-between blog-card-hover relative">
      <div>
        <div className="relative aspect-[16/9] bg-slate-100 overflow-hidden">
          <Image
            src={post.featuredImage}
            alt={post.title}
            fill
            className="object-cover object-center group-hover:scale-105 transition-transform duration-600 ease-out"
          />
          <div className="absolute top-3.5 left-3.5">
            <span className="px-3 py-1 rounded-full bg-[#0F2C59]/90 backdrop-blur-md text-white font-bold text-[10px] uppercase tracking-wider border border-white/20 shadow-xs">
              {post.category}
            </span>
          </div>
        </div>

        <div className="p-6 space-y-3.5">
          <div className="flex items-center gap-2.5 text-xs text-slate-500 font-medium">
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-teal-600" />
              {post.publishedAt}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-teal-600" />
              {post.readingTime}
            </span>
          </div>

          <Link href={`/blog/${post.slug}`} className="block group-hover:text-teal-700 transition-colors">
            <h3 className="text-base sm:text-lg font-bold text-[#0F2C59] leading-snug line-clamp-2">
              {post.title}
            </h3>
          </Link>

          <p className="text-xs sm:text-sm text-slate-600 line-clamp-3 leading-relaxed">
            {post.excerpt}
          </p>
        </div>
      </div>

      <div className="p-6 pt-0 flex items-center justify-between border-t border-slate-100 mt-2">
        <div className="flex items-center space-x-2.5 pt-3">
          <div className="w-7 h-7 rounded-full bg-[#0F2C59] text-white flex items-center justify-center font-bold text-[10px] shadow-xs">
            {post.author.charAt(0)}
          </div>
          <span className="text-xs font-semibold text-slate-700">{post.author}</span>
        </div>

        <Link
          href={`/blog/${post.slug}`}
          className="text-xs font-bold text-teal-700 group-hover:text-teal-900 flex items-center gap-1 pt-3 group-hover:translate-x-0.5 transition-all"
        >
          <span>Read</span>
          <ArrowUpRight className="w-3.5 h-3.5 text-teal-600" />
        </Link>
      </div>
    </article>
  );
}
