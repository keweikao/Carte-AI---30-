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
                'occasions_tracked': list(data.get('occasion_preferences', {}).keys()),
                'restaurants_visited': len(data.get('restaurant_history', [])),
                'favorite_cuisines': list(data.get('cuisine_preferences', {}).keys())[:3]
            }
            
        except Exception as e:
            print(f"⚠️  Error getting memory stats: {e}")
            return {}
    
    async def record_restaurant_visit(self,
                                     user_id: str,
                                     restaurant_name: str,
                                     place_id: Optional[str],
                                     cuisine_type: str,
                                     budget_spent: int,
                                     occasion: str,
                                     selected_dishes: List[str],
                                     rating: Optional[float] = None) -> bool:
        """
        Record a restaurant visit to build dining history
        
        Args:
            user_id: User identifier
            restaurant_name: Name of the restaurant
            place_id: Google Place ID
            cuisine_type: Type of cuisine (e.g., "台菜", "日式", "義式")
            budget_spent: Amount spent
            occasion: Dining occasion
            selected_dishes: List of dish names ordered
            rating: User rating (1-5)
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            timestamp = datetime.now()
            
            # Get existing data
            data = doc.to_dict() if doc.exists else {}
            restaurant_history = data.get('restaurant_history', [])
            cuisine_prefs = data.get('cuisine_preferences', {})
            budget_patterns = data.get('budget_patterns', {})
            
            # Update restaurant history
            existing_restaurant = next(
                (r for r in restaurant_history if r.get('place_id') == place_id or r.get('restaurant_name') == restaurant_name),
                None
            )
            
            if existing_restaurant:
                # Update existing entry
                existing_restaurant['visited_count'] = existing_restaurant.get('visited_count', 1) + 1
                existing_restaurant['last_visited'] = timestamp.isoformat()
                existing_restaurant['total_spent'] = existing_restaurant.get('total_spent', 0) + budget_spent
                existing_restaurant['avg_budget'] = existing_restaurant['total_spent'] / existing_restaurant['visited_count']
                if rating:
                    existing_restaurant['last_rating'] = rating
                # Add to favorite dishes
                existing_restaurant.setdefault('favorite_dishes', []).extend(selected_dishes)
                # Keep only unique dishes
                existing_restaurant['favorite_dishes'] = list(set(existing_restaurant['favorite_dishes']))[:10]
            else:
                # New restaurant entry
                restaurant_history.append({
                    'restaurant_name': restaurant_name,
                    'place_id': place_id,
                    'cuisine_type': cuisine_type,
                    'visited_count': 1,
                    'first_visited': timestamp.isoformat(),
                    'last_visited': timestamp.isoformat(),
                    'total_spent': budget_spent,
                    'avg_budget': budget_spent,
                    'favorite_dishes': selected_dishes[:10],
                    'last_rating': rating
                })
            
            # Update cuisine preferences
            if cuisine_type not in cuisine_prefs:
                cuisine_prefs[cuisine_type] = {'count': 0, 'total_rating': 0, 'avg_rating': 0}
            
            cuisine_prefs[cuisine_type]['count'] += 1
            if rating:
                cuisine_prefs[cuisine_type]['total_rating'] += rating
                cuisine_prefs[cuisine_type]['avg_rating'] = cuisine_prefs[cuisine_type]['total_rating'] / cuisine_prefs[cuisine_type]['count']
            
            # Update budget patterns by occasion
            if occasion not in budget_patterns:
                budget_patterns[occasion] = {'total': 0, 'count': 0, 'min': budget_spent, 'max': budget_spent}
            
            budget_patterns[occasion]['total'] += budget_spent
            budget_patterns[occasion]['count'] += 1
            budget_patterns[occasion]['avg'] = budget_patterns[occasion]['total'] / budget_patterns[occasion]['count']
            budget_patterns[occasion]['min'] = min(budget_patterns[occasion]['min'], budget_spent)
            budget_patterns[occasion]['max'] = max(budget_patterns[occasion]['max'], budget_spent)
            
            # Save updated data
            doc_ref.set({
                'restaurant_history': restaurant_history,
                'cuisine_preferences': cuisine_prefs,
                'budget_patterns': budget_patterns,
                'last_updated': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            print(f"✓ Recorded visit to {restaurant_name} for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error recording restaurant visit: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def update_dining_patterns(self,
                                    user_id: str,
                                    party_size: int,
                                    dining_style: str,
                                    occasion: str) -> bool:
        """
        Update user's dining patterns (called after each recommendation)
        
        Args:
            user_id: User identifier
            party_size: Number of people
            dining_style: "Shared" or "Individual"
            occasion: Dining occasion
        
        Returns:
            Success status
        """
        if not self.db or not user_id:
            return False
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            data = doc.to_dict() if doc.exists else {}
            patterns = data.get('dining_patterns', {
                'party_sizes': [],
                'dining_styles': {},
                'occasions': {}
            })
            
            # Track party sizes
            patterns['party_sizes'].append(party_size)
            # Keep last 20 records
            patterns['party_sizes'] = patterns['party_sizes'][-20:]
            # Calculate preferred party size (mode)
            if patterns['party_sizes']:
                patterns['preferred_party_size'] = max(set(patterns['party_sizes']), key=patterns['party_sizes'].count)
            
            # Track dining styles
            patterns['dining_styles'][dining_style] = patterns['dining_styles'].get(dining_style, 0) + 1
            # Determine preferred style
            patterns['preferred_dining_style'] = max(patterns['dining_styles'], key=patterns['dining_styles'].get)
            
            # Track occasions
            patterns['occasions'][occasion] = patterns['occasions'].get(occasion, 0) + 1
            # Get frequent occasions (top 3)
            sorted_occasions = sorted(patterns['occasions'].items(), key=lambda x: x[1], reverse=True)
            patterns['frequent_occasions'] = [occ for occ, _ in sorted_occasions[:3]]
            
            # Save
            doc_ref.set({
                'dining_patterns': patterns,
                'last_updated': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating dining patterns: {e}")
            return False
    
    async def get_restaurant_recommendations_from_history(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get restaurant recommendations based on user's history
        
        Args:
            user_id: User identifier
            limit: Number of recommendations
        
        Returns:
            List of recommended restaurants
        """
        if not self.db or not user_id:
            return []
        
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return []
            
            data = doc.to_dict()
            restaurant_history = data.get('restaurant_history', [])
            
            # Sort by visit count and rating
            sorted_restaurants = sorted(
                restaurant_history,
                key=lambda r: (r.get('visited_count', 0), r.get('last_rating', 0)),
                reverse=True
            )
            
            return sorted_restaurants[:limit]
            
        except Exception as e:
            print(f"⚠️  Error getting restaurant recommendations: {e}")
            return []
    
    async def get_enriched_memory_context(self, user_id: str, occasion: Optional[str] = None, restaurant_name: Optional[str] = None) -> str:
        """
        Get enriched memory context including restaurant history and patterns
        
        Args:
            user_id: User identifier
            occasion: Current occasion
            restaurant_name: Current restaurant (to check if visited before)
        
        Returns:
            Enriched memory string for Prompt injection
        """
        if not self.db or not user_id:
            return ""
        
        try:
            # Get basic memory
            basic_memory = await self.get_personal_memory(user_id, occasion)
            
            # Get additional context
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return basic_memory
            
            data = doc.to_dict()
            enriched_lines = [basic_memory] if basic_memory else []
            
            # Restaurant history context
            if restaurant_name:
                restaurant_history = data.get('restaurant_history', [])
                visited_restaurant = next(
                    (r for r in restaurant_history if r.get('restaurant_name') == restaurant_name),
                    None
                )
                
                if visited_restaurant:
                    enriched_lines.append(f"\n**🏪 You've Been Here Before:**")
                    enriched_lines.append(f"  - Visited {visited_restaurant.get('visited_count')} times")
                    enriched_lines.append(f"  - Avg Budget: ${visited_restaurant.get('avg_budget', 0):.0f}")
                    if visited_restaurant.get('favorite_dishes'):
                        enriched_lines.append(f"  - Your Favorites: {', '.join(visited_restaurant['favorite_dishes'][:3])}")
            
            # Budget pattern context
            if occasion:
                budget_patterns = data.get('budget_patterns', {})
                if occasion in budget_patterns:
                    pattern = budget_patterns[occasion]
                    enriched_lines.append(f"\n**💰 Your {occasion.title()} Budget Pattern:**")
                    enriched_lines.append(f"  - Typical Range: ${pattern.get('min', 0)}-${pattern.get('max', 0)}")
                    enriched_lines.append(f"  - Average: ${pattern.get('avg', 0):.0f}")
            
            # Cuisine preferences
            cuisine_prefs = data.get('cuisine_preferences', {})
            if cuisine_prefs:
                top_cuisines = sorted(cuisine_prefs.items(), key=lambda x: x[1].get('count', 0), reverse=True)[:3]
                if top_cuisines:
                    enriched_lines.append(f"\n**🍜 Your Favorite Cuisines:**")
                    for cuisine, stats in top_cuisines:
                        enriched_lines.append(f"  - {cuisine} (visited {stats.get('count')} times, avg rating: {stats.get('avg_rating', 0):.1f})")
            
            return "\n".join(enriched_lines) if enriched_lines else ""
            
        except Exception as e:
            print(f"⚠️  Error getting enriched memory: {e}")
            return basic_memory
