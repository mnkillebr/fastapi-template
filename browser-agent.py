from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from app.core.config import settings
import asyncio

gemini_llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    api_key=settings.GEMINI_API_KEY,
    temperature=0.0,
    max_retries=2,
)
openai_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
    max_retries=2,
    # other params...
)

sensitive_data = {'tradingview_username': settings.TRADING_VIEW_USERNAME, 'tradingview_password': settings.TRADING_VIEW_PASSWORD}

async def main():
    agent = Agent(
        task="""Go to tradingview.com and click the person icon and select sign in.
        Sign in by clicking the google icon or text that says "Sign in with Google".
        Follow the google login flow using the username tradingview_username and password tradingview_password.
        After login, go to https://www.tradingview.com/symbols/ETHUSD/?exchange=COINBASE and click "See on Supercharts".
        Change the timeframe to "1h". Between the Save button and the magnifying glass, there is a down caret button.
        The button should have a tooltip or aria-label "Manage layouts".
        If you click this "Manage layouts", a menu will show up with an menu item option to "Export chart data...".
        If a modal shows up that says "Save this chart" you clicked the wrong button; so close that modal if that happens.
        Click "Export chart data..." span to export the chart data for the 1 hr timeframe chart.
        A popup/modal should show with an option to change the time format. Select the "ISO time" from the dropdown.
        Then click the "Export" button to download the data.
        """,
        # llm=openai_llm,
        llm=gemini_llm,
        sensitive_data=sensitive_data
    )
    result = await agent.run()
    print(result)

asyncio.run(main())