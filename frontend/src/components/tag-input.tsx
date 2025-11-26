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
    } else if (e.key === "Escape") {
      e.preventDefault();
      setInputValue("");
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
      <div className="flex flex-wrap gap-2" role="list" aria-label="已選擇的標籤">
        {value.map((tag, index) => (
          <Badge
            key={tag}
            className="flex items-center gap-1.5 cursor-pointer"
            onClick={() => removeTag(tag)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                removeTag(tag);
              }
            }}
            tabIndex={0}
            role="button"
            aria-label={`移除標籤 ${tag}`}
          >
            {tag} <X className="size-3" aria-hidden="true" />
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
        aria-label="輸入新標籤"
        aria-describedby="tag-input-hint"
        role="combobox"
        aria-expanded={activeSuggestions.length > 0}
        aria-controls="tag-suggestions"
      />
      <span id="tag-input-hint" className="sr-only">
        輸入標籤後按 Enter 新增，或按 Backspace 刪除最後一個標籤
      </span>

      {activeSuggestions.length > 0 && (
        <div id="tag-suggestions" className="flex flex-wrap gap-2 pt-1" role="listbox" aria-label="建議標籤">
          {activeSuggestions.map((sug) => (
            <Button
              key={sug.id}
              variant="outline"
              size="sm"
              className="rounded-full gap-1.5 h-auto py-1.5"
              onClick={() => addTag(sug.label)}
              role="option"
              aria-label={`新增標籤 ${sug.label}`}
            >
              {sug.icon && <span className="text-sm" aria-hidden="true">{sug.icon}</span>}
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
