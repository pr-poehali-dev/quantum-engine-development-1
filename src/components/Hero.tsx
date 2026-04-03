import { useScroll, useTransform, motion } from "framer-motion";
import { useRef } from "react";

interface HeroProps {
  onCtaClick?: () => void;
}

export default function Hero({ onCtaClick }: HeroProps) {
  const container = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: container,
    offset: ["start start", "end start"],
  });
  const y = useTransform(scrollYProgress, [0, 1], ["0vh", "50vh"]);

  return (
    <div
      ref={container}
      className="relative flex items-center justify-center h-screen overflow-hidden"
    >
      <motion.div
        style={{ y }}
        className="absolute inset-0 w-full h-full"
      >
        <img
          src="https://cdn.poehali.dev/projects/c4a7b46a-6e1e-49d7-b1e2-70ddf2f9edcd/files/7984f629-7f85-4dcc-ba9e-e496d2896669.jpg"
          alt="Автоматические ворота"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/40" />
      </motion.div>

      <div className="relative z-10 text-center text-white">
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6">
          ОТКРЫВАЕМ
        </h1>
        <p className="text-lg md:text-xl max-w-2xl mx-auto px-6 opacity-90">
          Профессиональная установка автоматических ворот и шлагбаумов. Надёжно, быстро, с гарантией.
        </p>
        <button
          onClick={onCtaClick}
          className="mt-8 bg-white text-black px-8 py-3 text-sm uppercase tracking-widest font-medium hover:bg-neutral-200 transition-colors duration-300 cursor-pointer"
        >
          Получить расчёт
        </button>
      </div>
    </div>
  );
}
