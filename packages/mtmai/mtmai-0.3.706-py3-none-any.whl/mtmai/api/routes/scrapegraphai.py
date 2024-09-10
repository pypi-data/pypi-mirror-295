from fastapi import APIRouter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from pydantic import BaseModel
from scrapegraphai.graphs import SmartScraperMultiGraph

from mtmai.core.config import settings

router = APIRouter()

# ************************************************
# Define the configuration for the graph
# ************************************************
# ************************************************

# HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


class ScrapeGraphAiReq(BaseModel):
    prompt: str
    url: str


@router.post("/hello122", response_model=ScrapeGraphAiReq)
def hello122(req: ScrapeGraphAiReq):
    # Define the configuration for the scraping pipeline
    # graph_config = {
    #     "model_instance": llm_model_instance,
    #     "embedder_model_instance": embedder_model_instance,
    #     "verbose": True,
    #     "headless": False,
    # }
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm_model_instance = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_length=128,
        temperature=0.5,
        token=settings.HUGGINGFACEHUB_API_TOKEN,
    )

    embedder_model_instance = HuggingFaceInferenceAPIEmbeddings(
        api_key=settings.HUGGINGFACEHUB_API_TOKEN,
        model_name="sentence-transformers/all-MiniLM-l6-v2",
    )

    graph_config = {
        "llm": {"model_instance": llm_model_instance, "model_tokens": 2000},
        "verbose": True,
        "headless": False,
    }

    # Create the SmartScraperGraph instance
    # smart_scraper_graph = SmartScraperGraph(
    #     prompt="Find some information about what does the company do, the name and a contact email.",
    #     source="https://scrapegraphai.com/",
    #     config=graph_config,
    # )
    multiple_search_graph = SmartScraperMultiGraph(
        prompt="Who is Marco Perini?",
        source=["https://perinim.github.io/", "https://perinim.github.io/cv/"],
        schema=None,
        config=graph_config,
    )

    result = multiple_search_graph.run()
    # result = search_graph.run()
    print(result)

    # Run the pipeline
    # result = search_graph.run()
    return result
