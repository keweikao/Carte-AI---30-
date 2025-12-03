"""
Intelligence Layer - AI-powered data transformation
Handles menu parsing (text/vision) and review fusion using Gemini
"""

import os
import json
import base64
import httpx
import google.generativeai as genai
from typing import List, Optional

from schemas.pipeline import ParsedMenuItem, RawReview
from schemas.restaurant_profile import MenuItem, MenuItemAnalysis, DishAttributes


class MenuParser:
    """
    Parse menu items from text or images using Gemini AI
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)

    async def parse_from_text(self, content: str) -> List[ParsedMenuItem]:
        """
        Extract menu items from text content using Gemini

        Args:
            content: Menu text (markdown format from Jina)

        Returns:
            List of ParsedMenuItem objects
        """
        try:
            print(f"[MenuParser] Parsing menu from text ({len(content)} chars)")

            # Use stable text model
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            prompt = f"""
你是一個專業的菜單分析助手。請從以下文字中提取菜單資訊，並以 JSON 格式回傳。

重要規則：
1. 只提取有明確價格的菜色
2. 價格必須是數字（台幣）
3. 忽略沒有價格的項目
4. 盡可能識別菜色類別（前菜、主菜、湯品、飲料等）
5. 若有描述文字也請一併提取

回傳格式範例：
[
  {{"name": "宮保雞丁", "price": 180, "category": "主菜", "description": "經典川菜"}},
  {{"name": "酸辣湯", "price": 60, "category": "湯品", "description": null}}
]

以下是菜單內容：

{content[:5000]}
"""

            response = await model.generate_content_async(prompt)
            menu_text = response.text

            # Clean response
            if menu_text.startswith("```json"):
                menu_text = menu_text[len("```json"):].strip()
            if menu_text.endswith("```"):
                menu_text = menu_text[:-len("```")].strip()

            # Parse JSON
            menu_items_raw = json.loads(menu_text)

            # Convert to ParsedMenuItem objects
            menu_items = []
            for item_data in menu_items_raw:
                try:
                    item = ParsedMenuItem(
                        name=item_data.get("name", "Unknown"),
                        price=item_data.get("price"),
                        category=item_data.get("category", "其他"),
                        description=item_data.get("description")
                    )
                    menu_items.append(item)
                except Exception as e:
                    print(f"[MenuParser] Failed to parse menu item: {e}")
                    continue

            print(f"[MenuParser] Extracted {len(menu_items)} items from text")
            return menu_items

        except json.JSONDecodeError as e:
            print(f"[MenuParser] JSON parsing error: {e}")
            print(f"[MenuParser] Raw response: {menu_text[:500]}")
            return []
        except Exception as e:
            print(f"[MenuParser] Error parsing text: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def _classify_images(self, image_urls: List[str]) -> List[str]:
        """
        Stage 1: Quickly classify images to find menu images
        
        Args:
            image_urls: List of all image URLs
            
        Returns:
            List of image URLs that likely contain menus
        """
        try:
            print(f"[MenuParser] Stage 1: Classifying {len(image_urls)} images to find menus")
            
            # Use lightweight model for classification
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Download all images
            image_data = []
            async with httpx.AsyncClient() as client:
                for idx, url in enumerate(image_urls):
                    try:
                        print(f"[MenuParser] Downloading image {idx+1}/{len(image_urls)} for classification")
                        response = await client.get(url, timeout=30)
                        response.raise_for_status()
                        
                        # Encode to base64
                        image_base64 = base64.b64encode(response.content).decode('utf-8')
                        image_data.append({
                            'url': url,
                            'data': {
                                'mime_type': 'image/jpeg',
                                'data': image_base64
                            }
                        })
                    except Exception as e:
                        print(f"[MenuParser] Failed to download image {url[:60]}: {e}")
                        continue
            
            if not image_data:
                print(f"[MenuParser] No images successfully downloaded")
                return []
            
            # Build classification prompt
            classification_prompt = """
