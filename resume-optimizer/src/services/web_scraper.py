import asyncio
from langchain_community.document_loaders import PlaywrightURLLoader


class WebScraper:
    """
    A class to scrape the text content from a given URL.

    This scraper is designed to handle web pages that load content
    dynamically using JavaScript.
    """

    def scrape_text_from_url(self, url: str) -> str:
        """
        Takes a single URL, launches a headless browser to scrape the
        webpage, extracts the main text content, and returns it.

        Args:
            url: The URL of the webpage to scrape.

        Returns:
            The extracted text content of the page as a single string.
            Returns an error message if content cannot be fetched.
        """
        if not url:
            return "Error: No URL provided."

        print(f"Scraping text from: {url}")

        # PlaywrightURLLoader is used to handle JavaScript-driven sites.
        # It loads the URL in a headless browser, allowing all content to render.
        # We also tell it to remove common clutter like headers and footers.
        loader = PlaywrightURLLoader(
            urls=[url],
            remove_selectors=["header", "footer", "nav"],
            continue_on_failure=True,
        )

        try:
            # The .load() method fetches and parses the content.
            # It returns a list of LangChain "Document" objects.
            documents = loader.load()

            # We check if the list is empty or the content is missing.
            if documents and documents[0].page_content:
                print("Scraping successful.")
                # The actual text is in the page_content attribute of the first document.
                return documents[0].page_content
            else:
                # Add more debug info here
                print(f"Loader returned: {documents}")
                return (
                    f"Error: Could not retrieve content from the URL: {url}\n"
                    f"Loader returned: {documents}"
                )

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"An error occurred during scraping: {e}\n{tb}")
            return f"An error occurred during scraping: {e}\n{tb}"
