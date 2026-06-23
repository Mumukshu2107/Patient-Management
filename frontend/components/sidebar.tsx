import Link from "next/link";

interface SidebarProps {
  items: {
    name: string;
    href: string;
  }[];
}

export default function Sidebar({
  items,
}: SidebarProps) {
  return (
    <aside className="w-64 bg-white shadow p-4">

      <h2 className="text-lg font-bold mb-4">
        Menu
      </h2>

      <div className="flex flex-col gap-3">

        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="hover:text-blue-600"
          >
            {item.name}
          </Link>
        ))}

      </div>

    </aside>
  );
}