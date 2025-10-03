import { Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import Home from "../pages/Home";   

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
      <Route index element={<Home />} />
      </Route>
    </Routes>
  );
}
