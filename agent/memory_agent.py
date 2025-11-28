"""
Memory Agent - Personal Memory System

This module manages user's personal dining preferences and history.
It provides personalized context to the recommendation agents.

Features:
- Track rejected dishes (with reasons)
- Track loved dishes
- Track occasion-specific preferences
- Integrate with Firestore for persistence
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from google.cloud import firestore
from dataclasses import dataclass

@dataclass
class DishMemory:
    """Represents a memory about a specific dish"""
    dish_name: str
    category: Optional[str] = None
    reason: Optional[str] = None
    occasion: Optional[str] = None
    timestamp: Optional[datetime] = None

class MemoryAgent:
    """
    Personal Memory Agent
    
    Manages individual user's dining preferences and history.
    Provides personalized context to recommendation agents.
    """
    
    def __init__(self):
        """Initialize Firestore client"""
        try:
            self.db = firestore.Client()
            self.collection = 'user_memory'
        except Exception as e:
            print(f"⚠️  Firestore initialization failed: {e}")
            self.db = None
    
    async def get_personal_memory(self, user_id: str, occasion: Optional[str] = None) -> str:
        """
        Retrieve user's personal memory formatted as Prompt context
        
        Args:
            user_id: User identifier
            occasion: Current dining occasion (optional, for filtering)
        
        Returns:
            Formatted memory string for Prompt injection
        """
        if not self.db or not user_id:
            return ""
        
        try:
            # Fetch user memory document
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return ""
            
            data = doc.to_dict()
            memory_lines = []
            
            # Section 1: Rejected Dishes (CRITICAL - Never recommend)
            rejected = data.get('rejected_dishes', [])
            if rejected:
                memory_lines.append("**🚫 NEVER Recommend (You rejected these):**")
                
                # Filter by occasion if provided
                relevant_rejected = rejected
                if occasion:
                    relevant_rejected = [d for d in rejected if d.get('occasion') == occasion or not d.get('occasion')]
                
                for dish in relevant_rejected[:10]:  # Limit to top 10
                    reason = dish.get('reason', 'No reason provided')
                    occ = dish.get('occasion', 'any occasion')
                    memory_lines.append(f"  - {dish['name']}: {reason} (in {occ})")
            
            # Section 2: Loved Dishes (HIGH PRIORITY - Recommend similar)
            loved = data.get('loved_dishes', [])
            if loved:
                memory_lines.append("\n**❤️  You LOVE These (Prioritize similar dishes):**")
                
                for dish in loved[:10]:  # Limit to top 10
                    category = dish.get('category', 'Unknown')
                    memory_lines.append(f"  - {dish['name']} ({category})")
            
            # Section 3: Occasion-Specific Preferences
            if occasion and 'occasion_preferences' in data:
                occ_prefs = data['occasion_preferences'].get(occasion, {})
                if occ_prefs:
                    memory_lines.append(f"\n**🎯 Your {occasion.title()} Preferences:**")
                    
                    if 'avoid_categories' in occ_prefs:
                        memory_lines.append(f"  - Avoid: {', '.join(occ_prefs['avoid_categories'])}")
                    if 'prefer_categories' in occ_prefs:
                        memory_lines.append(f"  - Prefer: {', '.join(occ_prefs['prefer_categories'])}")
                    if 'notes' in occ_prefs:
                        memory_lines.append(f"  - Note: {occ_prefs['notes']}")
            
            # Section 4: General Preferences
            general_prefs = data.get('general_preferences', {})
            if general_prefs:
                memory_lines.append("\n**⚙️  General Preferences:**")
                
                if 'spice_tolerance' in general_prefs:
                    memory_lines.append(f"  - Spice Level: {general_prefs['spice_tolerance']}")
                if 'portion_preference' in general_prefs:
                    memory_lines.append(f"  - Portion: {general_prefs['portion_preference']}")
                if 'price_sensitivity' in general_prefs:
                    memory_lines.append(f"  - Budget Style: {general_prefs['price_sensitivity']}")
            
            if memory_lines:
                return "\n".join(memory_lines)
            else:
                return ""
                
        except Exception as e:
            print(f"⚠️  Error fetching personal memory: {e}")
            return ""
    
    async def save_feedback(self, 
                           user_id: str,
                           recommendation_id: str,
                           selected_dishes: List[Dict[str, Any]],
                           rejected_dishes: List[Dict[str, Any]],
                           occasion: Optional[str] = None) -> bool:
        """
        Save user feedback to build personal memory
        
        Args:
            user_id: User identifier
            recommendation_id: ID of the recommendation session
            selected_dishes: List of dishes user selected/loved
            rejected_dishes: List of dishes user rejected (with reasons)
            occasion: Dining occasion
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            timestamp = datetime.now()
            
            # Prepare update data
            update_data = {
                'last_updated': firestore.SERVER_TIMESTAMP,
                'user_id': user_id
            }
            
            # Add loved dishes
            if selected_dishes:
                loved_entries = []
                for dish in selected_dishes:
                    loved_entries.append({
                        'name': dish.get('dish_name', dish.get('name')),
                        'category': dish.get('category'),
                        'occasion': occasion,
                        'timestamp': timestamp.isoformat(),
                        'recommendation_id': recommendation_id
                    })
                
                update_data['loved_dishes'] = firestore.ArrayUnion(loved_entries)
            
            # Add rejected dishes
            if rejected_dishes:
                rejected_entries = []
                for dish in rejected_dishes:
                    rejected_entries.append({
                        'name': dish.get('dish_name', dish.get('name')),
                        'reason': dish.get('reason', 'Not specified'),
                        'occasion': occasion,
                        'timestamp': timestamp.isoformat(),
                        'recommendation_id': recommendation_id
                    })
                
                update_data['rejected_dishes'] = firestore.ArrayUnion(rejected_entries)
            
            # Save to Firestore
            doc_ref.set(update_data, merge=True)
            
            print(f"✓ Saved feedback for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving feedback: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def update_occasion_preference(self,
                                        user_id: str,
                                        occasion: str,
                                        preference_updates: Dict[str, Any]) -> bool:
        """
        Update user's occasion-specific preferences
        
        Args:
            user_id: User identifier
            occasion: Dining occasion
            preference_updates: Dictionary of preference updates
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            
            # Update occasion preferences
            doc_ref.set({
                f'occasion_preferences.{occasion}': preference_updates,
                'last_updated': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            print(f"✓ Updated {occasion} preferences for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating occasion preference: {e}")
            return False
    
    async def update_general_preferences(self,
                                        user_id: str,
                                        preferences: Dict[str, Any]) -> bool:
        """
        Update user's general dining preferences
        
        Args:
            user_id: User identifier
            preferences: Dictionary of general preferences
                - spice_tolerance: 'low', 'medium', 'high'
                - portion_preference: 'small', 'regular', 'large'
                - price_sensitivity: 'budget', 'moderate', 'premium'
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            
            doc_ref.set({
                'general_preferences': preferences,
                'last_updated': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            print(f"✓ Updated general preferences for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating general preferences: {e}")
            return False
    
    async def clear_user_memory(self, user_id: str) -> bool:
        """
        Clear all memory for a user (GDPR compliance)
        
        Args:
            user_id: User identifier
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc_ref.delete()
            
            print(f"✓ Cleared all memory for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing memory: {e}")
            return False
    
    async def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about user's memory
        
        Args:
            user_id: User identifier
        
        Returns:
            Dictionary with memory statistics
        """
        if not self.db or not user_id:
            return {}
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return {
                    'has_memory': False,
                    'loved_count': 0,
                    'rejected_count': 0
                }
            
            data = doc.to_dict()
            
            return {
                'has_memory': True,
                'loved_count': len(data.get('loved_dishes', [])),
                'rejected_count': len(data.get('rejected_dishes', [])),
                'last_updated': data.get('last_updated'),
                'occasions_tracked': list(data.get('occasion_preferences', {}).keys())
            }
            
        except Exception as e:
            print(f"⚠️  Error getting memory stats: {e}")
            return {}