你是一個專業的圖片分類助手。請分析這些圖片，判斷哪些圖片包含菜單資訊。

菜單圖片的特徵：
- 包含菜品名稱和價格的列表
- 可能是紙本菜單、電子菜單、或牆上的菜單板
- 包含多個菜品項目

非菜單圖片：
- 餐廳外觀
- 室內環境
- 單一菜品照片（沒有價格）
- 顧客用餐照片

請為每張圖片判斷是否為菜單圖片，並以 JSON 格式回傳：

{
  "classifications": [
    {"image_index": 0, "is_menu": true, "confidence": 0.9, "reason": "包含多個菜品名稱和價格"},
    {"image_index": 1, "is_menu": false, "confidence": 0.8, "reason": "餐廳外觀照片"}
  ]
}

請分析以下圖片：
"""
            
            # BATCH PROCESSING: Process images in batches of 5 to avoid quota limits
            BATCH_SIZE = 5
            all_menu_urls = []
            
            for batch_start in range(0, len(image_data), BATCH_SIZE):
                batch_end = min(batch_start + BATCH_SIZE, len(image_data))
                batch = image_data[batch_start:batch_end]
                
                print(f"[MenuParser] Processing batch {batch_start//BATCH_SIZE + 1}/{(len(image_data)-1)//BATCH_SIZE + 1} ({len(batch)} images)")
                
                # Build content parts for this batch
                content_parts = [classification_prompt]
                for img_data in batch:
                    content_parts.append(img_data['data'])
                
                try:
                    # Call Gemini for classification
                    response = await model.generate_content_async(content_parts)
                    
                    result_text = response.text
                    print(f"[MenuParser] Batch {batch_start//BATCH_SIZE + 1} raw response length: {len(result_text)}")
                    print(f"[MenuParser] Batch {batch_start//BATCH_SIZE + 1} raw response preview: {result_text[:500]}")
                    
                    # Clean response
                    if result_text.startswith("```json"):
                        result_text = result_text[len("```json"):].strip()
                    if result_text.endswith("```"):
                        result_text = result_text[:-len("```")].strip()
                    
                    # Parse JSON
                    result = json.loads(result_text)
                    print(f"[MenuParser] Batch {batch_start//BATCH_SIZE + 1} parsed result: {result}")
                    
                    # Extract menu image URLs from this batch
                    classifications_count = len(result.get("classifications", []))
                    print(f"[MenuParser] Batch {batch_start//BATCH_SIZE + 1} has {classifications_count} classifications")
                    
                    for classification in result.get("classifications", []):
                        if classification.get("is_menu", False):
                            idx = classification.get("image_index", -1)
                            confidence = classification.get("confidence", 0)
                            reason = classification.get("reason", "")
                            
                            if 0 <= idx < len(batch):
                                url = batch[idx]['url']
                                all_menu_urls.append(url)
                                print(f"[MenuParser] ✓ Batch image {idx+1} is menu (confidence: {confidence:.2f}) - {reason}")
                
                except json.JSONDecodeError as json_error:
                    print(f"[MenuParser] JSON parsing error in batch: {json_error}")
                    print(f"[MenuParser] Raw response: {result_text[:1000] if 'result_text' in locals() else 'N/A'}")
                    # Fallback: treat all images in this batch as potential menus
                    print(f"[MenuParser] Fallback: treating all {len(batch)} images in batch as potential menus")
                    for img_data in batch:
                        all_menu_urls.append(img_data['url'])
                except Exception as batch_error:
                    print(f"[MenuParser] Error processing batch: {batch_error}")
                    import traceback
                    traceback.print_exc()
                    # Fallback: treat all images in this batch as potential menus
                    print(f"[MenuParser] Fallback: treating all {len(batch)} images in batch as potential menus")
                    for img_data in batch:
                        all_menu_urls.append(img_data['url'])
            
            print(f"[MenuParser] Found {len(all_menu_urls)} menu images out of {len(image_urls)} total")
            return all_menu_urls
            
        except json.JSONDecodeError as e:
            print(f"[MenuParser] Classification JSON parsing error: {e}")
            # result_text might not be defined if error occurs before first batch, or in a batch.
            # For robustness, we can try to get it if it was set in the last successful batch.
            print(f"[MenuParser] Raw response: {result_text[:500] if 'result_text' in locals() else 'N/A'}")
            # Fallback: return first 5 images
            return image_urls[:5]
        except Exception as e:
            print(f"[MenuParser] Error classifying images: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: return first 5 images
            return image_urls[:5]

    async def parse_from_images(self, image_urls: List[str]) -> List[ParsedMenuItem]:
        """
        Extract menu items from images using two-stage intelligent processing:
        Stage 1: Classify all images to find menu images
        Stage 2: OCR only on menu images

        Args:
            image_urls: List of image URLs

        Returns:
            List of ParsedMenuItem objects
        """
        try:
            print(f"[MenuParser] Two-stage intelligent image processing: {len(image_urls)} images")

            # Stage 1: Classify images to find menus
            menu_image_urls = await self._classify_images(image_urls)
            
            if not menu_image_urls:
                print(f"[MenuParser] No menu images found after classification")
                return []
            
            # Stage 2: OCR on menu images only
            print(f"[MenuParser] Stage 2: OCR on {len(menu_image_urls)} menu images")
            
            # Use Gemini 2.5 Flash for OCR
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Download and encode menu images (max 5 for API limits)
            images_to_process = menu_image_urls[:5]
            image_parts = []

            async with httpx.AsyncClient() as client:
                for idx, url in enumerate(images_to_process):
                    try:
                        print(f"[MenuParser] Downloading menu image {idx+1}/{len(images_to_process)} for OCR")
                        response = await client.get(url, timeout=30)
                        response.raise_for_status()

                        # Encode to base64
                        image_base64 = base64.b64encode(response.content).decode('utf-8')

                        image_parts.append({
                            'mime_type': 'image/jpeg',
                            'data': image_base64
                        })

                    except Exception as e:
                        print(f"[MenuParser] Failed to download image {url[:60]}: {e}")
                        continue

            if not image_parts:
                print(f"[MenuParser] No menu images successfully downloaded for OCR")
                return []

            # Build OCR prompt
            text_prompt = """
