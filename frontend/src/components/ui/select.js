import React from "react";

export const Select = ({ children, onValueChange, defaultValue }) => {
  return (
    <select
      defaultValue={defaultValue}
      onChange={(e) => onValueChange(e.target.value)}
      className="px-4 py-2 border rounded-lg"
    >
      {children}
    </select>
  );
};

export const SelectTrigger = ({ children }) => <>{children}</>;

export const SelectContent = ({ children }) => <>{children}</>;

export const SelectItem = ({ value, children }) => (
  <option value={value}>{children}</option>
);
