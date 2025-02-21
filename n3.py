#AIzaSyDI5Po0BIOY_0L5RA-vo2eKwI_K9C44SCY
'''"I am truly overwhelmed by this recognition it's something I never expected, and I'm absolutely elated. NumpyNinja has been nothing short of a game-changer for me. It was the platform that gave me the confidence and tools to step back into the workforce with renewed energy and purpose.

The NumpyNinja resume format was a revelation it transformed my resume, putting it in the spotlight and capturing the attention of recruiters like never before. The hands-on projects I worked on here not only honed my skills but also elevated my profile, opening doors to opportunities I once thought were out of reach.
What's truly remarkable is how NumpyNinja stays unwavering in its noble mission of being the most career-centric company for women. Being part of this journey has been an honor, and I'm incredibly proud to have contributed to such a transformative community. I promise to continue supporting and championing this mission in any way I can, because NumpyNinja isn't just a platform-it's a movement that changes lives."

                                    ------Nidhi A

A NumpyNinja's success story: Landing a Product Manager role at one of the world's leading mobile service companies.
Is this the moment that kickstarts your own inspiring journey?
m1 = '''"Moving to the USA with a career gap left me feeling lost and unsure of my future. I lacked confidence and didn't know where to start. That's when my neighbor, a NumpyNinja member, introduced me to this incredible program -- and it changed everything.

Through live projects, Jobathon, and hackathons, I gained real-world experience, industry skills, and the confidence to re-enter the workforce. The structured guidance made all the difference.

Today, after a long break, I've successfully restarted my career-all thanks to NumpyNinja."

                                       -----Shruthi C

This is the success story of NumpyNinja who successfully overcame a career break through our program and secured a position at one of the largest dental insurance companies.
If you're feeling stuck, take that first step. Success will follow!
Connect with us on Messenger - https://m.me/numpyninjainc'''

m2 = '''"Restarting my career after a 9-year gap seemed daunting, but NumpyNinja changed everything.

The Jobathon at Numpy Ninja was a turning point—it gave me real-world experience, sharpened my technical skills, and boosted my confidence. The hands-on projects and interview-focused training played a crucial role in helping me secure a position in a top IT company.

If you trust the process at NumpyNinja, the sky is the limit to what you can achieve!"
                                     -----Anandhi K

This is the success story of NumpyNinja who has excelled through our program and secured a position at a leading financial information and analytics company.

Could this be the beginning of your own incredible journey?
Connect with us on Messenger - https://m.me/numpyninjainc'''

m3 = '''"Joining NumpyNinja was a turning point in my career. At a time when I was uncertain about job offers and training programs, I chose to invest in real learning rather than quick fixes. Balancing motherhood with classes, assignments, and late-night hackathons was challenging, but the experience was truly rewarding.

Through this program, I gained not only technical skills but also an incredible support system of peers and mentors. The hands-on projects, teamwork, and adrenaline-filled hackathons gave me the confidence to step into the job market fully prepared.

Job hunting is tough, but trust the process-your time will come! Grateful to NumpyNinja and the amazing mentors for making this journey so impactful."

                              -----Saranya M

Another Numpy Ninja success story-transforming career breaks into amazing comebacks!

Why wait? Your success is just one step away!
Connect with us on Messenger - https://m.me/numpyninjainc'''
 Connect with us on Messenger - https://m.me/numpyninjainc'''
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
