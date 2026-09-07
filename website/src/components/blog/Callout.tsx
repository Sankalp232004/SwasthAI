import React from "react";
import { Info, Lightbulb, AlertTriangle, ShieldAlert } from "lucide-react";

interface CalloutProps {
  type?: "info" | "tip" | "warning" | "caution";
  title?: string;
  children: React.ReactNode;
}

export default function Callout({ type = "info", title, children }: CalloutProps) {
  const styles = {
    info: {
      wrapper: "border-teal-500/30 bg-gradient-to-r from-teal-50/90 via-cyan-50/40 to-teal-50/70 text-teal-950",
      accentBar: "bg-gradient-to-b from-teal-500 to-cyan-600",
      iconBg: "bg-teal-500/15 text-teal-700 border-teal-400/30",
      icon: <Info className="w-5 h-5" />,
      defaultTitle: "Clinical & Operational Note",
      titleColor: "text-teal-900",
    },
    tip: {
      wrapper: "border-emerald-500/30 bg-gradient-to-r from-emerald-50/90 via-green-50/40 to-emerald-50/70 text-emerald-950",
      accentBar: "bg-gradient-to-b from-emerald-500 to-green-600",
      iconBg: "bg-emerald-500/15 text-emerald-700 border-emerald-400/30",
      icon: <Lightbulb className="w-5 h-5" />,
      defaultTitle: "Practice Recommendation",
      titleColor: "text-emerald-900",
    },
    warning: {
      wrapper: "border-amber-500/30 bg-gradient-to-r from-amber-50/95 via-yellow-50/40 to-amber-50/70 text-amber-950",
      accentBar: "bg-gradient-to-b from-amber-500 to-orange-500",
      iconBg: "bg-amber-500/15 text-amber-700 border-amber-400/30",
      icon: <AlertTriangle className="w-5 h-5" />,
      defaultTitle: "High-Priority Notice",
      titleColor: "text-amber-900",
    },
    caution: {
      wrapper: "border-rose-500/30 bg-gradient-to-r from-rose-50/95 via-red-50/40 to-rose-50/70 text-rose-950",
      accentBar: "bg-gradient-to-b from-rose-500 to-red-600",
      iconBg: "bg-rose-500/15 text-rose-700 border-rose-400/30",
      icon: <ShieldAlert className="w-5 h-5" />,
      defaultTitle: "Critical Safety Warning",
      titleColor: "text-rose-900",
    },
  };

  const current = styles[type] || styles.info;

  return (
    <div className={`my-8 p-5 sm:p-6 rounded-3xl border ${current.wrapper} shadow-md flex items-start gap-4 relative overflow-hidden transition-all duration-300 hover:shadow-lg`}>
      {/* Left accent indicator */}
      <div className={`absolute left-0 top-0 bottom-0 w-1.5 ${current.accentBar}`} />
      
      {/* Icon with glowing pill ring */}
      <div className={`w-10 h-10 rounded-2xl ${current.iconBg} border flex items-center justify-center shrink-0 mt-0.5 shadow-xs`}>
        {current.icon}
      </div>

      <div className="space-y-1.5 text-sm sm:text-base leading-relaxed flex-1">
        <h4 className={`font-extrabold text-xs uppercase tracking-wider ${current.titleColor}`}>
          {title || current.defaultTitle}
        </h4>
        <div className="font-medium opacity-95">{children}</div>
      </div>
    </div>
  );
}
