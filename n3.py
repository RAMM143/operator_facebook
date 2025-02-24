message = '''Want to get placed without faking a Single line in your Resume.
Announcing our newest SDET(QA AUTOMATION)batch!

Elevate your career with our highly acclaimed SDET (QA Automation) program. Previous batches have secured top positions at major IT and product companies globally, thanks to the real-world skills and knowledge gained through our training without faking a single line in their resume.

Why Choose Our Program?
• Proven Success: Alumni have landed full-time roles without faking a single line in their resume.
• High Demand: Employers highly value the practical, industry-relevant training we provide.
Discover NumpyNinja
Learn more about us and our offerings at www.numpyninja.com.

Try Us Out with a One-Week Trial Class
Get a genuine feel for our program with a no-obligation, one-week trial class. See firsthand what sets us apart.
Join the session
When: Monday, February 24th at 8:30 P.M. EST
Zoom Details:
https://us06web.zoom.us/j/88954340500...
Meeting ID: 889 5434 0500
Passcode: 769959

Our program is exclusively for women, creating a supportive and empowering learning environment.

Thank you, and we look forward to seeing you at the session!'''
    m2 = '''Announcing newest trial session for DATA ANALYTICS.
Previous batches were Placed full-time recently in Major IT Companies and Product companies in the world both in India and US without faking a single line in their Resume.

Join the Session on Monday, February 24th at 9:30 P.M Eastern Standard Time.
Please find the zoom meeting detail
https://us06web.zoom.us/j/88954340500...
Meeting ID: 889 5434 0500
Passcode: 769959

In this course, you will work alongside doctors and medical professionals in tackling some of the most challenging Healthcare projects.

All projects are live. Check us out on what we do at www.numpyninja.com
Try One Week trial classes and see if this is for you.
No obligations to join the batch.

note: Our program is exclusively for Women.
Thank You!'''
async def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Sleeping... {remaining // 60} min {remaining % 60} sec left ")
        sys.stdout.flush()
        await asyncio.sleep(1)
    sys.stdout.write("\r⏳ Waking up! Ready to post the next message!          \n")

await countdown_timer(3600)  # Sleep with countdown
            print("🚀 Time to post the next message!\n\n")
import asyncio
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent, Browser, BrowserConfig

# Load environment variables
load_dotenv()

# Set up proxy configurations
proxies = [
    {'http': 'http://5.189.153.156:80', 'https': 'http://5.189.153.156:80'}
]

# Define hardcoded credentials
credentials = [
    ('', '')
]

# Initialize LLM
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=SecretStr(api_key))

class LoginAgent:
    def __init__(self, username, password, llm, proxy_config):
        self.username = username
        self.password = password
        self.llm = llm
        self.proxy_config = proxy_config
        self.browser = None
        self.context = None

    async def login(self):
        try:
            self.browser = Browser(
                config=BrowserConfig(
                    chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                    headless=False,
                    proxy=self.proxy_config
                )
            )
            self.context = await self.browser.new_context()

            login_agent = Agent(
                task=f'''
                1. Navigate to facebook.com.
                2. If already logged in, log out and then login with the following credentials:
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

class GroupPostingAgent:
    def __init__(self, llm, browser_context):
        self.llm = llm
        self.browser_context = browser_context
        self.agent = None

    async def post_in_groups(self, message, link):
        with open('groups_data.txt', 'r') as file:
            posted_groups = file.read()
        print("Using browser context:", self.browser_context)
        try:
            self.agent = Agent(
                task=f'''
                1. Open link : {link} , This link directly takes to a group.
                2. Once on the group page opened, navigate to the discussion section.
                3. Click 'Write something...' to open posting interface, and post the following message: "{message}".
                4. After Posting do log out facebook.
                5. Store the group name in results.txt.
                <Situations>
                - Allow extra time for slow page loads.
                - Do not use '#' in the search keywords.
                - If an unexpected situation occurs, restart the process.
                </Situations>
                ''',
                llm=self.llm,
                browser_context=self.browser_context,
                use_vision=True
            )

            history = await self.agent.run()
            raw_result = history.final_result()
            result = llm.invoke(
                f'This is a raw result from a browser agent after posting in a Facebook group: {raw_result}. '
                f'Your task is to return only the group name. If no group name is found, return a blank space.'
            )
            result = result.content
            print("Posted in group:", result)
            with open('groups_data.txt', 'a') as file:
                file.write(f'\n{result}')
            await asyncio.sleep(2)
        except Exception as e:
            await self.agent.browser_context.close()
            raise e

async def main():
    main_agent = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=SecretStr(api_key))
    posts_today = 0
    links = ["https://www.facebook.com/groups/122536939790676/","https://www.facebook.com/groups/160163634036729/","https://www.facebook.com/groups/1452217005074211/","https://www.facebook.com/groups/1064619337268897/","https://www.facebook.com/groups/515120252338582/","https://www.facebook.com/groups/566380604022586/"]
    message = ''''''
    for link in links:
        # If 6 posts have been made today, wait until the next day.
        if posts_today >= 6:
            print("Reached 6 posts for today. Waiting until the next cycle...")
            # For example, sleep for 18 hours before resetting the counter.
            await asyncio.sleep(18 * 3600)
            posts_today = 0
            continue

        for i, (username, password) in enumerate(credentials):
            proxy_config = proxies[i % len(proxies)]
            login_agent = LoginAgent(username, password, llm, proxy_config)
            browser_context = await login_agent.login()

            posting_agent = GroupPostingAgent(llm, browser_context)
            await posting_agent.post_in_groups(message, link)
            await login_agent.logout()

            posts_today += 1
            print("Going to sleep one hour......")
            await asyncio.sleep(3600)  # Wait for 1 hour before posting the next message

if __name__ == '__main__':
    asyncio.run(main())
