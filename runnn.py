import threading

import agent
import gui
import server

threading.Thread(target=server.main()).start()
threading.Thread(target=agent.main()).start()
threading.Thread(target=agent.main()).start()
gui.main()
