"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

interface TagInputProps {
  value: string[]; // array of selected tags
  onChange: (tags: string[]) => void;
  suggestions?: { id: string; label: string; icon: string }[];
  placeholder?: string;
  className?: string;
}

export function TagInput({
  value,
  onChange,
  suggestions = [],
  placeholder = "輸入偏好標籤...",
  className,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState("");
  const [activeSuggestions, setActiveSuggestions] = useState(suggestions);

  useEffect(() => {
    setActiveSuggestions(
      suggestions.filter(
        (suggestion) =>
          !value.includes(suggestion.label) &&
          suggestion.label.toLowerCase().includes(inputValue.toLowerCase())
      )
    );
  }, [inputValue, suggestions, value]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && inputValue.trim() !== "") {
      e.preventDefault();
      const newTag = inputValue.trim();
      if (!value.includes(newTag)) {
        onChange([...value, newTag]);
        setInputValue("");
      }
    } else if (e.key === "Backspace" && inputValue === "" && value.length > 0) {
      e.preventDefault();
      const newTags = [...value];
      newTags.pop();
      onChange(newTags);
    }
  };

  const addTag = (tag: string) => {
    if (!value.includes(tag)) {
      onChange([...value, tag]);
      setInputValue("");
    }
  };

  const removeTag = (tagToRemove: string) => {
    onChange(value.filter((tag) => tag !== tagToRemove));
  };

  return (
    <div className={cn("space-y-3", className)}>
      <div className="flex flex-wrap gap-2">
        {value.map((tag) => (
          <Badge key={tag} className="flex items-center gap-1.5 cursor-pointer" onClick={() => removeTag(tag)}>
            {tag} <X className="size-3" />
          </Badge>
        ))}
      </div>

      <Input
        type="text"
        placeholder={placeholder}
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleInputKeyDown}
        className="w-full"
      />

      {activeSuggestions.length > 0 && (
        <div className="flex flex-wrap gap-2 pt-1">
          {activeSuggestions.map((sug) => (
            <Button
              key={sug.id}
              variant="outline"
              size="sm"
              className="rounded-full gap-1.5 h-auto py-1.5"
              onClick={() => addTag(sug.label)}
            >
              {sug.icon && <span className="text-sm">{sug.icon}</span>}
              {sug.label}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
}

// Re-export Badge, though it might be defined elsewhere
import { Badge } from "@/components/ui/badge";
