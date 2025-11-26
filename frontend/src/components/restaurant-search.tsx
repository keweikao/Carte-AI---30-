"use client";

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';

interface RestaurantSearchProps {
  onSelect: (details: { name: string }) => void;
  defaultValue?: string;
}

export function RestaurantSearch({ onSelect, defaultValue }: RestaurantSearchProps) {
  const [value, setValue] = useState(defaultValue || '');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    // 簡單版本：直接使用輸入的文字作為餐廳名稱
    onSelect({ name: newValue });
  };

  return (
    <Input
      type="text"
      placeholder="例如：鼎泰豐、海底撈..."
      value={value}
      onChange={handleChange}
      className="text-lg py-6 bg-background border-border"
      autoFocus
    />
  );
}
