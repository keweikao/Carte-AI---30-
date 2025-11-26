"use client";

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';

interface RestaurantSearchProps {
  onSelect: (details: { name: string }) => void;
  onChange?: (value: string) => void;
  defaultValue?: string;
}

export function RestaurantSearch({ onSelect, onChange, defaultValue }: RestaurantSearchProps) {
  const [value, setValue] = useState(defaultValue || '');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    if (onChange) {
      onChange(newValue);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Allow escape to clear the input
    if (e.key === 'Escape') {
      setValue('');
      if (onChange) onChange('');
      onSelect({ name: '' });
    }
    // Allow Enter to submit
    if (e.key === 'Enter') {
      onSelect({ name: value });
    }
  };

  return (
    <Input
      type="text"
      placeholder="例如：鼎泰豐、海底撈..."
      value={value}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      className="text-lg py-6 bg-background border-border"
      autoFocus
      aria-label="搜尋餐廳名稱"
      aria-describedby="restaurant-search-hint"
      role="searchbox"
    />
  );
}
