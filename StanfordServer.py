from nltk.parse.corenlp import CoreNLPServer
from pycorenlp import StanfordCoreNLP
import requests, os

class StanfordServer():
    def __init__(self, JAVA_HOME, DOWNLOAD_HOME, STANFORD_HOME, STANFORD_SERVER):
        self.JAVA_HOME = JAVA_HOME
        self.DOWNLOAD_HOME = DOWNLOAD_HOME
        self.STANFORD_HOME = STANFORD_HOME
        self.STANFORD_SERVER = STANFORD_SERVER

    def start_core_nlp_server(self):
        os.environ['JAVAHOME'] = self.JAVA_HOME
        HOMEDIR = os.path.expanduser("~")
        DOWNLOAD_HOME = os.path.join(HOMEDIR, self.DOWNLOAD_HOME)
        STANFORD_HOME = os.path.join(DOWNLOAD_HOME, self.STANFORD_HOME)

        print('Stanford_Directory: ', STANFORD_HOME)

        # # The server needs to know the location of the following files:
        # #   - stanford-corenlp-X.X.X.jar
        # #   - stanford-corenlp-X.X.X-models.jar
        # # Create the server
        server = CoreNLPServer(
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2-models.jar"),
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2.jar"),
            os.path.join(STANFORD_HOME, "stanford-english-corenlp-2018-10-05-models.jar"),
        )
        # # Start the server in the background
        server.start()
        print("Server Started")

    def startServer(self):
        try:
            response = requests.get(self.STANFORD_SERVER)
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            self.start_core_nlp_server()
        return StanfordCoreNLP(self.STANFORD_SERVER)


if __name__=='__main__':
    if os.name == 'nt':
        JAVA_HOME = 'C:\\Program Files\\Java\\jdk1.8.0_201\\bin\\java.exe'
        DOWNLOAD_HOME = 'Downloads'
        STANFORD_HOME = 'stanford-corenlp-full-2018-10-05'
    else:
        JAVA_HOME = '/usr/lib/jvm/java-8-oracle/'
        DOWNLOAD_HOME = 'ttp_sense_python'
        STANFORD_HOME = 'lib'
    STANFORD_SERVER = 'http://localhost:9000'
    model_STANFORD = StanfordServer(JAVA_HOME, DOWNLOAD_HOME, STANFORD_HOME, STANFORD_SERVER).startServer()