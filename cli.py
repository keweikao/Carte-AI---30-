import argparse
import json
from ai_dining_agent import DiningAgent

def main():
    parser = argparse.ArgumentParser(description="AI 點餐經紀人：根據您的偏好推薦菜色。")
    parser.add_argument("restaurant_name", type=str, help="餐廳名稱")
    parser.add_argument("total_budget", type=float, help="總預算")
    parser.add_argument("mode", type=str, choices=["sharing", "individual"], help="點餐模式 (sharing 或 individual)")
    parser.add_argument("--tags", type=str, default="", help="飲食偏好標籤，以逗號分隔 (例如: 不吃牛,不吃辣)")
    parser.add_argument("--note", type=str, default="", help="額外備註 (例如: 有長輩,有小孩)")

    args = parser.parse_args()

    tags_list = [tag.strip() for tag in args.tags.split(',') if tag.strip()]

    agent = DiningAgent(
        restaurant_name=args.restaurant_name,
        total_budget=args.total_budget,
        mode=args.mode,
        tags=tags_list,
        note=args.note
    )

    recommendations = agent.run()
    print(json.dumps(recommendations, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
