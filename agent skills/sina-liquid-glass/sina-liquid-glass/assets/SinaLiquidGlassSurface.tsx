"use client";

import { useRef, type CSSProperties, type ReactNode } from "react";
import dynamic from "next/dynamic";

const LiquidGlass = dynamic(() => import("liquid-glass-react"), {
  ssr: false,
  loading: () => null,
});

type GlassTone = "cyan" | "green" | "amber" | "red" | "violet" | "white";
type GlassVariant = "hero" | "metric" | "panel";

function cx(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ");
}

const toneClass: Record<GlassTone, string> = {
  cyan: "[&_.glass]:!bg-cyan-50/[0.052] [&_.glass__warp]:!bg-cyan-50/[0.026] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.30),0_10px_34px_rgba(165,243,252,0.28),inset_0_0_34px_rgba(165,243,252,0.10)]",
  green: "[&_.glass]:!bg-emerald-50/[0.052] [&_.glass__warp]:!bg-emerald-50/[0.026] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.30),0_10px_34px_rgba(167,243,208,0.28),inset_0_0_34px_rgba(167,243,208,0.10)]",
  amber: "[&_.glass]:!bg-amber-50/[0.052] [&_.glass__warp]:!bg-amber-50/[0.026] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.30),0_10px_34px_rgba(254,240,138,0.26),inset_0_0_34px_rgba(254,240,138,0.09)]",
  red: "[&_.glass]:!bg-red-50/[0.052] [&_.glass__warp]:!bg-red-50/[0.026] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.30),0_10px_34px_rgba(254,202,202,0.25),inset_0_0_34px_rgba(254,202,202,0.09)]",
  violet: "[&_.glass]:!bg-violet-50/[0.06] [&_.glass__warp]:!bg-violet-50/[0.03] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.32),0_10px_36px_rgba(221,214,254,0.30),inset_0_0_36px_rgba(221,214,254,0.11)]",
  white: "[&_.glass]:!bg-white/[0.05] [&_.glass__warp]:!bg-white/[0.026] [&_.glass]:!shadow-[0_26px_52px_rgba(0,0,0,0.32),0_10px_34px_rgba(255,255,255,0.24),inset_0_0_34px_rgba(255,255,255,0.09)]",
};

const edgeGradient: Record<GlassTone, string> = {
  cyan: "linear-gradient(135deg, rgba(236,254,255,0.74) 0%, rgba(103,232,249,0.18) 28%, rgba(255,255,255,0.08) 52%, rgba(34,211,238,0.26) 100%)",
  green: "linear-gradient(135deg, rgba(236,253,245,0.72) 0%, rgba(110,231,183,0.18) 28%, rgba(255,255,255,0.08) 52%, rgba(52,211,153,0.25) 100%)",
  amber: "linear-gradient(135deg, rgba(255,251,235,0.72) 0%, rgba(253,230,138,0.18) 28%, rgba(255,255,255,0.08) 52%, rgba(251,191,36,0.24) 100%)",
  red: "linear-gradient(135deg, rgba(254,242,242,0.72) 0%, rgba(252,165,165,0.18) 28%, rgba(255,255,255,0.08) 52%, rgba(248,113,113,0.24) 100%)",
  violet: "linear-gradient(135deg, rgba(245,243,255,0.76) 0%, rgba(196,181,253,0.2) 28%, rgba(255,255,255,0.09) 52%, rgba(167,139,250,0.28) 100%)",
  white: "linear-gradient(135deg, rgba(255,255,255,0.78) 0%, rgba(255,255,255,0.18) 28%, rgba(255,255,255,0.08) 52%, rgba(255,255,255,0.28) 100%)",
};

const variantProps: Record<
  GlassVariant,
  {
    displacementScale: number;
    blurAmount: number;
    saturation: number;
    aberrationIntensity: number;
    elasticity: number;
    mode: "standard" | "polar" | "prominent";
  }
> = {
  hero: { displacementScale: 58, blurAmount: 0.05, saturation: 116, aberrationIntensity: 1.05, elasticity: 0, mode: "standard" },
  metric: { displacementScale: 40, blurAmount: 0.05, saturation: 112, aberrationIntensity: 0.82, elasticity: 0, mode: "standard" },
  panel: { displacementScale: 34, blurAmount: 0.05, saturation: 110, aberrationIntensity: 0.68, elasticity: 0, mode: "standard" },
};

export default function SinaLiquidGlassSurface({
  children,
  className,
  contentClassName,
  tone = "white",
  variant = "panel",
  radius = 10,
  style,
}: {
  children: ReactNode;
  className?: string;
  contentClassName?: string;
  tone?: GlassTone;
  variant?: GlassVariant;
  radius?: number;
  style?: CSSProperties;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const props = variantProps[variant];
  const edgeWidth = variant === "hero" ? 1.35 : 1.15;

  return (
    <div
      ref={ref}
      className={cx(
        "relative min-w-0 overflow-visible",
        "[&>div.bg-black]:!hidden [&>span]:!hidden",
        className,
      )}
      style={style}
    >
      <div aria-hidden="true" className={cx("invisible pointer-events-none", contentClassName)}>
        {children}
      </div>

      <LiquidGlass
        mouseContainer={ref}
        mode={props.mode}
        displacementScale={props.displacementScale}
        blurAmount={props.blurAmount}
        saturation={props.saturation}
        aberrationIntensity={props.aberrationIntensity}
        elasticity={props.elasticity}
        cornerRadius={radius}
        padding="0px"
        className={cx(
          "absolute z-0 h-full w-full text-white",
          "[&_.glass]:!flex [&_.glass]:!h-full [&_.glass]:!w-full [&_.glass]:!items-stretch [&_.glass]:!gap-0",
          "[&_.glass]:!border-0",
          "[&_.glass>div]:!h-full [&_.glass>div]:!w-full [&_.glass>div]:!font-[inherit]",
          "[&_.glass__warp]:!backdrop-blur-[3px] [&_.glass__warp]:!backdrop-saturate-[116%]",
          toneClass[tone],
        )}
        style={{ position: "absolute", left: "50%", top: "50%", width: "100%", height: "100%" }}
      >
        <div className={cx("h-full w-full", contentClassName)}>{children}</div>
      </LiquidGlass>

      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 z-[2]"
        style={{
          borderRadius: `${radius}px`,
          padding: `${edgeWidth}px`,
          background: edgeGradient[tone],
          WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
        }}
      />
    </div>
  );
}
