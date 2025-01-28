import React from "react";

export const Button = ({ children, onClick, className }) => (
  <button
    onClick={onClick}
    className={`px-4 py-2 text-white bg-blue-500 rounded-xl hover:bg-blue-600 ${className || ""}`}
  >
    {children}
  </button>
);
