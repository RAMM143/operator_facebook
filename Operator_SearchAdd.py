import asyncio
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent, Browser, BrowserConfig
import sys
from google import genai

# Add package to path (only needed if using local development)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Define hardcoded credentials
credentials = [
    ('', '')
]

# Initialize LLM
api_key = ""

client = genai.Client(api_key=api_key)
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

class LoginAgent:
    def __init__(self, username, password, llm):
        self.username = username
        self.password = password
        self.llm = llm
        self.browser = None
        self.context = None

    async def login(self):
        try:
            self.browser = Browser(
                config=BrowserConfig(
                    chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                    headless=False
                )
            )
            self.context = await self.browser.new_context()

            login_agent = Agent(
                task=f'''
                1. Navigate to facebook.com.
                2. If already logged in, then do note it as done.
                3. Find email field (id="email") and type "{self.username}".
                4. Find password field (id="pass") and type "{self.password}".
                5. Click the login button (name="login").
                6. Verify that the news feed appears.
                ''',
                llm=self.llm,
                browser_context=self.context
            )

            await login_agent.run()
            await asyncio.sleep(2)
            return self.context
        except Exception as e:
            await self.logout()
            raise e

    async def logout(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

class groupSearching:
    def __init__(self, llm):
        self.llm = llm
        self.agent = None

    async def groupSearchAdd(self, link, browser_context, client):
        try:
            self.context = browser_context

            self.agent = Agent(
                task=f'''
                First go to this link: {link}, and see the group details, info ,name, about and analyse the group details.
                then in next tab find the most related groups in facebook to the above group.
                select any one public group and join there and in result get the group link.
                <Situations>
                - Allow extra time for slow page loads.
                - While searching for groups, do not navigate using own links or generated links. Use the given link or click the content that appeared while searching.
                - Do not use '#' in the search keywords.
                - Don't count already joined groups. Need to join in new group.
                - Need to check the group status as public or private. Only join in public group.
                - If an unexpected situation occurs, restart the process.
                </Situations>
                ''',
                llm=self.llm,
                browser_context=self.context,
                use_vision=True
            )

            history = await self.agent.run()
            raw_result = history.final_result()

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f'This is the raw result from an ai agent raw_result:{raw_result}, Your task is to get the link in this result and return. Don not include any other than link.No Sentences also not needed just give me the link only.',
            )

            result = response.text
            with open('links.txt', 'r') as file:
                content = file.read()
                if result not in content:
                    with open('links.txt', 'a') as file:
                        file.write(f'\n{result}')
                else:
                    print("Link already exists")
            await asyncio.sleep(2)
        except Exception as e:
            await self.agent.browser_context.close()
            raise e

async def main():
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=SecretStr(api_key))
    with open('links.txt', 'r') as file:
        links = file.readlines()
    for link in links:
        link = link.strip()
        for i, (username, password) in enumerate(credentials):
            login_agent = LoginAgent(username, password, llm)
            browser_context = await login_agent.login()

            posting_agent = groupSearching(llm)
            await posting_agent.groupSearchAdd(link,browser_context, client)
            await login_agent.logout()
            print("got the group name")  # Wait for 24 hour before joining in a new group
            await asyncio.sleep(3600*24)
if __name__ == '__main__':
    asyncio.run(main())
