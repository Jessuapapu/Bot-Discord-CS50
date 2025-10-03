// src/layouts/MainLayout.jsx
import { Outlet } from "react-router-dom";
import Navbar from "../components/layout/Navbar";

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow p-6">
        <Outlet />
      </main>
      <footer className="bg-gray-800 text-white text-center py-3">
        © 2025 Mi App
      </footer>
    </div>
  );
}
