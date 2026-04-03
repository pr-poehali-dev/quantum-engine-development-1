import { useState } from "react";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Featured from "@/components/Featured";
import Promo from "@/components/Promo";
import Footer from "@/components/Footer";
import ContactForm from "@/components/ContactForm";

const Index = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);

  return (
    <main className="min-h-screen">
      <Header onContactClick={() => setIsFormOpen(true)} />
      <Hero onCtaClick={() => setIsFormOpen(true)} />
      <Featured onCtaClick={() => setIsFormOpen(true)} />
      <Promo />

      {/* Contact Section */}
      <section id="contact" className="bg-white px-6 py-20 lg:py-32">
        <div className="max-w-3xl mx-auto text-center">
          <h3 className="uppercase text-xs sm:text-sm tracking-widest text-neutral-500 mb-4">
            Оставьте заявку
          </h3>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-neutral-900 leading-tight mb-6">
            Рассчитаем стоимость<br />бесплатно
          </h2>
          <p className="text-neutral-600 text-base lg:text-lg mb-10 max-w-xl mx-auto">
            Укажите ваш объект и задачу — мы подберём оборудование и пришлём точную смету в течение 1 часа.
          </p>
          <button
            onClick={() => setIsFormOpen(true)}
            className="bg-neutral-900 text-white px-10 py-4 text-sm uppercase tracking-widest font-medium hover:bg-neutral-700 transition-colors duration-300 cursor-pointer"
          >
            Получить расчёт
          </button>
        </div>
      </section>

      <Footer />
      <ContactForm isOpen={isFormOpen} onClose={() => setIsFormOpen(false)} />
    </main>
  );
};

export default Index;
