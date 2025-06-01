import requests
import json
import os

class VocabularyCrawler:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path

    def fetch_and_save(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"✅ Data saved to {self.save_path}")

        except requests.RequestException as e:
            print(f"❌ Error fetching data: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

# Thực thi chỉ khi chạy trực tiếp file này
if __name__ == "__main__":
    url = "https://nhiney.github.io/api/vocabulary/data.json"
    save_path = os.path.join(os.path.dirname(__file__), "data/data.crawl.json")
    
    crawler = VocabularyCrawler(url, save_path)
    crawler.fetch_and_save()
