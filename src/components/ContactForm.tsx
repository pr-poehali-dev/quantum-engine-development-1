import { useState } from "react";
import { toast } from "sonner";

interface ContactFormProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ContactForm({ isOpen, onClose }: ContactFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    company: "",
    message: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.phone) {
      toast.error("Пожалуйста, заполните имя и телефон");
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch(
        `https://functions.poehali.dev/a42ca07f-ec22-455c-a1e4-ef0d4e142a9d`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        }
      );

      const data = await res.json();

      if (res.ok) {
        toast.success("Заявка отправлена! Мы свяжемся с вами в ближайшее время.");
        setFormData({ name: "", phone: "", company: "", message: "" });
        onClose();
      } else {
        toast.error(data.error || "Ошибка отправки. Попробуйте позже.");
      }
    } catch {
      toast.error("Ошибка соединения. Проверьте интернет и попробуйте снова.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />

      {/* Modal */}
      <div className="relative bg-white w-full max-w-lg z-10">
        {/* Header */}
        <div className="bg-neutral-900 px-8 py-6 flex justify-between items-center">
          <div>
            <h2 className="text-white text-lg font-bold uppercase tracking-widest">
              Заявка
            </h2>
            <p className="text-neutral-400 text-xs uppercase tracking-wide mt-1">
              Рассчитаем стоимость и свяжемся с вами
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-neutral-400 hover:text-white transition-colors duration-200 text-2xl leading-none"
            aria-label="Закрыть"
          >
            ×
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="px-8 py-6 space-y-4">
          <div>
            <label className="block text-xs uppercase tracking-widest text-neutral-500 mb-2">
              Ваше имя <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Иван Иванов"
              required
              className="w-full border border-neutral-200 px-4 py-3 text-sm focus:outline-none focus:border-neutral-900 transition-colors duration-200 placeholder-neutral-300"
            />
          </div>

          <div>
            <label className="block text-xs uppercase tracking-widest text-neutral-500 mb-2">
              Телефон <span className="text-red-500">*</span>
            </label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+7 (999) 123-45-67"
              required
              className="w-full border border-neutral-200 px-4 py-3 text-sm focus:outline-none focus:border-neutral-900 transition-colors duration-200 placeholder-neutral-300"
            />
          </div>

          <div>
            <label className="block text-xs uppercase tracking-widest text-neutral-500 mb-2">
              Название компании
            </label>
            <input
              type="text"
              name="company"
              value={formData.company}
              onChange={handleChange}
              placeholder="ООО Ромашка (необязательно)"
              className="w-full border border-neutral-200 px-4 py-3 text-sm focus:outline-none focus:border-neutral-900 transition-colors duration-200 placeholder-neutral-300"
            />
          </div>

          <div>
            <label className="block text-xs uppercase tracking-widest text-neutral-500 mb-2">
              Сообщение
            </label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Опишите ваш объект и что нужно сделать..."
              rows={3}
              className="w-full border border-neutral-200 px-4 py-3 text-sm focus:outline-none focus:border-neutral-900 transition-colors duration-200 placeholder-neutral-300 resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-neutral-900 text-white py-4 text-sm uppercase tracking-widest font-medium hover:bg-neutral-700 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Отправка..." : "Отправить заявку"}
          </button>

          <p className="text-neutral-400 text-xs text-center">
            Нажимая кнопку, вы соглашаетесь на обработку персональных данных
          </p>
        </form>
      </div>
    </div>
  );
}