你是一個專業的菜單 OCR 助手。請從這些菜單圖片中提取所有菜色資訊，並以 JSON 格式回傳。

重要規則：
1. 只提取有明確價格的菜色
2. 價格必須是數字（台幣，去除 $ 符號）
3. 忽略沒有價格的項目
4. 盡可能識別菜色類別（前菜、主菜、湯品、飲料、小吃等）
5. 若有描述文字也請一併提取
6. 合併所有圖片中的菜單項目

回傳格式範例：
[
  {"name": "宮保雞丁", "price": 180, "category": "主菜", "description": "經典川菜"},
  {"name": "酸辣湯", "price": 60, "category": "湯品", "description": null},
  {"name": "高麗菜鍋貼", "price": 80, "category": "小吃", "description": "10入"}
]

請仔細分析以下菜單圖片，提取所有菜色資訊：
"""

            # Build content parts (text + images)
            content_parts = [text_prompt] + image_parts

            # Call Gemini Vision API for OCR
            print(f"[MenuParser] Calling Gemini Vision for OCR with {len(image_parts)} menu images")
            response = await model.generate_content_async(content_parts)

            menu_text = response.text
            print(f"[MenuParser] OCR response length: {len(menu_text)}")

            # Clean response
            if menu_text.startswith("```json"):
                menu_text = menu_text[len("```json"):].strip()
            if menu_text.endswith("```"):
                menu_text = menu_text[:-len("```")].strip()

            # Parse JSON
            menu_items_raw = json.loads(menu_text)

            # Convert to ParsedMenuItem objects
            menu_items = []
            for item_data in menu_items_raw:
                try:
                    item = ParsedMenuItem(
                        name=item_data.get("name", "Unknown"),
                        price=item_data.get("price"),
                        category=item_data.get("category", "其他"),
                        description=item_data.get("description")
                    )
                    menu_items.append(item)
                except Exception as e:
                    print(f"[MenuParser] Failed to parse menu item: {e}")
                    continue

            print(f"[MenuParser] ✓ Extracted {len(menu_items)} items from {len(image_parts)} menu images")
            return menu_items

        except json.JSONDecodeError as e:
            print(f"[MenuParser] OCR JSON parsing error: {e}")
            print(f"[MenuParser] Raw response: {menu_text[:500] if 'menu_text' in locals() else 'N/A'}")
            return []
        except Exception as e:
            print(f"[MenuParser] Error in two-stage image processing: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def extract_from_reviews(self, reviews: List[RawReview], restaurant_name: str) -> List[ParsedMenuItem]:
        """
        Extract menu items from customer reviews using Gemini AI
        This is an intelligent fallback when menu is not available
        
        Args:
            reviews: List of customer reviews
            restaurant_name: Name of the restaurant
            
        Returns:
            List of ParsedMenuItem objects extracted from reviews
        """
        try:
            print(f"[MenuParser] Extracting dishes from {len(reviews)} reviews")
            
            if not reviews:
                return []
            
            # Use Gemini to analyze reviews with structured output
            generation_config = {
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "dishes": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "name": {"type": "STRING"},
                                    "category": {"type": "STRING"},
                                    "description": {"type": "STRING"},
                                    "mention_count": {"type": "INTEGER"}
                                },
                                "required": ["name", "category", "description"]
                            }
                        }
                    }
                }
            }
            
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                generation_config=generation_config
            )
            
            # Prepare review text
            review_texts = []
            for review in reviews[:50]:  # Increased from 30 to 50 for better coverage
                if review.text:
                    review_texts.append(review.text)
            
            if not review_texts:
                return []
            
            combined_reviews = "\n\n---\n\n".join(review_texts)
            
            prompt = f"""
