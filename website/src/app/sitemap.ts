import type { MetadataRoute } from "next";
import { getAllPosts, getAllCategories } from "@/lib/mdx";
import { SITE_CONFIG } from "@/lib/config";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getAllPosts();
  const categories = getAllCategories();
  const baseUrl = SITE_CONFIG.url;

  // Static core routes
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "daily",
      priority: 1.0,
    },
    {
      url: `${baseUrl}/features`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "weekly",
      priority: 0.9,
    },
    {
      url: `${baseUrl}/demo`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "weekly",
      priority: 0.9,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "daily",
      priority: 0.9,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${baseUrl}/privacy`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
  ];

  // Dynamic Blog Posts
  const blogRoutes: MetadataRoute.Sitemap = posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.publishedAt),
    changeFrequency: "weekly",
    priority: post.slug === "receptionist-triage-decisions-indian-clinics" ? 0.9 : 0.8,
  }));

  // Dynamic Category Routes
  const categoryRoutes: MetadataRoute.Sitemap = categories
    .filter((cat) => cat.slug !== "all")
    .map((cat) => ({
      url: `${baseUrl}/blog/category/${cat.slug}`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "weekly",
      priority: 0.7,
    }));

  // Author Routes
  const authorRoutes: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}/blog/author/sankalp-mishra`,
      lastModified: new Date("2026-09-07"),
      changeFrequency: "weekly",
      priority: 0.6,
    },
  ];

  return [...staticRoutes, ...blogRoutes, ...categoryRoutes, ...authorRoutes];
}
