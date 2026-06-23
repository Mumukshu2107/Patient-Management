"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import BackToDashboard from "@/components/BackToDashboard";

export default function ProfilePage() {

  const [user, setUser] = useState<any>();

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

  return (
    <div className="p-10">
      <BackToDashboard />

      <h1 className="text-3xl font-bold">
        Logged In User
      </h1>

      <pre className="mt-5">
        {JSON.stringify(user, null, 2)}
      </pre>

    </div>
  );
}