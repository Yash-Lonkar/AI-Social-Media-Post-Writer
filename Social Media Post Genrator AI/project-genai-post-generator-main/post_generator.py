from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    # Base prompt
    prompt = f'''
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
'''

    # Instructions for Hinglish
    if language.lower() == "hinglish":
        prompt += "If Language is Hinglish, it means it is a mix of Hindi and English. The script for the generated post should always be English.\n"

    # Instructions for Japanese
    elif language.lower() == "japanese":
        prompt += "If Language is Japanese, the post should be written entirely in Japanese script. Keep it natural and suitable for LinkedIn.\n"

    # Include few-shot examples if available
    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1:  # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    # Example usage for all three languages
    print("---- English ----")
    print(generate_post("Medium", "English", "Mental Health"))

    print("\n---- Hinglish ----")
    print(generate_post("Medium", "Hinglish", "Mental Health"))

    print("\n---- Japanese ----")
    print(generate_post("Medium", "Japanese", "メンタルヘルス"))  # "Mental Health" in Japanese