你是一個專業的餐廳菜單分析助手。請從以下顧客評論中提取菜品資訊。

餐廳名稱：{restaurant_name}

顧客評論：
{combined_reviews}

請分析這些評論，提取出被提及的菜品。

規則：
1. 只提取明確提到的菜品名稱
2. 優先提取被多次提及的菜品
3. 至少提取 5 個菜品（如果評論中有的話）
4. 最多提取 15 個菜品
5. description 要簡潔，突出特色
6. 如果無法確定分類，使用「推薦」
"""
            
            response = await model.generate_content_async(prompt)
            result_text = response.text
            
            print(f"[MenuParser] Review extraction response length: {len(result_text)}")
            
            # Parse JSON (no need to clean markdown code blocks as response is pure JSON)
            result = json.loads(result_text)
            
            # Convert to ParsedMenuItem objects
            menu_items = []
            for dish_data in result.get("dishes", []):
                try:
                    item = ParsedMenuItem(
                        name=dish_data.get("name", "Unknown"),
                        price=None,  # No price info from reviews
                        category=dish_data.get("category", "推薦"),
                        description=dish_data.get("description")
                    )
                    menu_items.append(item)
                except Exception as e:
                    print(f"[MenuParser] Failed to parse dish from review: {e}")
                    continue
            
            print(f"[MenuParser] ✓ Extracted {len(menu_items)} dishes from reviews")
            return menu_items
            
        except json.JSONDecodeError as e:
            print(f"[MenuParser] Review extraction JSON parsing error: {e}")
            print(f"[MenuParser] Raw response: {result_text[:500] if 'result_text' in locals() else 'N/A'}")
            return []
        except Exception as e:
            print(f"[MenuParser] Error extracting from reviews: {e}")
            import traceback
            traceback.print_exc()
            return []


class InsightEngine:
    """
    Fuse customer reviews with menu items using AI analysis
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)

    async def fuse_reviews(self, menu_items: List[ParsedMenuItem], reviews: List[RawReview]) -> tuple[List[MenuItem], str]:
        """
        Analyze reviews and link sentiments to specific menu items

        Args:
            menu_items: List of parsed menu items
            reviews: List of customer reviews

        Returns:
            Tuple of (enhanced menu items with ai_insight, overall review summary)
        """
        try:
            print(f"[InsightEngine] Fusing {len(reviews)} reviews with {len(menu_items)} menu items")

            if not reviews:
                print(f"[InsightEngine] No reviews to analyze")
                return self._create_basic_menu_items(menu_items), "No customer reviews available."

            # Build prompt
            menu_names = [item.name for item in menu_items]
            # Filter out reviews with None text and use first 15 valid reviews
            review_texts = [f"({r.rating}★) {r.text}" for r in reviews if r.text][:15]

            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            prompt = f"""
你是一個專業的餐廳評價分析師。請分析顧客評論，並將評論中提到的菜色與標準菜單進行對應。

標準菜單：
{json.dumps(menu_names, ensure_ascii=False)}

顧客評論：
{chr(10).join(review_texts)}

請完成兩個任務：

1. 菜色評價對應（Entity Linking）：
   - 找出評論中提到的具體菜色
   - 將該菜色的評價（正面/負面/中性）與標準菜單對應
   - 為每個菜色生成簡短摘要（例如：「肉太柴」、「湯頭濃郁」）
   - 計算提及次數

2. 整體評價摘要：
   - 用 2-3 句話總結整體用餐體驗
   - 提及最受好評和最受批評的菜色

回傳格式：
{{
  "menu_insights": [
    {{
      "dish_name": "宮保雞丁",
      "sentiment": "positive",
      "summary": "網友大推，外皮酥脆內餡多汁",
      "mention_count": 5
    }},
    {{
      "dish_name": "酸辣湯",
      "sentiment": "neutral",
      "summary": "評論中未特別提及",
      "mention_count": 0
    }}
  ],
  "overall_summary": "整體評價正面，特別推薦宮保雞丁和酸辣湯。服務態度友善，價格合理。"
}}
"""

            response = await model.generate_content_async(prompt)
            result_text = response.text

            # Clean response
            if result_text.startswith("```json"):
                result_text = result_text[len("```json"):].strip()
            if result_text.endswith("```"):
                result_text = result_text[:-len("```")].strip()

            # Parse JSON
            result = json.loads(result_text)

            # Build insight map
            insight_map = {}
            for insight_data in result.get("menu_insights", []):
                dish_name = insight_data.get("dish_name")
                insight_map[dish_name] = MenuItemAnalysis(
                    sentiment=insight_data.get("sentiment", "neutral"),
                    summary=insight_data.get("summary", "No specific feedback"),
                    mention_count=insight_data.get("mention_count", 0)
                )

            # Create enhanced menu items
            enhanced_items = []
            for item in menu_items:
                enhanced_item = MenuItem(
                    name=item.name,
                    price=item.price,
                    category=item.category,
                    description=item.description,
                    source_type="dine_in",  # Assume dine_in for scraped menus
                    is_popular=False,  # Will be determined by recommendation agent
                    is_risky=False,
                    ai_insight=insight_map.get(item.name)
                )
                enhanced_items.append(enhanced_item)

            overall_summary = result.get("overall_summary", "Customer reviews analyzed successfully.")

            print(f"[InsightEngine] Generated insights for {len(enhanced_items)} items")
            return enhanced_items, overall_summary

        except json.JSONDecodeError as e:
            print(f"[InsightEngine] JSON parsing error: {e}")
            print(f"[InsightEngine] Raw response: {result_text[:500] if 'result_text' in locals() else 'N/A'}")
            return self._create_basic_menu_items(menu_items), "Failed to analyze customer reviews."
        except Exception as e:
            print(f"[InsightEngine] Error fusing reviews: {e}")
            import traceback
            traceback.print_exc()
            return self._create_basic_menu_items(menu_items), "Failed to analyze customer reviews."

    def _create_basic_menu_items(self, parsed_items: List[ParsedMenuItem]) -> List[MenuItem]:
        """Convert ParsedMenuItem to MenuItem without insights"""
        return [
            MenuItem(
                name=item.name,
                price=item.price,
                category=item.category,
                description=item.description,
                source_type="dine_in",
                is_popular=False,
                is_risky=False,
                ai_insight=MenuItemAnalysis(
                    sentiment="neutral",
                    summary="No customer feedback available.",
                    mention_count=0
                )
            )
            for item in parsed_items
        ]


