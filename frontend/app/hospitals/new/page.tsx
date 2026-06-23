"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/services/api";
import ProtectedRoute from "@/components/ProtectedRoute";
import BackToDashboard from "@/components/BackToDashboard";

export default function NewHospitalPage() {

  const router = useRouter();

  const [name, setName] = useState("");
  const [city, setCity] = useState("");

  const handleSubmit = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    try {

      await api.post("/hospitals", {
        name,
        city,
      });

      alert("Hospital added successfully");

      router.push("/hospitals");

    } catch (error) {

      console.error(error);

      alert("Failed to add hospital");
    }
  };

  return (
    <ProtectedRoute
      allowedRoles={[
        "SUPER_ADMIN",
        "ADMIN",
      ]}
    >
      <div className="max-w-2xl mx-auto p-8">
        <BackToDashboard />

        <h1 className="text-3xl font-bold mb-6">
          Add Hospital
        </h1>
        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >

          <input
            type="text"
            placeholder="Hospital Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            className="w-full border p-3 rounded"
            required
          />

          <input
            type="text"
            placeholder="City"
            value={city}
            onChange={(e) =>
              setCity(e.target.value)
            }
            className="w-full border p-3 rounded"
            required
          />

          <button
            type="submit"
            className="bg-blue-700 text-white px-6 py-3 rounded"
          >
            Add Hospital
          </button>

        </form>

      </div>
    </ProtectedRoute>
  );
}