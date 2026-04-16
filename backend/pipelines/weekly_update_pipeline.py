from prefect import flow, task
import subprocess
import sys

def run_script(script_path: str):
    subprocess.run([sys.executable, "-m", script_path], check=True)

@task
def scrape_homes():
    run_script("backend.scripts.scrape_homes")

@task
def scrape_ads():
    run_script("backend.scripts.scrape_ads")

@task
def scrape_news():
    run_script("backend.scripts.scrape_all_news")

@task
def scrape_releases():
    run_script("backend.scripts.scrape_releases")

@task
def embed_homes():
    run_script("backend.scripts.generate_home_embeddings")

@task
def embed_ads():
    run_script("backend.scripts.generate_ads_embeddings")

@task
def embed_news():
    run_script("backend.scripts.generate_news_embeddings")

@task
def embed_releases():
    run_script("backend.scripts.generate_release_embeddings")

@flow
def weekly_data_pipeline():
    scrape_homes()
    scrape_ads()
    scrape_news()
    scrape_releases()

    embed_homes()
    embed_ads()
    embed_news()
    embed_releases()

if __name__ == "__main__":
    weekly_data_pipeline()
