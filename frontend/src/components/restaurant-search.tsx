"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { useSession } from "next-auth/react";
import { getPlaceAutocomplete } from "@/lib/api";
import { MapPin, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface RestaurantSearchProps {
  onSelect: (details: { name: string; place_id?: string }) => void;
  onChange?: (value: string) => void;
  value?: string; // Controlled value
  defaultValue?: string; // Fallback for uncontrolled mode
  name?: string;
  placeholder?: string;
  className?: string; // Allow custom styling for Input
}

interface Suggestion {
  description: string;
  place_id: string;
  main_text: string;
  secondary_text: string;
}

export function RestaurantSearch({ onSelect, onChange, value, defaultValue, name, placeholder, className }: RestaurantSearchProps) {
  const { data: session } = useSession();
  // Use controlled value if provided, otherwise use internal state
  const [internalValue, setInternalValue] = useState(defaultValue || '');
  const displayValue = value !== undefined ? value : internalValue;

  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Debounced search
  useEffect(() => {
    // Don't search if value hasn't changed significantly or is empty
    if (!displayValue.trim()) {
      setSuggestions([]);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      // Only search if we have a session token and input length > 1
      // @ts-expect-error - id_token exists on session but not in type definition
      if (displayValue.length > 1 && session?.id_token) {
        setLoading(true);
        try {
          // @ts-expect-error - id_token exists on session
          const data = await getPlaceAutocomplete(displayValue, session.id_token);
          if (data.suggestions && data.suggestions.length > 0) {
            setSuggestions(data.suggestions);
            setIsOpen(true);
          } else {
            setSuggestions([]);
            setIsOpen(false);
          }
        } catch (error) {
          console.error("Autocomplete error:", error);
        } finally {
          setLoading(false);
        }
      }
    }, 500); // 500ms debounce

    return () => clearTimeout(timer);
  }, [displayValue, session]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (value === undefined) {
      // Uncontrolled mode: update internal state
      setInternalValue(newValue);
    }
    // Always call onChange callback if provided
    if (onChange) {
      onChange(newValue);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Prevent triggering search when using IME (e.g. typing Chinese)
    if (e.nativeEvent.isComposing) {
      return;
    }

    // Allow escape to clear the input or close dropdown
    if (e.key === 'Escape') {
      if (isOpen) {
        setIsOpen(false);
      } else {
        if (value === undefined) setInternalValue('');
        if (onChange) onChange('');
        onSelect({ name: '' });
      }
    }
    // Allow Enter to submit current value (even if not selected from list)
    if (e.key === 'Enter') {
      e.preventDefault();
      setIsOpen(false);
      onSelect({ name: displayValue });
    }
  };

  const handleSelectSuggestion = (suggestion: Suggestion) => {
    const name = suggestion.main_text;
    if (value === undefined) setInternalValue(name);
    if (onChange) onChange(name);
    onSelect({ name, place_id: suggestion.place_id });
    setIsOpen(false);
  };

  return (
    <div className="relative w-full" ref={containerRef}>
      <div className="relative">
        <Input
          name={name}
          type="text"
          placeholder={placeholder || "例如：鼎泰豐、海底撈..."}
          value={displayValue}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className={cn("text-lg py-6 bg-background border-border pr-10", className)}
          autoFocus
          aria-label="搜尋餐廳名稱"
          aria-describedby="restaurant-search-hint"
          role="combobox"
          aria-expanded={isOpen}
          aria-controls="restaurant-suggestions"
        />
        {loading && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        )}
      </div>

      {isOpen && suggestions.length > 0 && (
        <ul
          id="restaurant-suggestions"
          className="absolute z-50 w-full mt-1 bg-popover border rounded-md shadow-md max-h-60 overflow-auto py-1 focus:outline-none"
          role="listbox"
        >
          {suggestions.map((suggestion) => (
            <li
              key={suggestion.place_id}
              className={cn(
                "relative flex cursor-default select-none items-center rounded-sm px-2 py-2 text-sm outline-none",
                "hover:bg-accent hover:text-accent-foreground cursor-pointer"
              )}
              onClick={() => handleSelectSuggestion(suggestion)}
              role="option"
              aria-selected={false}
            >
              <MapPin className="mr-2 h-4 w-4 text-muted-foreground shrink-0" />
              <div className="flex flex-col overflow-hidden">
                <span className="font-medium truncate">{suggestion.main_text}</span>
                <span className="text-xs text-muted-foreground truncate">
                  {suggestion.secondary_text}
                </span>
              </div>
            </li>
          ))}
          <div className="px-2 py-2 border-t mt-1">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/powered_by_google_on_white.png" alt="Powered by Google" className="h-4 w-auto opacity-70" />
          </div>
        </ul>
      )}
    </div>
  );
}