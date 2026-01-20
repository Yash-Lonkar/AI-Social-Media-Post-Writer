import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts_data = json.load(f)

        self.df = pd.json_normalize(posts_data)

        # Categorize post length
        self.df["length"] = self.df["line_count"].apply(self.categorize_length)

        # Collect unique tags
        all_tags = self.df["tags"].sum()
        self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df["tags"].apply(lambda tags: tag in tags)) &
            (self.df["language"] == language) &
            (self.df["length"] == length)
        ]
        return df_filtered.to_dict(orient="records")

    @staticmethod
    def categorize_length(line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    filtered_posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(filtered_posts)
