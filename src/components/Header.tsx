interface HeaderProps {
  className?: string;
  onContactClick?: () => void;
}

export default function Header({ className, onContactClick }: HeaderProps) {
  return (
    <header className={`absolute top-0 left-0 right-0 z-10 p-6 ${className ?? ""}`}>
      <div className="flex justify-between items-center">
        <div className="text-white text-sm uppercase tracking-wide">АвтоВорота</div>
        <nav className="flex gap-8">
          <a
            href="#services"
            className="text-white hover:text-neutral-400 transition-colors duration-300 uppercase text-sm"
          >
            Услуги
          </a>
          <button
            onClick={onContactClick}
            className="text-white hover:text-neutral-400 transition-colors duration-300 uppercase text-sm cursor-pointer bg-transparent border-none"
          >
            Заказать
          </button>
        </nav>
      </div>
    </header>
  );
}
