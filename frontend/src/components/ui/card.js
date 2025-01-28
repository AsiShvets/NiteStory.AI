import React from "react";

export const Card = ({ children, className }) => (
  <div className={`rounded-2xl shadow-lg p-4 bg-white ${className || ""}`}>
    {children}
  </div>
);

export const CardContent = ({ children }) => <div>{children}</div>;