class MenuIntelligence:
    """
    Advanced menu analysis with DishAttributes generation
    Batch analyzes menu items to generate filterable and rankable attributes
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)

    async def analyze_dish_batch(
        self,
        menu_items: List[MenuItem],
        reviews: List[RawReview]
    ) -> List[MenuItem]:
        """
        Batch analyze menu items and generate DishAttributes for each

        This method enriches menu items with AI-generated attributes that enable:
        - Hard filtering (binary constraints like is_spicy, contains_beef)
        - Soft ranking (contextual attributes like flavors, textures)
        - Value assessment (sentiment_score, is_signature)

        Args:
            menu_items: List of menu items with basic info (name, price, category)
            reviews: Customer reviews for sentiment analysis

        Returns:
            Enhanced menu items with DishAttributes populated in analysis field
        """
        try:
            print(f"[MenuIntelligence] Analyzing {len(menu_items)} menu items")

            if not menu_items:
                return []

            # Use stable text model
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Build menu data for analysis
            menu_data = []
            for item in menu_items:
                item_dict = {
                    "name": item.name,
                    "price": item.price,
                    "category": item.category,
                    "description": item.description
                }

                # Add existing AI insights if available
                if item.ai_insight:
                    item_dict["review_sentiment"] = item.ai_insight.sentiment
                    item_dict["review_summary"] = item.ai_insight.summary
                    item_dict["mention_count"] = item.ai_insight.mention_count

                menu_data.append(item_dict)

            # Filter out reviews with None text and use first 15 valid reviews
            review_texts = [f"({r.rating}★) {r.text}" for r in reviews if r.text][:15]

            prompt = f"""
