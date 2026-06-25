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

  const [showForm, setShowForm] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("ADMIN");

  const [error, setError] = useState("");

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

  const handleCreateUser = async () => {
    setError("");

    if (username.trim() === "") {
      setError("Username is required.");
      return;
    }

    if (password.trim() === "") {
      setError("Password is required.");
      return;
    }

    try {
      await api.post("/users", {
        username,
        password,
        role,
      });

      setUsername("");
      setPassword("");
      setRole("ADMIN");
      setError("");

      setShowForm(false);

      fetchUsers();

      alert("User created successfully");
    } catch (error) {
      console.error(error);
      setError("Failed to create user.");
    }
  };

  return (
    <ProtectedRoute allowedRoles={["SUPER_ADMIN"]}>
      <div className="max-w-6xl mx-auto p-8">

        <BackToDashboard />

        <div className="flex justify-between items-center mb-6">

          <h1 className="text-3xl font-bold">
            Manage Users
          </h1>

          <button
            onClick={() => {
              setShowForm(true);
              setError("");
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 text-sm rounded-md"
          >
            + Add User
          </button>

        </div>

        <div className="bg-white shadow rounded-lg overflow-hidden">

          <table className="w-full">

            <thead className="bg-gray-100">

              <tr>
                <th className="p-4 text-left border">
                  ID
                </th>

                <th className="p-4 text-left border">
                  Username
                </th>

                <th className="p-4 text-left border">
                  Role
                </th>
              </tr>

            </thead>

            <tbody>

              {users.map((user) => (
                <tr
                  key={user.id}
                  className="hover:bg-gray-50"
                >
                  <td className="border p-4">
                    {user.id}
                  </td>

                  <td className="border p-4">
                    {user.username}
                  </td>

                  <td className="border p-4">
                    <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm font-medium">
                      {user.role}
                    </span>
                  </td>
                </tr>
              ))}

            </tbody>

          </table>

        </div>

        {/* Add User Modal */}

        {showForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

            <div className="bg-white w-96 rounded-xl shadow-xl p-6">

              <h2 className="text-2xl font-bold mb-5">
                Add New User
              </h2>

              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
                  {error}
                </div>
              )}

              <div className="space-y-4">

                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => {
                    setUsername(e.target.value);
                    setError("");
                  }}
                  className={`w-full p-3 rounded border ${
                    error && username.trim() === ""
                      ? "border-red-500"
                      : "border-gray-300"
                  }`}
                />

                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError("");
                  }}
                  className={`w-full p-3 rounded border ${
                    error && password.trim() === ""
                      ? "border-red-500"
                      : "border-gray-300"
                  }`}
                />

                <select
                  value={role}
                  onChange={(e) =>
                    setRole(e.target.value)
                  }
                  className="w-full border border-gray-300 p-3 rounded"
                >
                  <option value="ADMIN">
                    ADMIN
                  </option>

                  <option value="DOCTOR">
                    DOCTOR
                  </option>

                  <option value="RECEPTIONIST">
                    RECEPTIONIST
                  </option>
                </select>

              </div>

              <div className="flex justify-end gap-3 mt-6">

                <button
                  onClick={() => {
                    setShowForm(false);
                    setError("");
                    setUsername("");
                    setPassword("");
                    setRole("ADMIN");
                  }}
                  className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                >
                  Cancel
                </button>

                <button
                  onClick={handleCreateUser}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Create User
                </button>

              </div>

            </div>

          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}