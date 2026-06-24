"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import BackToDashboard from "@/components/BackToDashboard";

export default function ProfilePage() {

  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const response = await api.get("/me");
      setUser(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case "SUPER_ADMIN":
        return "bg-red-100 text-red-700";

      case "ADMIN":
        return "bg-green-100 text-green-700";

      case "DOCTOR":
        return "bg-purple-100 text-purple-700";

      case "RECEPTIONIST":
        return "bg-blue-100 text-blue-700";

      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  if (!user) {
    return (
      <div className="p-10">
        <BackToDashboard />

        <div className="mt-10 text-gray-500 text-lg">
          Loading profile...
        </div>
      </div>
    );
  }

  return (
  <div className="min-h-screen bg-gray-100">

    <div className="p-6">
      <BackToDashboard />
    </div>

    <div className="flex justify-center items-center px-4">

      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-2xl">

        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          My Profile
        </h1>

        {/* User Header */}
        <div className="flex flex-col items-center mb-8">

          <div className="w-24 h-24 rounded-full bg-blue-600 flex items-center justify-center text-white text-4xl font-bold mb-4">
            {user.username.charAt(0).toUpperCase()}
          </div>

          <h2 className="text-3xl font-semibold text-gray-800">
            {user.username}
          </h2>

          <p className="text-gray-500 mt-1">
            Hospital Management System User
          </p>

          <span
            className={`mt-4 px-4 py-2 rounded-full font-semibold ${getRoleColor(
              user.role
            )}`}
          >
            {user.role}
          </span>

        </div>

        {/* User Details */}
        <div className="space-y-5">

          <div className="border rounded-lg p-4">
            <p className="text-sm text-gray-500">
              User ID
            </p>
            <p className="text-xl font-semibold">
              {user.id}
            </p>
          </div>

          <div className="border rounded-lg p-4">
            <p className="text-sm text-gray-500">
              Username
            </p>
            <p className="text-xl font-semibold">
              {user.username}
            </p>
          </div>

        </div>

      </div>

    </div>

  </div>
);
}