"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import ProtectedRoute from "@/components/ProtectedRoute";
import BackToDashboard from "@/components/BackToDashboard";

interface User {
  id: number;
  username: string;
  role: string;
}

export default function UsersPage() {

  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {

    try {

      const response = await api.get("/users");

      setUsers(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  return (
    <ProtectedRoute
      allowedRoles={[
        "SUPER_ADMIN"
      ]}
    >
      <div className="max-w-6xl mx-auto p-8">
        <BackToDashboard />

        <h1 className="text-3xl font-bold mb-6">
          Users
        </h1>

        <table className="w-full border border-gray-300">

          <thead>

            <tr className="bg-gray-100">

              <th className="border p-3">
                ID
              </th>

              <th className="border p-3">
                Username
              </th>

              <th className="border p-3">
                Role
              </th>

            </tr>

          </thead>

          <tbody>

            {users.map((user) => (

              <tr key={user.id}>

                <td className="border p-3">
                  {user.id}
                </td>

                <td className="border p-3">
                  {user.username}
                </td>

                <td className="border p-3">
                  {user.role}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>
    </ProtectedRoute>
  );
}