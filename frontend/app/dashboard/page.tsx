"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/navbar";
import api from "@/services/api";

interface DashboardStats {
  total_patients: number;
  total_hospitals: number;
  admitted_patients: number;
  discharged_patients: number;
  total_users: number;
}

export default function DashboardPage() {

  const [stats, setStats] = useState<DashboardStats>({
    total_patients: 0,
    total_hospitals: 0,
    admitted_patients: 0,
    discharged_patients: 0,
    total_users: 0,
  });

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {

    try {

      const response = await api.get("/dashboard");

      setStats(response.data);

    } catch (error) {

      console.error(
        "Error fetching dashboard stats:",
        error
      );
    }
  };

  return (
    <>
      <Navbar />

      <main className="min-h-screen bg-gray-100 p-8">

        <h1 className="text-4xl font-bold mb-8">
          Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">

          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-gray-600">
              Total Patients
            </h2>

            <p className="text-3xl font-bold">
              {stats.total_patients}
            </p>
          </div>

          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-gray-600">
              Total Hospitals
            </h2>

            <p className="text-3xl font-bold">
              {stats.total_hospitals}
            </p>
          </div>

          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-gray-600">
              Admitted
            </h2>

            <p className="text-3xl font-bold">
              {stats.admitted_patients}
            </p>
          </div>

          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-gray-600">
              Discharged
            </h2>

            <p className="text-3xl font-bold">
              {stats.discharged_patients}
            </p>
          </div>

          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-gray-600">
              Total Users
            </h2>

            <p className="text-3xl font-bold">
              {stats.total_users}
            </p>
          </div>

        </div>

      </main>
    </>
  );
}