你是一個專業的菜單分析專家。請分析以下菜單項目，為每個菜色生成詳細的屬性標籤。

## 菜單資料
{json.dumps(menu_data, ensure_ascii=False, indent=2)}

## 顧客評論（參考）
{chr(10).join(review_texts) if review_texts else "無評論"}

## 分析任務
請為每個菜色生成以下屬性：

### 1. 硬過濾屬性 (Hard Filter Attributes)
這些是絕對的二元屬性，用於排除不符合用戶限制的菜色：
- is_spicy: 是否辣（微辣也算 true）
- is_vegan: 是否純素（完全無動物性成分）
- contains_beef: 是否含牛肉
- contains_pork: 是否含豬肉
- contains_seafood: 是否含海鮮（魚、蝦、貝類等）
- allergens: 過敏原列表（如 ["nuts", "shrimp", "milk"]）

### 2. 軟排序屬性 (Soft Ranking Attributes)
這些用於 AI 排序和推薦：
- flavors: 口味標籤，如 ["sour", "garlic_heavy", "sweet", "savory", "mild"]
- textures: 質地標籤，如 ["crispy", "soup", "chewy", "tender", "soft"]
- temperature: "hot", "cold", 或 "room"
- cooking_method: 烹飪方式，如 "fried", "steamed", "braised", "grilled", "raw"
- suitable_occasions: 適合場合，如 ["date", "group_share", "alcohol_pairing", "business", "family"]

### 3. 價值屬性 (Value Attributes)
- is_signature: 是否為招牌菜（根據菜名、價格、或評論判斷）
- sentiment_score: 評論情感分數（-1.0 到 1.0，正面為正值）
- highlight_review: 最有代表性的評論（一句話，可為 null）

## 回傳格式
請以 JSON 格式回傳每個菜色的屬性：

