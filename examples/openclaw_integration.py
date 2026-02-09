import os
import agentops
import openclaw
from dotenv import load_dotenv

load_dotenv()
agentops.init(os.getenv('AGENTOPS_API_KEY'))
claw = openclaw.initialize(api_key=os.getenv('OPENCLAW_API_KEY'))
result = claw.process('Example task')
agentops.end_session('Success')
