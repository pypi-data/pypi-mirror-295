import json
import logging
from typing import List

from .gen_base_v3 import GenBaseV3
from .gen_course_image_prompt import CourseImagePromptModel
from .models import CourseArticleImagesPromptsModel, CourseArticleWTitleModel, CourseArticleWIDModel
from .utils import remove_html


class GenArticleImagesPrompts(GenBaseV3):
    """
    Generator class for article images prompts.
    """
    PROMPT_NAME = "gen_card_images_prompts"

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, lang=None, verbose=verbose, logger=self.logger)

    def parse_output(self, output: str) -> CourseImagePromptModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            return json.loads(output)["articles"]
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 articles: List[CourseArticleWIDModel],
                 ) -> List[CourseArticleImagesPromptsModel]:

        course_info = ""
        for index, article in enumerate(articles, start=1):
            course_info += f"{index}. {remove_html(article.title)}\n\t{remove_html(article.content)}\n\n"

        prompts_data = self.generate_output(
            course_info=course_info,
        )

        selected_articles = [entry["title"] for entry in prompts_data]

        articles_prompts = []
        for article in articles:
            if article.title in selected_articles:
                articles_prompts.append(CourseArticleImagesPromptsModel(
                    article_id=article.id,
                    prompt=prompts_data[selected_articles.index(article.title)]["prompt"],
                ))

        return articles_prompts
