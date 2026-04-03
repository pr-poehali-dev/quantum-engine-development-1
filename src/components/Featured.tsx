export default function Featured() {
  return (
    <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center min-h-screen px-6 py-12 lg:py-0 bg-white">
      <div className="flex-1 h-[400px] lg:h-[800px] mb-8 lg:mb-0 lg:order-2">
        <img
          src="https://cdn.poehali.dev/projects/c4a7b46a-6e1e-49d7-b1e2-70ddf2f9edcd/files/2b7e34b2-fb8b-411b-8233-2e82b11bb113.jpg"
          alt="Автоматический шлагбаум"
          className="w-full h-full object-cover"
        />
      </div>
      <div className="flex-1 text-left lg:h-[800px] flex flex-col justify-center lg:mr-12 lg:order-1">
        <h3 className="uppercase mb-4 text-sm tracking-wide text-neutral-600" id="services">Почему выбирают нас</h3>
        <p className="text-2xl lg:text-4xl mb-8 text-neutral-900 leading-tight">
          Монтаж за 1 день. Работаем с частными домами, коммерческой недвижимостью и промышленными объектами. Гарантия на все виды работ — 2 года.
        </p>
        <div className="flex flex-col gap-3 mb-8 text-neutral-700 text-base lg:text-lg">
          <span>→ Откатные, распашные, секционные ворота</span>
          <span>→ Шлагбаумы для парковок и КПП</span>
          <span>→ Сервисное обслуживание и ремонт</span>
        </div>
        <button className="bg-black text-white border border-black px-4 py-2 text-sm transition-all duration-300 hover:bg-white hover:text-black cursor-pointer w-fit uppercase tracking-wide">
          Рассчитать стоимость
        </button>
      </div>
    </div>
  );
}