{{
  "dish_attributes": [
    {{
      "dish_name": "菜色名稱（必須與輸入完全相同）",
      "is_spicy": false,
      "is_vegan": false,
      "contains_beef": false,
      "contains_pork": true,
      "contains_seafood": false,
      "allergens": ["gluten"],
      "flavors": ["savory", "garlic_heavy"],
      "textures": ["crispy", "tender"],
      "temperature": "hot",
      "cooking_method": "fried",
      "suitable_occasions": ["group_share"],
      "is_signature": true,
      "sentiment_score": 0.8,
      "highlight_review": "外皮酥脆內餡多汁，網友大推"
    }}
  ]
}}

注意事項：
1. 所有菜色都必須回傳屬性（不能遺漏）
2. dish_name 必須與輸入的 name 完全一致
3. 若無法判斷某屬性，使用保守預設值（如 is_spicy=false）
4. 根據菜色名稱、類別、描述來推測屬性
5. 若有評論提及該菜色，sentiment_score 和 highlight_review 應反映評論內容
"""

            response = await model.generate_content_async(prompt)
            result_text = response.text

            # Clean response
            if result_text.startswith("```json"):
                result_text = result_text[len("```json"):].strip()
            if result_text.endswith("```"):
                result_text = result_text[:-len("```")].strip()

            # Parse JSON
            result = json.loads(result_text)

            # Build attribute map
            attribute_map = {}
            for attr_data in result.get("dish_attributes", []):
                dish_name = attr_data.get("dish_name")

                try:
                    attributes = DishAttributes(
                        # Hard Filter Attributes
                        is_spicy=attr_data.get("is_spicy", False),
                        is_vegan=attr_data.get("is_vegan", False),
                        contains_beef=attr_data.get("contains_beef", False),
                        contains_pork=attr_data.get("contains_pork", False),
                        contains_seafood=attr_data.get("contains_seafood", False),
                        allergens=attr_data.get("allergens", []),
                        # Soft Ranking Attributes
                        flavors=attr_data.get("flavors", []),
                        textures=attr_data.get("textures", []),
                        temperature=attr_data.get("temperature", "hot"),
                        cooking_method=attr_data.get("cooking_method", "unknown"),
                        suitable_occasions=attr_data.get("suitable_occasions", []),
                        # Value Attributes
                        is_signature=attr_data.get("is_signature", False),
                        sentiment_score=attr_data.get("sentiment_score", 0.0),
                        highlight_review=attr_data.get("highlight_review")
                    )
                    attribute_map[dish_name] = attributes
                except Exception as e:
                    print(f"[MenuIntelligence] Failed to parse attributes for {dish_name}: {e}")
                    continue

            # Apply attributes to menu items
            enhanced_items = []
            for item in menu_items:
                if item.name in attribute_map:
                    # Create new MenuItem with analysis
                    enhanced_item = MenuItem(
                        id=item.id,
                        name=item.name,
                        price=item.price,
                        category=item.category,
                        description=item.description,
                        image_url=item.image_url,
                        source_type=item.source_type,
                        is_popular=item.is_popular,
                        is_risky=item.is_risky,
                        analysis=attribute_map[item.name],
                        ai_insight=item.ai_insight  # Keep legacy insight
                    )
                    enhanced_items.append(enhanced_item)
                else:
                    print(f"[MenuIntelligence] No attributes generated for {item.name}, keeping original")
                    enhanced_items.append(item)

            print(f"[MenuIntelligence] Generated attributes for {len(attribute_map)} items")
            return enhanced_items

        except json.JSONDecodeError as e:
            print(f"[MenuIntelligence] JSON parsing error: {e}")
            print(f"[MenuIntelligence] Raw response: {result_text[:500] if 'result_text' in locals() else 'N/A'}")
            return menu_items  # Return original items if analysis fails
        except Exception as e:
            print(f"[MenuIntelligence] Error analyzing dishes: {e}")
            import traceback
            traceback.print_exc()
            return menu_items  # Return original items if analysis fails
