"use client";

import { useRouter } from "next/navigation";

export default function BackToDashboard() {

  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/dashboard")}
      className="
        mb-6
        flex
        items-center
        gap-2
        bg-gray-200
        hover:bg-gray-300
        px-4
        py-2
        rounded
        font-small
      "
    >
      ← Back
    </button>
  );
}