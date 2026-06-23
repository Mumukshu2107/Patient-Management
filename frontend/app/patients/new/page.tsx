"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/services/api";
import ProtectedRoute from "@/components/ProtectedRoute";
import BackToDashboard from "@/components/BackToDashboard";

export default function NewPatientPage() {

    const router = useRouter();

    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [contactNo, setContactNo] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");
    const [bloodGroup, setBloodGroup] = useState("");

    const handleSubmit = async (
        e: React.FormEvent
    ) => {

        e.preventDefault();

        try {

            await api.post("/patients", {
                name,
                age: Number(age),
                contact_no: contactNo,
                height: Number(height),
                weight: Number(weight),
                blood_group: bloodGroup,
            });

            alert("Patient added successfully");

            router.push("/patients");

        } catch (error) {

            console.error(error);

            alert("Failed to add patient");
        }
    };

    return (
    <ProtectedRoute
    allowedRoles={[
      "SUPER_ADMIN",
      "ADMIN",
      "RECEPTIONIST",
    ]}
    >
    
    <div className="max-w-2xl mx-auto p-8">
      <BackToDashboard />

      <h1 className="text-3xl font-bold mb-6">
        Add Patient
      </h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-4"
      >

        <input
          type="text"
          placeholder="Patient Name"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        />

        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) =>
            setAge(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        />

        <input
          type="text"
          placeholder="Contact Number"
          value={contactNo}
          onChange={(e) =>
            setContactNo(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        />

        <input
          type="number"
          step="0.01"
          placeholder="Height"
          value={height}
          onChange={(e) =>
            setHeight(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        />

        <input
          type="number"
          step="0.01"
          placeholder="Weight"
          value={weight}
          onChange={(e) =>
            setWeight(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        />

        <select
          value={bloodGroup}
          onChange={(e) =>
            setBloodGroup(e.target.value)
          }
          className="w-full border p-3 rounded"
          required
        >
          <option value="">
            Select Blood Group
          </option>

          <option value="A+">A+</option>
          <option value="A-">A-</option>

          <option value="B+">B+</option>
          <option value="B-">B-</option>

          <option value="AB+">AB+</option>
          <option value="AB-">AB-</option>

          <option value="O+">O+</option>
          <option value="O-">O-</option>

        </select>

        <button
          type="submit"
          className="bg-blue-700 text-white px-6 py-3 rounded"
        >
          Add Patient
        </button>

      </form>

    </div>
    </ProtectedRoute >
  );
}